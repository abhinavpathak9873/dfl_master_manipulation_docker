"""Expose FollowJointTrajectory over the Doosan Gazebo position controller."""

from __future__ import annotations

import argparse
import threading
import time

import rclpy
from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray


JOINTS = [f"joint_{index}" for index in range(1, 7)]


class TrajectoryAdapter(Node):
    def __init__(self, robot: str) -> None:
        super().__init__("trajectory_adapter", namespace=robot)
        self._positions: dict[str, float] = {}
        self._lock = threading.Lock()
        self._commands = self.create_publisher(Float64MultiArray, "dsr_position_controller/commands", 10)
        self.create_subscription(JointState, "joint_states", self._joint_state, 10)
        self._server = ActionServer(
            self,
            FollowJointTrajectory,
            "dsr_position_controller/follow_joint_trajectory",
            execute_callback=self._execute,
            goal_callback=self._goal,
            cancel_callback=lambda _: CancelResponse.ACCEPT,
        )

    def _joint_state(self, message: JointState) -> None:
        with self._lock:
            self._positions = dict(zip(message.name, message.position))

    def _goal(self, request: FollowJointTrajectory.Goal) -> GoalResponse:
        if request.trajectory.joint_names != JOINTS or not request.trajectory.points:
            self.get_logger().error(f"expected non-empty trajectory ordered as {JOINTS}")
            return GoalResponse.REJECT
        if any(len(point.positions) != 6 for point in request.trajectory.points):
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def _execute(self, goal_handle):
        trajectory = goal_handle.request.trajectory
        result = FollowJointTrajectory.Result()
        started = time.monotonic()
        for point in trajectory.points:
            target_time = point.time_from_start.sec + point.time_from_start.nanosec / 1e9
            while time.monotonic() - started < target_time:
                if goal_handle.is_cancel_requested:
                    self._hold()
                    goal_handle.canceled()
                    result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
                    result.error_string = "canceled; last measured position commanded as hold"
                    return result
                time.sleep(0.01)
            command = Float64MultiArray()
            command.data = list(point.positions)
            self._commands.publish(command)
        deadline = time.monotonic() + 5.0
        target = dict(zip(JOINTS, trajectory.points[-1].positions))
        while time.monotonic() < deadline:
            with self._lock:
                measured = dict(self._positions)
            if measured and all(abs(measured.get(name, value + 1.0) - value) < 0.035 for name, value in target.items()):
                goal_handle.succeed()
                result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
                return result
            if goal_handle.is_cancel_requested:
                self._hold()
                goal_handle.canceled()
                result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
                return result
            time.sleep(0.02)
        goal_handle.abort()
        result.error_code = FollowJointTrajectory.Result.GOAL_TOLERANCE_VIOLATED
        result.error_string = f"Gazebo joints did not reach target; measured={measured}, target={target}"
        return result

    def _hold(self) -> None:
        with self._lock:
            values = [self._positions.get(name, 0.0) for name in JOINTS]
        message = Float64MultiArray()
        message.data = values
        self._commands.publish(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--robot", required=True, choices=("picker1", "picker2", "h2515"))
    args, _ = parser.parse_known_args()
    rclpy.init()
    node = TrajectoryAdapter(args.robot)
    executor = MultiThreadedExecutor(num_threads=3)
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
