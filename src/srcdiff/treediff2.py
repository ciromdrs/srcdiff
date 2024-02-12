'''Perform diffs on Trees.'''


from src.srcdiff import EMPTY
from src.srcdiff.tree import Tree


# CLASSES

class TreeDiff2:
    def __init__(self, a: Tree, b: Tree):
        self.a = a
        self.b = b

    def run(self) -> int: # TODO: return the Tree diffs
        self._initialize_treedist()
        # Compute keyroots
        keyrootsa = self.a.keyroots()
        keyrootsb = self.b.keyroots()
        # Compute tree distance between each pair of keyroots
        for kra in keyrootsa:
            for krb in keyrootsb:
                self._treedist(self.a.index_of[kra], self.b.index_of[krb])
        return self.table[len(self.a)][len(self.b)]

    def _treedist(self, ikra: int, ikrb: int):
        """Computes the tree edit distance between the subtrees rooted at `ikra` and `ikrb`.
        `ikra` and `ikrb` are the indices of the keyroots `a` and `b`, respectively."""
        assert self.table[ikra][ikrb] < 0, 'Should be unitialized.'
        temp = self._create_temp_edit_table(ikra, ikrb)
        self.table[ikra][ikrb] = ...
        return self.table[ikra][ikrb]
    
    def _create_temp_edit_table(self, ikra: int, ikrb: int) -> list[list[int]]:
        """Creates a temporary (n+1) x (m+1) tree edit distance table to compute the edit distance between the subtrees rooted at `ikra` and `ikrb`, where n and m are the number elements in the subtree rooted at keyroot a and keyroot b, respectively, and the +1 is for representing the empty trees.
        """
        n = len(self.a[ikra]) + 1
        m = len(self.b[ikrb]) + 1
        temp = [[i for i in range(m)]]
        for i in range(1, n):
            temp += [[i] + [-1] * (m-1)]
        return temp

# FUNCTIONS

def tree_diff2(a: Tree, b: Tree) -> int:
    '''Performs a diff between Trees `a`and `b`.'''
    result = TreeDiff2(a, b).run()
    return result
