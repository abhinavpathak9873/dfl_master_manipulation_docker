from glob import glob
from pathlib import Path
from setuptools import find_packages, setup

package_name = "dfl_manipulation_toolbox"


def asset_files(root: str):
    return [
        ("share/" + package_name + "/" + str(path.parent), [str(path)])
        for path in Path(root).glob("**/*")
        if path.is_file()
    ]

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/config", glob("config/*.yaml")),
        ("share/" + package_name + "/launch", glob("launch/*.launch.py")),
        ("share/" + package_name + "/urdf", glob("urdf/*.xacro")),
        ("share/" + package_name + "/scenes/empty", glob("scenes/empty/*")),
        ("share/" + package_name + "/scenes/gallery", glob("scenes/gallery/*")),
    ] + asset_files("meshes"),
    install_requires=["setuptools", "PyYAML"],
    zip_safe=True,
    maintainer="DFL Robotics",
    maintainer_email="robotics@dfl.ae",
    description="Phase 00 profiles and simulator glue",
    license="Apache-2.0",
    entry_points={
        "console_scripts": [
            "dfl-profile = dfl_manipulation_toolbox.cli:main",
            "dfl-sim-io = dfl_manipulation_toolbox.sim_io:main",
            "dfl-trajectory-adapter = dfl_manipulation_toolbox.trajectory_adapter:main",
        ]
    },
)
