from package import Package
import logging


class PackageFilter:

    def __init__(self, repo):
        self.repo = repo


    def get_packages(self, identifier):
        """Returns a list of the packages in which match the identifier."""

        # Identify the type of operation.
        if "<=" in identifier:
            op = '<='
        elif ">=" in identifier:
            op = '>='
        elif "<" in identifier:
            op = '<'
        elif ">" in identifier:
            op = '>'
        elif "=" in identifier:
            op = '='
        else:
            op = None

        # Split the package into name and version.
        if op == None:
            name = identifier
            version = None
        else:
            name, version = identifier.split(op)

        if isinstance(name, list):
            name = name[0]

        # Iterate over repo building return package list.
        packages = []
        if name in self.repo:
            for _, package in self.repo[name].items():
                if package.within_range(op, version):
                    packages.append(package)

        return packages


    def get_package(self, identifier):
        """Returns a singular unambigious package object for the given identifier."""

        package = self.get_packages(identifier)[0]
        return package


    def get_identifiers(self, identifier):
        """Returns a list of unambiguous package identifiers in which match
        the identifier."""

        package_ids = [package.id for package in self.get_packages(identifier)]
        return package_ids