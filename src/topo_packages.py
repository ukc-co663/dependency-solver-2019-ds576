from toposort import toposort, toposort_flatten
from package_filter import PackageFilter
from util import list_flatten


class TopoSorter:

    def __init__(self, repo, state):
        self.repo = repo
        self.state = state
        self.p_filter = PackageFilter(repo)


    def sort(self, solution):
        """"""

        install = [p for p in solution if '-' not in p]
        uninstall = [p for p in solution if '-' in p]
        f_solution = self._format(solution)
        output = list(toposort_flatten(f_solution))

        non_dependent = []
        for p in install:
            p = "+{}".format(p)
            if p not in output:
                non_dependent.append("+{}".format(p))
                output.insert(0, p)

        # print(uninstall)
        for p in uninstall:
            if p not in output and p[1:] in self.state:
                output.insert(0, p)

        return output


    def _format(self, solution):
        """"""

        install = [p for p in solution if '-' not in p]
        _uninstall = [p[1:] for p in solution if '-' in p]
        output = {}

        # Calculate install topo constraints.
        for identifier in install:
            p = self.p_filter.get_package(identifier)
            potential_deps = list_flatten(p.depends)
            potential_conf = list_flatten(p.conflicts)

            depends = set()
            for dep in potential_deps:
                if dep in install:
                    depends.add("+{}".format(dep))

            conflicts = set()
            for conf in potential_conf:
                if conf in self.state:
                    conflicts.add("-{}".format(conf))

            constraints = depends.union(conflicts)
            if len(constraints) > 0:
                output["+{}".format(identifier)] = constraints

        return output


