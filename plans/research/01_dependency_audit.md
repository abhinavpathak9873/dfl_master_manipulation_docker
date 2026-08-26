# External dependency audit

## Accepted pins

| Dependency | Pin | Planned use | Main risk | Required gate |
|---|---|---|---|---|
| Doosan `doosan-robot2` | Jazzy commit [`816ecb5`](https://github.com/DoosanRobotics/doosan-robot2/commit/816ecb5d1c2599303eaf9540216afa03552f80ad) | Vendor descriptions, hardware interface, emulator, Gazebo, MoveIt configuration source, messages, and controller behavior | Sparse releases, controller-generation build option, real bringup reports, namespace collisions | Build both models; run one emulator per identity; run mixed concurrent instances; verify real hardware, cancel, stop, and firmware paths |
| Gazebo | Harmonic paired with ROS 2 Jazzy | Primary physics simulator and local test path | Tool/contact fidelity and multiple emulator resource use | Headless launch, deterministic reset, cancel/stop, all robot/tool models, representative grasp task |
| Isaac ROS | 4.6 release | SAM2 and FoundationPose integration on the desktop GPU | Exact driver/CUDA/JetPack requirements; memory growth; NITROS graph coupling | Pinned image build, D455 graph, recovery tests, GPU memory slope, two-hour run |
| M3T | Commit [`f021061`](https://github.com/DLR-RM/3DObjectTracking/commit/f02106186a1e756450226b3b793e309506817c58) after spike | Multi-body RGB-D tracking seeded by FoundationPose | No ROS package, no public confidence signal, OpenGL/headless build, local minima and occlusion | Noble/Jazzy build, ROS adapter, recorded data, false-stable drift, health heuristic, reseed |
| Genesis | 1.3.3 after upgrade smoke | Secondary simulator with the same task/controller contract | No official ROS or Doosan bridge; rapidly changing Python stack | URDF import, official-emulator feasibility, FollowJointTrajectory semantics, JointState, `/clock`, reset, contact/tool behavior |
| CaP-X | Reference checkout only | API discoverability, skill documentation, fixtures, and evaluation patterns | Incompatible runtime, simulator, dependency, and repository assumptions | Written accept/reject mapping; no runtime dependency added |

## Doosan findings

The official Jazzy branch contains M1013 and H2515 description and MoveIt assets. Its virtual mode starts a Docker-hosted controller emulator. Multi-robot Gazebo uses a unique robot name, port, pose, and TF remapping for each instance. The README also requires controller firmware 2.12 or newer for MoveIt and a `-DDRCF_VER=3` build for controller generation 3.x. See the [official Jazzy README](https://github.com/DoosanRobotics/doosan-robot2/blob/jazzy/README.md).

The branch has no suitable semantic release for this plan, so the workspace manifest must pin the audited commit. Real-hardware support is claimed upstream, but current issues show that build success does not prove controller-manager or joint-state behavior. Phase 00 therefore treats real bringup as a hardware gate.

Gazebo Harmonic is the supported pairing for Jazzy according to the [Gazebo ROS installation guide](https://gazebosim.org/docs/latest/ros_installation/). The new project must not import the old Humble Gazebo dependency set unchanged.

## Isaac ROS findings

Isaac ROS 4.6 is a Jazzy release for Ubuntu 24.04. The x86 requirements include an Ampere-or-newer GPU, sufficient VRAM, current NVIDIA drivers, and the release's CUDA baseline. Jetson Orin support is tied to the matching JetPack release. Use the versioned [4.6 requirements](https://nvidia-isaac-ros.github.io/v/release-4.6/getting_started/index.html) rather than floating latest documentation.

SAM2 accepts point or bounding-box prompts and publishes a label mask. The 4.6 release notes document live-camera GPU-memory growth after prompts. FoundationPose consumes rectified RGB, depth, CameraInfo, a segmentation mask, and a target mesh; it publishes `vision_msgs/Detection3DArray` and tensor pose output. Its tracking node can reset to estimation. See the [release notes](https://nvidia-isaac-ros.github.io/releases/index.html), [SAM2 documentation](https://nvidia-isaac-ros.github.io/v/release-4.6/repositories_and_packages/isaac_ros_image_segmentation/isaac_ros_segment_anything2/index.html), and [FoundationPose documentation](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_pose_estimation/isaac_ros_foundationpose/).

## M3T findings

M3T is an MIT-licensed C++17/CMake library, not an ament package. It coordinates cameras, bodies, modalities, detectors, tracking iterations, and publishers through a synchronous tracker. It supports region, depth, texture, multiple bodies, and multiple cameras, but the project must supply ROS image adapters, pose initialization, health output, and recovery.

The published work describes local optimization limits under large pose jumps, occlusion, ambiguous silhouettes, similar foreground/background colors, non-rigid objects, and inaccurate meshes. Published performance used different hardware and datasets and sometimes ground-truth initialization. It cannot be used as the DFL performance claim. See the [M3T source](https://github.com/DLR-RM/3DObjectTracking/tree/master/M3T) and [tracking dissertation](https://mediatum.ub.tum.de/doc/1696259/1696259.pdf).

## Genesis findings

Genesis 1.3.3 supports URDF/xacro import, joint indexing, position and velocity control, force control, and fixed-step simulation through Python. The official source does not provide a ROS 2 or Doosan integration. This is an inference from the official trees, not an upstream statement. See the [1.3.3 release](https://github.com/Genesis-Embodied-AI/genesis-world/releases/tag/v1.3.3) and [joint-control API](https://genesis-world.readthedocs.io/en/latest/user_guide/getting_started/control_your_robot.html).

The Phase 00 spike first tests whether the Doosan emulator can remain authoritative while a project bridge mirrors state into Genesis. Replacing the emulator with a Genesis-owned trajectory controller would change the accepted requirement, so that fallback needs user approval.

## Upgrade rule

Every adopted external dependency is locked by an ordinary source pin plus image
digest or source commit. An upgrade packet records the old and new pins,
upstream changes, focused affected tests, benchmark deltas, data migrations, and
rollback. A release may summarize those pins in one readable record; no runtime
manifest registry is required. Floating branch or latest-at-build resolution is
prohibited.
