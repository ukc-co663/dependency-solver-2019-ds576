import networkx as nx
from package_filter import PackageFilter
import logging
import sys


def calculate_cycles(repo):
    """Returns the list of cyclic dependencies within the given repo."""

    p_filter = PackageFilter(repo)
    graph = nx.DiGraph()

    # Iterate over packages in repo
    # to generate the directed graph.
    for package_name in repo:
        for package_ver in repo[package_name]:

            package = repo[package_name][package_ver]
            graph.add_node(package.id)

            # Iterate over set of dependencies.
            for dependency_set in package.depends:

                # Iterate over ambiguous package identifiers.
                for target in dependency_set:

                    # Iterate over concrete package identifiers.
                    dep_packages = p_filter.get_identifiers(target)
                    for dep in dep_packages:
                        graph.add_edge(package.id, dep)

    # Find the cycles within the graph.
    # Generate the permutations of cycles.
    try:
        cycles_gen = nx.simple_cycles(graph)
        cycles = []
        for cycle in cycles_gen:
            cycles.extend(cyclic_orders(cycle))

    except nx.NetworkXNoCycle as _e:
        cycles = []

    return cycles


def cyclic_orders(cycle):
    """Calculates and returns all permutations of a cylic depedency."""

    output = []
    for i in range(0, len(cycle)):
        temp = []
        for j in range(0, len(cycle)):
            temp.append(cycle[(i + j) % len(cycle)])
        output.append(temp)

    return output


def is_cyclic(cycles, history):
    """Returns whether the set of explored dependencies includes a cyclic set."""

    history = (''.join(map(str, history)))[::-1]
    for cycle in cycles:

        if history.startswith(cycle):
            return True

    return False