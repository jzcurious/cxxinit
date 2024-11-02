from model import Project
from dirsmaker import DirsMaker
from cmakegen import CmakeGen
from pathlib import Path

if __name__ == "__main__":
    proj = Project("cxxinit.yml")
    DirsMaker.make(proj, True)
    CmakeGen.generate(proj)
