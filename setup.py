from setuptools import setup

setup(
    name="cxxinit",
    version="1.0.0",
    description="An utility for initializing a C++ project. Based on CMake.",
    url="https://github.com/jzcurious/cxxinit",
    author="void",
    author_email="paranoid.hpc.io@gmail.com",
    license="GNU GPLv3",
    packages=["cxxinit"],
    install_requires=[
        "Jinja2 >= 3.1.4",
        "MarkupSafe >= 3.0.2",
        "PyYAML >= 6.0.2",
        "setuptools >= 75.5.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)
