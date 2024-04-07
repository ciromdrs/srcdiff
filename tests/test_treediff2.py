"""Tests for the treediff2 script."""

import unittest
from src.srcdiff import EMPTY_SPACE
from src.srcdiff.tree import Tree
from src.srcdiff.treediff2 import TreeDiff2


class TestTreeDiff2(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.example_tree_a = Tree('f', children=[
            Tree('d', children=[
                Tree('a'),
                Tree('c', children=[
                    Tree('b'),
                ]),
            ]),
            Tree('e'),
        ])

        self.example_tree_b = Tree('f', children=[
            Tree('c', children=[
                Tree('d', children=[
                    Tree('a'),
                    Tree('b'),
                ]),
            ]),
            Tree('e'),
        ])

    def test_init(self):
        """Test if a TreeDiff2 object is instantiated correctly using the constructor."""
        a = Tree('a')
        b = Tree('b')
        td = TreeDiff2(a, b)

        self.assertEqual(td.a, a)
        self.assertEqual(td.b, b)

    def test_create_edit_distance_table(self):
        """Tests if the edit distance table is created correctly."""
        td = TreeDiff2(self.example_tree_a, self.example_tree_b)
        # The tables below are expected edit distance tables
        t1x1 = [[-1]]
        t1x2 = [[-1, -1]]
        t2x1 = [[-1],
                [-1]]
        t2x2 = [[-1, -1],
                [-1, -1]]
        # Data used in the subtests
        test_data = [
            [1, 1, t1x1],
            [1, 2, t1x2],
            [2, 1, t2x1],
            [2, 2, t2x2],
        ]
        for n, m, expected in test_data:
            with self.subTest(f'n={n}, m={m}'):
                created = td._create_edit_distance_table(n, m)
                self.assertEqual(created, expected)

    def test_create_keyroot_edit_distance_table(self):
        """Tests if the keyroot edit distance table is created correctly."""
        td = TreeDiff2(self.example_tree_a, self.example_tree_b)
        # The tables below are expected keyroot edit distance tables
        t1x1 = [[0,  1],
                [1, -1]]
        t1x2 = [[0,  1,  2],
                [1, -1, -1]]
        t2x1 = [[0,  1],
                [1, -1],
                [2, -1]]
        t2x2 = [[0,  1,  2],
                [1, -1, -1],
                [2, -1, -1]]
        test_data = [
            [1, 1, t1x1],
            [1, 2, t1x2],
            [2, 1, t2x1],
            [2, 2, t2x2],
        ]
        for ikra, ikrb, expected in test_data:
            with self.subTest(f'Keyroots: A={ikra}, B={ikrb}'):
                temp = td._create_keyroot_edit_distance_table(ikra, ikrb)
                self.assertEqual(temp, expected)

    def test_treedist(self):
        """Tests if the tree edit distance is computed correctly."""
        td = TreeDiff2(self.example_tree_a, self.example_tree_b)
        # The tables below are expected edit distance tables
        t3_2 = [[0, 1],
                [1, 0],
                [2, 1]]
        t3_5 = [[0, 1],
                [1, 1],
                [2, 2]]
        t3_6 = [[0, 1, 2, 3, 4, 5, 6],
                [1, 1, 1, 2, 3, 4, 5],
                [2, 2, 2, 2, 2, 3, 4]]
        t5_2 = [[0, 1],
                [1, 1]]
        t5_5 = [[0, 1],
                [1, 0]]
        t5_6 = [[0, 1, 2, 3, 4, 5, 6],
                [1, 1, 2, 3, 4, 4, 5]]
        t6_2 = [[0, 1],
                [1, 1],
                [2, 1],
                [3, 2],
                [4, 3],
                [5, 4],
                [6, 5]]
        t6_5 = [[0, 1],
                [1, 1],
                [2, 2],
                [3, 3],
                [4, 4],
                [5, 4],
                [6, 5]]
        ''' BUG: The resulting 6x6 forest distance table is different from the paper* where I got this algorithm from.
        In the paper, the 6x6 table is
        t6_6 = [[0, 1, 2, 3, 4, 5, 6],
                [1, 0, 1, 2, 3, 4, 5],
                [2, 1, 0, 1, 2, 3, 4],
                [3, 2, 1, 2, 3, 4, 5],
                [4, 3, 2, 1, 2, 3, 4],
                [5, 4, 3, 2, 3, 2, 3],
                [6, 5, 4, 3, 3, 3, 2]]
        (lines 3, 4, and 5 changed, starting at position [3,3]).
        Apparently that is because it is not allowed to replace node c by node d.
        Gotta find out why.

        * ZHANG, K. and SHASHA, D. Simple Fast Algorithms For the Editing Distance Between Trees and Related Problems. 1989. Available at: https://grantjenks.com/wiki/_media/ideas/simple_fast_algorithms_for_the_editing_distance_between_tree_and_related_problems.pdf
        '''
        t6_6 = [[0, 1, 2, 3, 4, 5, 6],
                [1, 0, 1, 2, 3, 4, 5],
                [2, 1, 0, 1, 2, 3, 4],
                [3, 2, 1, 1, 1, 2, 3],
                [4, 3, 2, 1, 2, 2, 3],
                [5, 4, 3, 2, 2, 2, 3],
                [6, 5, 4, 3, 3, 3, 2]]
        # Keyroots of A are 3, 5, 6
        # Keyroots of B are 2, 5, 6
        # The tests explore all the possibilities (cartesian product)
        test_data = [
            [3, 2, t3_2],
            [3, 5, t3_5],
            [3, 6, t3_6],
            [5, 2, t5_2],
            [5, 5, t5_5],
            [5, 6, t5_6],
            [6, 2, t6_2],
            [6, 5, t6_5],
            [6, 6, t6_6],
        ]
        for ikra, ikrb, expected in test_data:
            with self.subTest(f'Keyroots A={ikra}, B={ikrb}'):
                kra = td.a[ikra]
                krb = td.b[ikrb]
                computed = td._treedist(kra, krb)
                self.assertEqual(computed, expected)

    def test_is_tree_comparison(self):
        """Tests the is_tree_comparison method."""
        td = TreeDiff2(self.example_tree_a, self.example_tree_b)
        test_data = [
            ['Nodes', 1, 1, 1, 1, True],
            ['Node and subtree', 2, 2, 1, 3, True],
            ['Subtree and node', 1, 4, 2, 2, True],
            ['Subtrees', 2, 3, 1, 4, True],
            ['Subtree and tree', 2, 3, 1, 6, True],
            ['Tree and subtree', 1, 6, 1, 3, True],
            ['Trees', 1, 6, 1, 6, True],
            ['Node and subtrees', 1, 1, 1, 5, False],
            ['Subtrees and node', 1, 5, 1, 1, False],
            ['Subtrees', 1, 5, 1, 5, False],
            ['Subtrees and tree', 1, 5, 1, 6, False],
            ['Tree and subtrees', 1, 6, 1, 5, False],
        ]
        for desc, ia0, ia1, ib0, ib1, expected in test_data:
            with self.subTest(f'{desc} (a[{ia0}..{ia1}], b[{ib0}..{ib1}]. {expected})'):
                res = td._is_tree_comparison(ia0, ia1, ib0, ib1)
                self.assertEqual(res, expected)
