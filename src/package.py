class Package:
    """
    Data structure for repo packages.

    Attributes:
        name        (str): The name of the package.
        version     (str): Version number of the package.
        size        (int): Size of the package.
        depends     (list): List of dependent package identifiers (conjunct of disjuncts).
        conflicts   (list): List of conflicting package identifers (conjuncts).
        id          (str): The ID of the package.
    """

    def __init__(self, name, version, size, depends, conflicts):
        self.name = name
        self.version = version
        self.size = size
        self.depends = depends
        self.conflicts = conflicts
        self.id = "{}={}".format(name, version)


    def __str__(self):
        return self.__repr__()


    def __repr__(self):
        res = "Package(name={}, version={}, size={}, depends={}, conflicts={})".format(
            self.name,
            self.version,
            self.size,
            self.depends,
            self.conflicts
        )
        return res


    def within_range(self, op, version_id):
        """Given a version identifier and comparison operation returns True if own version
        is within the given range otherwise False."""

        if op == None or version_id == None:
            return True

        elif op == "<=":
            if self.compare_version(version_id) in [0, -1]:
                return True

        elif op == ">=":
            if self.compare_version(version_id) in [1, 0]:
                return True

        elif op == "<":
            if self.compare_version(version_id) == -1:
                return True

        elif op == ">":
            if self.compare_version(version_id) == 1:
                return True

        elif op == "=":
            if self.compare_version(version_id) == 0:
                return True

        return False


    def compare_version(self, comparison):
        """Compares own version against paramater provided.
        If own version is greater returns '1', if versions are the same '0' and '-1' if lower."""

        # Split the two versions into integer lists
        # of equal length.
        v = [int(item) for item in self.version.split('.')]
        c = [int(item) for item in comparison.split('.')]
        length = len(v) if len(v) > len(c) else len(c)
        v = (v + length * [0])[:length]
        c = (c + length * [0])[:length]

        # Iterate over lists comparing values.
        for i in range(length):
            if v[i] == c[i]:
                continue
            elif v[i] < c[i]:
                return -1
            elif v[i] > c[i]:
                return 1

        return 0