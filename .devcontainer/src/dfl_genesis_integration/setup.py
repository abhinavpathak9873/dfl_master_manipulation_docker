from glob import glob
from setuptools import find_packages, setup

package_name = "dfl_genesis_integration"
setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="DFL Robotics",
    maintainer_email="robotics@dfl.ae",
    description="Direct Genesis ROS bridge",
    license="Apache-2.0",
    entry_points={"console_scripts": ["dfl-genesis-bridge = dfl_genesis_integration.bridge:main"]},
)
