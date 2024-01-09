"""Tests for the diff2 script."""

import unittest
from src.diff2 import diff2, Diff2, EMPTY


class TestDiff2(unittest.TestCase):
    def setUp(self):
        self.a = 'paper'
        self.b = 'poster'
        self.diff = Diff2(self.a, self.b)

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

        # The dynamic programming table starts empty and has size `(n+1) * (m+1)`
        self.assertEqual(
            self.diff.t,
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

    def test_compute_base_row(self):
        """
        Test the computation of the base row for the dynamic programming table.
        """
        self.diff._initialize()

        self.diff._compute_base_row_and_column()

        # The distances in the base row are 0, 1, 2, ... , m
        self.assertEqual(self.diff.t[0], list(range(self.diff.m + 1)))
        # The distances in the base column are 0, 1, 2, ... , n
        for i in range(self.diff.n + 1):
            self.assertEqual(
                i,
                self.diff.t[i][0],
                f'Expected t[{i}][0] to be {i}, got {self.diff.t[i][0]}.')

    def test_run(self):
        """
        Test if the minimum edit distance and the dynamic programming table are correct.
        """
        distance = self.diff.run()

        self.assertEqual(5, distance)
        expected_table = [
            [0, 1, 2, 3, 4, 5, 6],
            [1, 0, 1, 2, 3, 4, 5],
            [2, 1, 2, 3, 4, 5, 6],
            [3, 2, 3, 4, 5, 6, 7],
            [4, 3, 4, 5, 6, 5, 6],
            [5, 4, 5, 6, 7, 6, 5],
        ]
        self.assertEqual(expected_table, self.diff.t)
