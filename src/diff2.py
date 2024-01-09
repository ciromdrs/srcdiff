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
        # Matrix for dynamic programming. The +1's are for the empty string.
        self.matrix = []
        for _ in range(self.n + 1):
            self.matrix.append([-1] * (self.m + 1))

    def run(self):
        """
        Run the diff.
        Returns the edit distance.
        """
        self._initialize()
        self._compute_base_row_and_column()

        # Main loop
        # Fill `t` using row 0 and column 0
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                # If the characters are equal
                if self._get_row_char_at(i) == self._get_col_char_at(j):
                    # Copy the distance from the diagonal
                    self.matrix[i][j] = self.matrix[i-1][j-1]
                else:
                    # Characters differ, try to push b first
                    if self.matrix[i][j-1] <= self.matrix[i-1][j]:
                        self.matrix[i][j] = self.matrix[i][j-1] + 1
                    else:
                        self.matrix[i][j] = self.matrix[i-1][j] + 1

        return self.matrix[self.n][self.m]

    def _push_a(self, i: int, j: int):
        """
        TODO
        """
        raise NotImplemented()

    def _push_b(self, i: int, j: int):
        """
        TODO
        """
        raise NotImplemented()

    def _shift(self, i: int, j: int):
        """
        TODO
        """
        raise NotImplemented()

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

    def _get_row_char_at(self, i: int):
        """
        Get the char corresponding to index `i` of the row in the dynamic programming matrix.
        """
        # The -1 compensates the \0's added to the matrix
        return self._a[i-1]

    def _get_col_char_at(self, j: int):
        """
        Get the char corresponding to index `j` of the column in the dynamic programming matrix.
        """
        # The -1 compensates the \0's added to the matrix
        return self._b[j-1]

    def _compute_base_row_and_column(self):
        """
        Compute the base row and column of `t`.
        """
        for k in range(self.n + 1):
            self.matrix[k][0] = k
        for k in range(self.m + 1):
            self.matrix[0][k] = k


# FUNCTIONS

def diff2(a: str, b: str) -> Diff2:
    '''Performs a diff between strings `a`and `b`.'''
    result = Diff2(a, b)
    return result
