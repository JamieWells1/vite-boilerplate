from setuptools import setup

# cli setup
setup(
    name="forge",
    version="0.1.0",
    packages=["forge"],
    entry_points={
        "console_scripts": [
            "forge=forge.cli:main",
        ],
    },
)
