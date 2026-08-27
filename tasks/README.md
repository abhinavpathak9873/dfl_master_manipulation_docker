# Tasks

Task files are ordinary Python entry points. Phase 00 provides one fixed task:

```bash
python3 /workspace/tasks/phase0_fixed_task.py \
  --robot picker1 --tool vgc10_1cup --mode gazebo
```

The task checks readiness, joint state, home and probe motion, tool command
acknowledgement, cancellation/hold, and—on Picker robots—camera and base state.
It refuses `--mode real` unless the current shell was deliberately armed by
`scripts/real_mode_guard.sh` after fresh operator authorization.
