# Namespaces, TF, units, and time

## Goal

Make multi-robot data and transforms unambiguous using normal ROS conventions.

## Task-script payoff

Picker 1 and Picker 2 can run together, poses say what frame they use, and stale
camera/tracker data fails clearly instead of moving the wrong robot.

## Work

1. Assign stable namespaces and TF prefixes to Picker 1, Picker 2, H2515, their
   controllers, bases, tools, cameras, and integration nodes.
2. Audit upstream Doosan/global names and patch or remap only concrete
   collisions.
3. Follow REP-103: metres, radians, right-handed frames, standard optical frames,
   and explicit quaternion order.
4. Preserve sensor source timestamps through segmentation, pose, tracking,
   alignment, scene updates, and run evidence.
5. Use the ROS clock appropriate to the selected mode and detect mixed wall/sim
   time.
6. Centralize only small repeated TF lookup/freshness helpers; keep the actual
   frame target explicit at call sites.
7. Define actionable missing, extrapolated, and stale transform errors.
8. Test concurrent Pickers, delayed camera data, reset/clock jumps, and scene
   transformations with standard ROS tools.

## Acceptance

- No node/topic/action/service/controller/parameter/TF collision exists between
  both Pickers.
- Pose conversions retain frame and timestamp where relevant.
- Old perception data cannot be presented as a current grasp target.
- The solution uses ROS TF/time rather than a parallel frame/time system.

## Non-goals

- Hiding frame transforms or silently choosing a nearby timestamp.
- A namespace registry or centralized clock service.
