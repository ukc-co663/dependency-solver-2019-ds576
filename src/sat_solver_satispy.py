from satispy import Variable, Cnf
from satispy.solver import Minisat
import logging


class SATSolver:
    """
    Wrapper class for 'Satispy' library.
    """

    def __init__(self):
        self.solver = Minisat()


    def solve(self, expr):
        """Takes a list of dependent and conflicting packages
        and returns whether the current configuration is satisfiable."""

        dependent   = [p for p in expr if '-' not in p]
        conflicting = [p[1:] for p in expr if '-' in p]

        # Generate set of unique package variables.
        variables = {}
        for var in set(dependent + conflicting):
            variables[var] = Variable(var)

        # Generate 'CNF' logical expression from dependencies
        # and conflicts.
        expr = Cnf()

        for con in dependent:
            v = variables[con]
            expr = expr & v

        for con in conflicting:
            v = variables[con]
            expr = expr & -v

        # Calculate the satisfiability of the input variables.
        valid, param = self._check_satisfiability(variables, expr)

        if valid:
            logging.debug("Logical expression, {}, is satisfiable with parameters, {}.".format(expr, param))
        else:
            logging.debug("Logical expression, {} , is unsatisfiable.".format(expr))

        return valid, param


    def _check_satisfiability(self, variables, logic_expr):
        """Given a 'CNF' logical expression returns a boolean stating if valid and
        the configuration of variables achieving this."""

        # Case expression is empty.
        if str(logic_expr) == '()':
            logging.debug("Logical expression, {}, is empty and therefore satisfiable.".format(logic_expr))
            return True, None

        solution = self.solver.solve(logic_expr)

        # No satisifiable path.
        if not solution.success:
            return False, None

        # Build satisfiable solution output.
        param = []
        for k, v in variables.items():

            if solution[v] == True:
                param.append(k)
            else:
                param.append('-{}'.format(k))

        return True, param