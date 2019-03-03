import logging
import cyclic as cy
from package import Package
from package_filter import PackageFilter
import time


class DepExpander:

    def __init__(self, repo):
        self.repo = repo
        self.p_filter = PackageFilter(repo)
        self.cycles = cy.calculate_cycles(repo)
        self.explored = {}
        self.history = []


    def explore(self, identifier):
        """Given a repo and identfier generate the set of dependency combinations."""

        deps  = self._explore_dep(identifier)
        combo = self._explore_conf(deps)

        return combo


    def _explore_dep(self, identifier):
        """Generate set of dependency combinations."""

        # Retrieve package and output
        output = [[identifier]]
        p = self.p_filter.get_package(identifier)

        # Check if identifier has previously been explored.
        if identifier in self.explored:
            return self.explored[identifier]

        # Check for cycles within the dep tree
        # if cyclic return empty route.
        self.history.append(identifier)
        if self._check_cyclic():
            return []

        # For each set of optional dependencies in package.
        for depset in p.depends:

            # For each optional dep in set of optional dependencies.
            temp = []
            for dep in depset:

                # Explore the existing dep.
                dep = self._explore_dep(dep)

                # If the existing dep resolves to None, continue loop.
                if dep == None:
                    continue

                # For each combination in given dependency.
                for combo in dep:

                    # For each existing combination in the output.
                    for row in output:
                        row = row[:]
                        row.extend(combo)
                        if self._check_cyclic_row(row) == False:
                            temp.append(row)

            output = temp

        # Add solution to explored dict and return output.
        self.explored[identifier] = output
        return output


    def _explore_conf(self, combinations):
        """Expand set of dependency combinations to include conflicts."""

        # For each combo in the list of dependency combinations.
        output = []
        for combo in combinations:

            # For each package in the combo.
            for p in combo:

                combo = combo[:]
                p = self.p_filter.get_package(p)
                for conf in p.conflicts:
                    combo.append("-{}".format(conf))

            output.append(combo)

        return output


    def _check_cyclic(self):
        """Checks if the current route being explored is cyclic."""

        for cycle in self.cycles:

            match = self.history[-len(cycle):]
            if match == cycle:
                return True

        return False


    def _check_cyclic_row(self, values):
        """Checks if the current route being explored is cyclic."""

        values = set(values)
        for cycle in self.cycles:

            cycle = set(cycle)
            if cycle <= values:
                return True

        return False


    def calculate_weight(self, state, identifier_list):
        """Takes a list of package insertions and deletions and
        calculates the total weight to perform the operation."""

        total_weight = 0
        uninstall_weight = 1000000

        for identifier in identifier_list:

            # Uninstall
            if '-' in identifier:
                package = self.p_filter.get_package(identifier[1:])
                if package.id in state:
                    total_weight += uninstall_weight

            # Install
            elif '-' not in identifier:
                package = self.p_filter.get_package(identifier)
                total_weight += package.size

        return total_weight