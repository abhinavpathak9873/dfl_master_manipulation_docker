# Phase 00 host inventory

Recorded: 2026-08-27, Asia/Dubai

| Item | Observed value |
|---|---|
| Host OS | Ubuntu 26.04 (Resolute), kernel `7.0.0-29-generic` |
| Container target | Ubuntu 24.04, ROS 2 Jazzy |
| CPU | 12 logical CPUs |
| RAM | 123 GiB |
| Workspace filesystem | 937 GiB total, 220 GiB free at inspection |
| Docker | Engine/client 29.5.3, Compose 5.1.4 |
| GPU 0 | NVIDIA RTX PRO 4500 Blackwell, 32623 MiB |
| GPU 1 | NVIDIA RTX A4000, 16376 MiB |
| NVIDIA driver | 595.84 |
| GPU container smoke | Both GPUs visible from pinned CUDA 12.8 Ubuntu 24.04 image |
| ROS on host | Not installed; all ROS work is container-owned |
| Display | X11 variables are forwarded when present; headless is the default |

Unknown Phase 00 hardware facts remain explicit gates: NUC/Jetson model and OS,
Doosan controller firmware/generation, installed tool mapping, robot endpoints,
and final D455 serial/mount. No real-mode support claim is made from this file.
