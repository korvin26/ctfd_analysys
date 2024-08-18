from setuptools import setup, find_packages

setup(
    name="ctfd_analysis",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pydot",
        "argparse"
    ],
    entry_points={
        "console_scripts": [
            "ctfd_analysis = ctfd_analysis.main:main"
        ]
    },
)
