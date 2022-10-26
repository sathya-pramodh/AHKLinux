from setuptools import setup


def get_long_description():
    with open("README.md", "r") as file:
        long_description = file.read()
        return long_description


setup(
    name="AHKLinux",
    version="v0.0.1-backport-3.10",
    author="sathya-pramodh",
    author_email="sathyapramodh17@gmail.com",
    description="An AHK interpreter for Linux.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/sathya-pramodh/AHKLinux",
    project_urls={
        "Bug Tracker": "https://github.com/sathya-pramodh/AHKLinux/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.10",
    install_requires=["tk", "pillow", "typing_extensions", "typing"],
    entry_points={
        "console_scripts": [
            "ahk = AHKLinux.init:start",
        ]
    },
)
