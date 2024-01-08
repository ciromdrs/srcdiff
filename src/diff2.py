'''Perform diffs of 2 source-code files.'''


from . import EMPTY


# CLASSES

class Diff2:
    def __init__(self, a: str, b: str):
        self._a = a
        self._b = b
        # Diff structure. It contains 2 rows, one for each string. Each string is
        # of size n + m for the case when `a` and `b` are competely different.
        self.diff = [[EMPTY] * (self.n + self.m)] * 2
        # Table for dynamic programming
        self.t = [[] * self.n] * self.m

    @property
    def n(self):
        """
        Returns the size of string `a`.
        """
        return len(self._a)

    @property
    def m(self):
        """
        Returns the size of string `b`.
        """
        return len(self._b)

    def _compute_base_row_and_column(self):
        """
        Compute the base row and column of `t`.
        """
        for k in range(self.n):
            self.t[k][0] = k
        for k in range(self.m):
            self.t[0][k] = k


# FUNCTIONS

def diff2(a: str, b: str) -> Diff2|None:
    '''Performs a diff between strings `a`and `b`.'''
    result = None
    return result
