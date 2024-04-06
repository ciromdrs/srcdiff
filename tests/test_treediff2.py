"""Tests for the treediff2 script."""

import unittest
from src.srcdiff import EMPTY
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
            Tree('d', children=[
                Tree('c', children=[
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

    def test_create_temp_edit_table(self):
        """Tests if the temporary table to compute the edit distance between the subtrees rooted at `ikra` and `ikrb` is created correctly."""
        td = TreeDiff2(self.example_tree_a, self.example_tree_b)
        # The tables below are expected temporary tables
        t2x2 = [[0, 1], [1, -1]]
        t3x2 = [[0, 1], [1, -1], [2, -1]]
        t3x7 = [
            [0,  1,  2,  3,  4,  5,  6],
            [1, -1, -1, -1, -1, -1, -1],
            [2, -1, -1, -1, -1, -1, -1]
        ]
        t2x7 = [[0, 1, 2, 3, 4, 5, 6], [1, -1, -1, -1, -1, -1, -1]]
        t7x2 = [[0, 1], [1, -1], [2, -1], [3, -1], [4, -1], [5, -1], [6, -1]]
        t7x7 = [
            [0,  1,  2,  3,  4,  5,  6],
            [1, -1, -1, -1, -1, -1, -1],
            [2, -1, -1, -1, -1, -1, -1],
            [3, -1, -1, -1, -1, -1, -1],
            [4, -1, -1, -1, -1, -1, -1],
            [5, -1, -1, -1, -1, -1, -1],
            [6, -1, -1, -1, -1, -1, -1]
        ]
        # Keyroots of A are 3, 5, 6
        # Keyroots of B are 2, 5, 6
        # The tests explore all the possibilities (cartesian product)
        test_data = [
            [3, 2, t3x2],
            [3, 5, t3x2],
            [3, 6, t3x7],
            [5, 2, t2x2],
            [5, 5, t2x2],
            [5, 6, t2x7],
            [6, 2, t7x2],
            [6, 5, t7x2],
            [6, 6, t7x7],
        ]

        for ikra, ikrb, expected in test_data:
            with self.subTest(f'Keyroots: A={ikra}, B={ikrb}'):
                temp = td._create_temp_edit_table(ikra, ikrb)
                self.assertEqual(temp, expected)

    def test_is_tree_comparison(self):
        """Tests the is_tree_comparison  method."""
        td = TreeDiff2(self.example_tree_a, self.example_tree_b)
        test_data = [
            ['Nodes', 1, 1, 1, 1, True],
            ['Node and subtree', 2, 2, 1, 3, True],
            ['Subtrees', 2, 3, 1, 4, True],
            ['Subtree and tree', 2, 3, 1, 6, True],
            ['Trees', 1, 6, 1, 6, True],
            ['Node and subtrees', 1, 1, 1, 5, False],
            ['Subtrees', 1, 5, 1, 5, False],
            ['Subtrees and tree', 1, 5, 1, 6, False],
        ]
        for desc, ia0, ia1, ib0, ib1, expected in test_data:
            with self.subTest(f'{desc} ({expected})'):
                res = td.is_tree_comparison(ia0, ia1, ib0, ib1)
                self.assertEqual(res, expected)
