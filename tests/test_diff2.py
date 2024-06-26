"""Tests for the diff2 script."""

import unittest  # TODO: Switch to pytest
from src.srcdiff import EMPTY
from src.srcdiff.diff2 import Diff2


class TestDiff2(unittest.TestCase):
    def setUp(self):
        self.a = 'paper'
        self.b = 'poster'
        self.diff = Diff2(self.a, self.b)
        self.expected_matrix = [
            [0, 1, 2, 3, 4, 5, 6],
            [1, 0, 1, 2, 3, 4, 5],
            [2, 1, 2, 3, 4, 5, 6],
            [3, 2, 3, 4, 5, 6, 7],
            [4, 3, 4, 5, 6, 5, 6],
            [5, 4, 5, 6, 7, 6, 5],
        ]

    def test_init(self):
        """
        Test if a Diff2 object is instantiated correctly using the constructor.
        """
        # Assert the strings are equal
        self.assertEqual(self.diff._a, self.a)
        self.assertEqual(self.diff._b, self.b)

    def test_initialize(self):
        """
        Test if the data structures for the diff are initialized correctly.
        """
        self.diff._initialize()

        # The dynamic programming matrix starts empty and has size `(n+1) * (m+1)`
        self.assertEqual(
            self.diff.matrix,
            [[-1] * (self.diff.m + 1)] * (self.diff.n + 1))

    def test_n(self):
        """
        Test if propery `n` is equal to the length of string `a`.
        """
        self.assertEqual(len(self.a), self.diff.n)

    def test_m(self):
        """
        Test if propery `m` is equal to the length of string `b`.
        """
        self.assertEqual(len(self.b), self.diff.m)

    def test_compute_base_distances(self):
        """
        Test the computation of the base distances fo the dynamic programming matrix.
        """
        self.diff._initialize()

        self.diff._compute_base_distances()

        # The distances in the base row are 0, 1, 2, ... , m
        self.assertEqual(self.diff.matrix[0], list(range(self.diff.m + 1)))
        # The distances in the base column are 0, 1, 2, ... , n
        for i in range(self.diff.n + 1):
            self.assertEqual(
                i,
                self.diff.matrix[i][0],
                f'Expected matrix[{i}][0] to be {i}, got {self.diff.matrix[i][0]}.')

    def test_compute_distance_matrix(self):
        """
        Test the computation of the distance matrix.
        """
        self.diff._initialize()

        self.diff._compute_distance_matrix()

        self.assertEqual(self.expected_matrix, self.diff.matrix)

    def test_run(self):
        """
        Test if the minimum edit distance and the dynamic programming matrix are correct.
        """
        distance, _, _ = self.diff.run()

        self.assertEqual(5, distance)
        self.assertEqual(self.expected_matrix, self.diff.matrix)

    def test_get_row_char_at(self):
        """
        Test if it returns the correct character corresponding to index `i` of the row in the dynamic programming matrix.
        """
        self.assertEqual('p', self.diff._get_row_char_at(1))
        self.assertEqual('a', self.diff._get_row_char_at(2))
        self.assertEqual('p', self.diff._get_row_char_at(3))
        self.assertEqual('e', self.diff._get_row_char_at(4))
        self.assertEqual('r', self.diff._get_row_char_at(5))

    def test_get_col_char_at(self):
        """
        Test if it returns the correct character corresponding to index `j` of the column in the dynamic programming matrix.
        """
        self.assertEqual('p', self.diff._get_col_char_at(1))
        self.assertEqual('o', self.diff._get_col_char_at(2))
        self.assertEqual('s', self.diff._get_col_char_at(3))
        self.assertEqual('t', self.diff._get_col_char_at(4))
        self.assertEqual('e', self.diff._get_col_char_at(5))
        self.assertEqual('r', self.diff._get_col_char_at(6))

    def test_shift(self):
        """
        Test the shift operation.
        """
        ij = [5, 6]
        diffa = []
        diffb = []
        self.diff._initialize()

        self.diff._shift(ij, diffa, diffb)

        self.assertEqual([4, 5], ij)
        self.assertEqual(['r'], diffa)
        self.assertEqual(['r'], diffb)

    def test_push_b(self):
        """
        Test the push b operation.
        """
        ij = [2, 0]
        diffa_old = ['p', EMPTY, EMPTY, EMPTY, 'e', 'r']
        diffb_old = ['p', 'o', 's', 't', 'e', 'r']
        diffa = diffa_old.copy()
        diffb = diffb_old.copy()
        self.diff._initialize()

        self.diff._push_b(ij, diffa, diffb)

        self.assertEqual([1, 0], ij)
        self.assertEqual(['a'] + diffa_old, diffa)
        self.assertEqual([EMPTY] + diffb_old, diffb)

    def test_push_a(self):
        """
        Test the push a operation.
        """
        ij = [3, 4]
        diffa = ['e', 'r']
        diffb = ['e', 'r']
        self.diff._initialize()

        self.diff._push_a(ij, diffa, diffb)

        self.assertEqual([3, 3], ij)
        self.assertEqual([EMPTY, 'e', 'r'], diffa)
        self.assertEqual(['t', 'e', 'r'], diffb)

    def test_build_diffs(self):
        self.diff._initialize()
        self.diff._compute_distance_matrix()

        diffa, diffb = self.diff._build_diffs()
        self.assertEqual(['p', 'a', 'p', EMPTY, EMPTY, EMPTY, 'e', 'r'], diffa)
        self.assertEqual(['p', EMPTY, EMPTY, 'o', 's', 't', 'e', 'r'], diffb)