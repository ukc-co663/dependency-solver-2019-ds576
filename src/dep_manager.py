import json
import sys
import logging
import itertools
import time
import logger
import parse_input as pi
import cyclic as cy
from package_filter import PackageFilter
from dep_expander import DepExpander
from package import Package
from sat_solver_satispy import SATSolver
from topo_packages import TopoSorter
from util import list_flatten
sys.setrecursionlimit(60000)


def main():
    """
    Given the location of the input data, loads the description
    of the repo, the current state and the set of constraints
    in which need to be solved.
    """

    # Path to input directory provided.
    if len(sys.argv) == 2:
        path = sys.argv[1]
        repo_path = path + "repository.json"
        state_path = path + "initial.json"
        const_path = path + "constraints.json"

    # Path to all input files provided.
    elif len(sys.argv) == 4:
        repo_path = sys.argv[1]
        state_path = sys.argv[2]
        const_path = sys.argv[3]

    # Error regarding input variables.
    else:
        print("Exiting, path to input data not provided.")
        sys.exit(1)

    # Load input JSON files.
    try:
        path  = sys.argv[1]
        with open(repo_path, 'r') as f:
            repo_json = json.load(f)

        with open(state_path, 'r') as f:
            state_json = json.load(f)

        with open(const_path, 'r') as f:
            const_json = json.load(f)

    except:
        print("Exiting, failed to load or parse the JSON input files.")
        sys.exit(1)

    # Parse JSON in internal representation.
    repo = pi.generate_repo(repo_json)
    state = pi.generate_state(repo, state_json)
    install, uninstall = pi.generate_actions(repo, state, const_json)
    cycles = cy.calculate_cycles(repo)

    # Debug output.
    logging.debug("Repo: {}".format(repo))
    logging.debug("State: {}".format(state))
    logging.debug("Install constraints: {}".format(install))
    logging.debug("Uninstall constraint: {}".format(uninstall))

    calculate_output(repo = repo, state = state, cycles = cycles, install = install, uninstall = uninstall)


def calculate_output(repo, state, cycles, install, uninstall):
    """
    Given a repo description, current state and set of constraints,
    calculate if a valid state T can be produced that meets that constraints.
    If possible output a list of commands that transform the current state
    into the new valid state.
    N.B. All intermediate states of the transformation must be valid.
    """

    solver = SATSolver()
    dep_expander = DepExpander(repo)
    sorter = TopoSorter(repo, state)

    # Generate required set of initial uninstalls.
    uninstall_requirement = []
    for package_set in uninstall:
        for identifier in package_set:
            uninstall_requirement.append("-{}".format(identifier))


    # For each set of installs generate the set of permutations.
    permutations = []
    permutations.append(uninstall_requirement)
    for install_opt in install:

        # For each installable package:
        temp = []
        for opt in install_opt:
            temp.extend(dep_expander.explore(opt))

        permutations = temp if len(permutations) == 0 else [list(set(list_flatten(list(perm)))) for perm in list(itertools.product(permutations, temp))]


    # Check permutations
    if permutations == [[]]:
        print([])
        return

    solutions = []
    for perm in permutations:
        valid, params = solver.solve(perm)
        if valid:
            weight = dep_expander.calculate_weight(state, params)
            output = sorter.sort(params)
            solutions.append((weight, output))

    if len(solutions) > 0:
        solutions.sort(key = lambda x:x[0])
        output_text = json.dumps(solutions[0][1])
        print(output_text)
    else:
        print([])



if __name__ == "__main__":
    main()