class Structure:
    def __init__(self, root_path, *subdirs_paths):
        self.__paths = [root_path]

        for p in subdirs_paths:
            self.__paths.append(p.joinpath("src"))
            self.__paths.append(p.joinpath("include"))

    @property
    def paths(self):
        self.__paths

    def apply(self, force=False):
        from os import listdir
        from shutil import rmtree

        if force:
            root = self.__paths[0]

            for item in listdir(root):
                if item == "cxxinit.yml":
                    continue

                path = root.joinpath(item)

                if path.is_file():
                    path.unlink()
                    continue

                if path.is_dir():
                    rmtree(path)

        for p in self.__paths:
            p.mkdir(parents=True, exist_ok=True)
