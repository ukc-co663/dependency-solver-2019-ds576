import sys
import itertools
from package_filter import PackageFilter
from util import list_flatten
from package import Package


def generate_repo(repo_json):
    """Takes a JSON repository description and generates
    a dictionary of corresponding Package objects.

    The repo is a dictionary organised via package name, version."""

    # Create repository of package objects.
    repo = {}
    for package in repo_json:

        name        = package.get("name", "")
        version     = package.get("version", "")
        size        = package.get("size", "")
        depends     = package.get("depends", [])
        conflicts   = package.get("conflicts", [])

        # Required fields for a package, if missing invalid repository.
        if name == "" or version == "" or size == "":
            print("Exiting, invalid repo description.")
            sys.exit(1)

        # Create Package object for the current package and add to the repo.
        p = Package(name = name, version = version, size = size, depends = depends, conflicts = conflicts)
        if not name in repo:
            repo[name] = {}
            repo[name][version] = p
        else:
            repo[name][version] = p

    return _expand_constraints(repo)


def _expand_constraints(repo):
    """Takes a repo and expands the set of constraints to concrete versions
    instead of set identifiers."""

    p_filter = PackageFilter(repo)

    # Iterate over packages expanding ambigious dependencies and conflicts
    # to concrete lists.
    for package_name in repo:
        for package_version in repo[package_name]:
            package = repo[package_name][package_version]

            expanded_deps = []
            for dep in package.depends:
                if isinstance(dep, list):
                    temp = []
                    for item in dep:
                        temp.append(p_filter.get_identifiers(item))
                        temp = list_flatten(temp)
                    expanded_deps.append(temp)
                else:
                    expanded_dep = p_filter.get_identifiers(dep)
                    expanded_deps.append(expanded_dep)

            expanded_confs = []
            for conf in package.conflicts:
                expanded_conf = p_filter.get_identifiers(conf)
                expanded_confs.extend(expanded_conf)

            package.depends = expanded_deps
            package.conflicts = expanded_confs

    return repo


def generate_state(repo, state_json):
    """Takes a JSON state description and Package repo and generates
    a corresponding list of Package from the repository."""

    # Create a current state list of package objects.
    state = []
    for package in state_json:
        name, version = package.split('=')
        state.append(package)

    return state


def generate_actions(repo, state, constraint_json):
    """Takes a JSON constraint description and Package repo and generates
    two corresponding lists of Package constraints, one positive and one negative."""

    p_filter = PackageFilter(repo)

    install = []
    uninstall = []
    for package in constraint_json:

        # Get the unambigious list of packages.
        constraint_type = package[:1]
        identifier = package[1:]
        packages = p_filter.get_identifiers(identifier)

        # Sort packages into install and uninstall.
        if constraint_type == '-':
            uninstall.append(packages)
        elif constraint_type == '+':
            name, _ = packages[0].split('=')
            add = True
            for p in packages:
                if p in state:
                    add = False
            if add:
                install.append(packages)

    return install, uninstall