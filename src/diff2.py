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

        self._compute_distance_matrix()

        return self.matrix[self.n][self.m]

    def _build_diffs(self) -> tuple[list[str], list[str]]:
        diffa: list[str] = []
        diffb: list[str] = []
        # Indices i and j. This allows us to pass these as arguments by reference.
        ij = [self.n, self.m]
        i, j = ij
        while i > 0 and j > 0:
            # If the characters are equal
            if self._get_row_char_at(i) == self._get_col_char_at(j):
                self._shift(ij, diffa, diffb)
            else:
                # Characters differ, try to push b first
                if self.matrix[i][j-1] > self.matrix[i-1][j]:
                    self._push_b(ij, diffa, diffb)
                else:
                    self._push_a(ij, diffa, diffb)
            # Variables i and j must be updated at the end of every iteration
            i, j = ij
        # Copy the remainder of a or b
        while i > 0:
            self._push_b(ij, diffa, diffb)
            i, j = ij
        while j > 0:
            self._push_a(ij, diffa, diffb)
            i, j = ij

        return diffa, diffb

    def _push_a(self, ij: list[int], diffa: list[str], diffb: list[str]):
        """
        Copy from b and push a.
        """
        char = self._get_col_char_at(ij[1])
        diffa.insert(0, EMPTY)  # Push a
        diffb.insert(0, char)  # Copy from b
        ij[1] -= 1  # Decrement j

    def _push_b(self, ij: list[int], diffa: list[str], diffb: list[str]):
        """
        Copy from a and push b.
        """
        char = self._get_row_char_at(ij[0])
        diffa.insert(0, char)  # Copy from a
        diffb.insert(0, EMPTY)  # Push b
        ij[0] -= 1  # Decrement i

    def _shift(self, ij: list[int], diffa: list[str], diffb: list[str]):
        """
        Copy the next common character of the sequences and increment both indices.
        """
        # Copy the common character
        char = self._get_row_char_at(ij[0])
        diffa.insert(0, char)
        diffb.insert(0, char)
        # Decrement i and j
        ij[0] -= 1
        ij[1] -= 1

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

    def _compute_base_distances(self):
        """
        Compute the base distances of the matrix.
        """
        for k in range(self.n + 1):
            self.matrix[k][0] = k
        for k in range(self.m + 1):
            self.matrix[0][k] = k

    def _compute_distance_matrix(self):
        """
        Compute the distance matrix.
        """
        # First, compute the base distances
        self._compute_base_distances()
        # Then, compute the remainder using them
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


# FUNCTIONS

def diff2(a: str, b: str) -> Diff2:
    '''Performs a diff between strings `a`and `b`.'''
    result = Diff2(a, b)
    return result
