'''Perform diffs of 2 source-code files.'''


from . import EMPTY


# CLASSES

class Diff2:
    def __init__(self, a: str, b: str):
        self._a = a
        self._b = b

    def _initialize(self):
        """
        Initialize data structures to perform the diff.
        """
        # Diff results, one for each string
        # The size n + m is for the case when `a` and `b` are competely different
        self.diffa = [EMPTY] * (self.n + self.m)
        self.diffb = [EMPTY] * (self.n + self.m)
        # Table for dynamic programming
        self.t = [[-1] * self.m] * self.n

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

def diff2(a: str, b: str) -> Diff2:
    '''Performs a diff between strings `a`and `b`.'''
    result = Diff2(a, b)
    return result
