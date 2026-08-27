#!/usr/bin/env python3
"""Render one implemented robot/tool selection from the Genesis scene."""

from __future__ import annotations

import argparse
from pathlib import Path

import genesis as gs
import numpy as np
from PIL import Image
import torch

from dfl_genesis_integration.bridge import HOME, JOINTS, expanded_urdf


CAMERAS = {
    "picker1": ((2.8, -2.8, 2.2), (-0.1, 0.0, 1.05)),
    "picker2": ((3.1, -3.1, 2.7), (-0.1, 0.0, 1.3)),
    "h2515": ((2.3, -2.3, 1.8), (0.0, 0.0, 0.8)),
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("robot", choices=("picker1", "picker2", "h2515"))
    parser.add_argument("tool", choices=("vgc10_1cup", "vgc10_4cup", "vgp20", "2fg14"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--backend", choices=("auto", "cuda", "cpu"), default="auto")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.backend == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is unavailable")
    use_cuda = args.backend == "cuda" or (args.backend == "auto" and torch.cuda.is_available())
    gs.init(backend=gs.cuda if use_cuda else gs.cpu, precision="32", logging_level="warning")
    scene = gs.Scene(
        sim_options=gs.options.SimOptions(dt=0.005, substeps=2),
        rigid_options=gs.options.RigidOptions(enable_self_collision=False),
        show_viewer=False,
    )
    scene.add_entity(gs.morphs.Plane())
    model = "h2515" if args.robot == "h2515" else "m1013"
    entity = scene.add_entity(gs.morphs.URDF(
        file=str(expanded_urdf(args.robot, model, args.tool)),
        fixed=True,
        merge_fixed_links=False,
        convexify=True,
        decimate=True,
        decimate_face_num=500,
    ))
    position, lookat = CAMERAS[args.robot]
    camera = scene.add_camera(
        res=(1280, 960), pos=position, lookat=lookat, fov=38, GUI=False,
    )
    scene.build()
    indices = [entity.get_joint(name).dofs_idx_local[0] for name in JOINTS]
    entity.set_dofs_position(HOME, indices, zero_velocity=True)
    for _ in range(20):
        scene.step()
    rgb, _, _, _ = camera.render(
        rgb=True, depth=False, segmentation=False, normal=False, force_render=True,
    )
    pixels = np.asarray(rgb.detach().cpu() if hasattr(rgb, "detach") else rgb, dtype=np.uint8)
    output = args.output or Path(
        f"/workspace/logs/phase_00/genesis-{args.robot}-{args.tool}-preview.png"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(pixels[:, :, :3]).save(output)
    print(output)


if __name__ == "__main__":
    main()
