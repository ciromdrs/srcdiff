'''Perform diffs on Trees.'''


from src.srcdiff import EMPTY_SPACE
from src.srcdiff.tree import Tree


# CLASSES

class TreeDiff2:
    def __init__(self, a: Tree, b: Tree):
        self.a = a
        self.b = b
        self.table: list[list[int]] = self._create_edit_distance_table(
            len(self.a), len(self.b))

    def run(self) -> int:  # TODO: return the Tree diffs
        """Runs the tree diff algorithm."""
        self.table = self._create_edit_distance_table(
            len(self.a), len(self.b))
        # Compute keyroots
        keyrootsa = self.a.keyroots()
        keyrootsb = self.b.keyroots()
        # Compute tree distance between each pair of keyroots
        for kra in keyrootsa:
            for krb in keyrootsb:
                self._treedist(kra, krb)
        return self.table[len(self.a)][len(self.b)]

    def _treedist(self, kra: Tree, krb: Tree) -> list[list[int]]:
        """Computes the tree edit distance between the subtrees rooted at `kra` and `krb` and updates the global edit distance table.
        `kra` and `krb` are the keyroots `a` and `b`, respectively."""
        # Get the size of the subtrees
        n = len(kra)
        m = len(krb)
        # Indices of keyroots `a` and `b`, respectively
        ikra = self.a.index_of[kra]
        ikrb = self.b.index_of[krb]
        # Indices of leftmost leaves of keyroots `a` and `b`, respectively
        ilkra = self.a.index_of[kra.leftmost_leaf()]
        ilkrb = self.b.index_of[krb.leftmost_leaf()]
        # Create the keyroot edit distance table
        keyroot_distance_table = self._create_keyroot_edit_distance_table(n, m)
        # Compute the distance between the two subtrees at `kra` and `krb` locally
        for local_i in range(1, n+1):
            for local_j in range(1, m+1):
                # Convert "local" indices from nodes in subtree `kra` to "global" indices in tree `a` (analogous for `b` and `krb`)
                global_i = self.a.index_of[kra[local_i]]
                global_j = self.b.index_of[krb[local_j]]
                # Check if it is a tree or a forest comparison
                if self._is_tree_comparison(ilkra, ikra, ilkrb, ikrb):
                    self._do_tree_diff(kra, krb, local_i, local_j,
                                       global_i, global_j,
                                       keyroot_distance_table)
                else:
                    self._do_forest_diff(local_i, local_j,
                                       global_i, global_j,
                                       keyroot_distance_table)
        return keyroot_distance_table

    def _do_tree_diff(self, kra: Tree, krb: Tree, local_i: int, local_j: int,
                      global_i: int, global_j: int,
                      keyroot_distance_table: list[list[int]]):
        '''Performs a tree diff operation, which includes:
        1- Applying the cheapest operation to the diff trees.
        2- Updating the keyroot edit distance table with the cost of the chosen operation.
        3- Updating the global edit distance table with the new cost.
        Parameters (analogous for `b`):
        - `kra` is the keyroot from tree `a`.
        - `local_i` is the local index `i` in `kra`.
        - `global_i` is the global index `i` in tree `a`.
        - `keyroot_distance_table` is the keyroot edit distance table.
        '''
        # Check if the nodes are equal to get the edit cost
        equal, _, _ = kra[local_i].equals(
            krb[local_j], compare_children=False)
        # Replace cost
        rc = int(not equal)  # Equal nodes cost 0, different nodes cost 1
        # Tree comparison
        keyroot_distance_table[local_i][local_j] = min(
            keyroot_distance_table[local_i-1][local_j-1] + rc,  # Replace
            keyroot_distance_table[local_i][local_j-1] + 1,     # Insert
            keyroot_distance_table[local_i-1][local_j] + 1,     # Remove
        )
        # Copy tree distances to permanent table
        self.table[global_i-1][global_j-1] = keyroot_distance_table[local_i][local_j]

    def _do_forest_diff(self, local_i: int, local_j: int,
                      global_i: int, global_j: int,
                      keyroot_distance_table: list[list[int]]):
        '''Performs a forest diff operation, which includes:
        1- Applying the cheapest operation to the diff trees.
        2- Updating the keyroot edit distance table with the cost of the chosen operation.
        Parameters (analogous for `b`):
        - `local_i` is the local index `i` in `kra`.
        - `global_i` is the global index `i` in tree `a`.
        - `keyroot_distance_table` is the keyroot edit distance table.
        '''
        keyroot_distance_table[local_i][local_j] = min(
            keyroot_distance_table[local_i-1][local_j-1] + \
                self.table[global_i-1][global_j-1],          # Replace
            keyroot_distance_table[local_i][local_j-1] + 1,  # Insert
            keyroot_distance_table[local_i-1][local_j] + 1,  # Remove
        )

    def _is_tree_comparison(self, ia0: int, ia1: int, ib0: int, ib1: int) -> bool:
        '''Returns True if both node ranges are trees or False, otherwise.
        `ia0` and `ia1` are the first and last node indices in tree `a` (analogous for `b`).
        '''
        a_is_tree = len(self.a.forest(ia0, ia1)) == 1
        b_is_tree = len(self.b.forest(ib0, ib1)) == 1
        return a_is_tree and b_is_tree

    def _create_edit_distance_table(self, n: int, m: int) -> list[list[int]]:
        """Creates an `n*m` tree edit distance table, where `n` and `m` are the number elements in tree `a` and `b`, respectively.
        """
        table = []  # TODO: Create a dict instead
        for i in range(n):
            aux = []
            for _ in range(m):
                aux += [-1]
            table += [aux]
        return table

    def _create_keyroot_edit_distance_table(self, n: int, m: int) -> list[list[int]]:
        """Creates an `(n+1)*(m+1)` keyroot edit distance table, where `n` and `m` are the number elements in the subtrees rooted at keyroots `a` and `b`, respectively.
        """
        # The +1's are for representing empty trees
        temp = self._create_edit_distance_table(n+1, m+1)
        # Initialize the table
        for j in range(m+1):
            temp[0][j] = j  # First row is [0, 1, 2, ...]
        for i in range(1, n+1):
            temp[i][0] = i  # First column is [[0, ...], [1, ...], [2, ...], ...]
            for j in range(1, m+1):
                temp[i][j] = -1  # The remaining elements are -1
        return temp
        


# FUNCTIONS

def tree_diff2(a: Tree, b: Tree) -> int:
    '''Performs a diff between Trees `a`and `b`.'''
    result = TreeDiff2(a, b).run()
    return result
