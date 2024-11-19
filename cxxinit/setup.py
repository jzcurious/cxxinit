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
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "cxxinit = cxxinit.cxxinit:main",
        ],
    },
    package_data={
        "cxxinit": [
            "assets/sample/*",
            "assets/templates/cmake/*",
            "assets/dist/",
            "assets/dist/.clang-format",
            "assets/dist/.gitignore",
        ],
    },
)
