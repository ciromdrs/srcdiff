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
        # Table for dynamic programming. The +1's are for the empty string.
        self.t = []
        for _ in range(self.n + 1):
            self.t.append([-1] * (self.m + 1))

    def run(self):
        """
        Run the diff.
        Returns the edit distance.
        """
        self._initialize()
        self._compute_base_row_and_column()

        self.diffb = list(self._b) + ([EMPTY] * self.n)

        return self.distance

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
        for k in range(self.n + 1):
            self.t[k][0] = k
        for k in range(self.m + 1):
            self.t[0][k] = k


# FUNCTIONS

def diff2(a: str, b: str) -> Diff2:
    '''Performs a diff between strings `a`and `b`.'''
    result = Diff2(a, b)
    return result
