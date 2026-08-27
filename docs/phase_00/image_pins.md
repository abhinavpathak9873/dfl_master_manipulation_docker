# Phase 00 image and source pins

| Purpose | Immutable input |
|---|---|
| Ubuntu base | `ubuntu@sha256:4fbb8e6a8395de5a7550b33509421a2bafbc0aab6c06ba2cef9ebffbc7092d90` |
| CUDA/Genesis base | `nvcr.io/nvidia/cuda@sha256:e778509d37d66475120929671500377524f7278478ba08131b07ef3ffcc0dce0` |
| Doosan emulator | `doosanrobot/dsr_emulator@sha256:878b8557dfa2ffd843674e42576fd015b803cc805fe698156eb7b743e71547e9` |
| ROS apt source package | `ros2-apt-source` 1.1.0, SHA-256 `35441f3092fd05773a3c397fab38661bec466584c7a1f1c05366579997cb5fe7` |
| Doosan source | `816ecb5d1c2599303eaf9540216afa03552f80ad` |
| Genesis source | tag `v1.3.3`, commit `76f8f5b3457e7c6d6a078de2244066f9a8694c45` |
| Genesis Python environment | `config/genesis-requirements.lock` |
| PyTorch | `2.11.0+cu128` |

Dockerfiles use digests for base images and constrain every tested Genesis
Python dependency to the recorded version. Build scripts fail on a floating
source checkout or mismatched resolved revision.
