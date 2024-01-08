"""Tests for the diff2 script."""

import unittest
from src.diff2 import diff2, Diff2


class TestDiff2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = 'paper'
        cls.b = 'poster'
        cls.diff = Diff2(cls.a, cls.b)

    def test_init(self):
        """
        Test if a Diff2 object is instantiated correctly.
        """
        # Assert the strings are equal
        self.assertEqual(self.diff._a, self.a)
        self.assertEqual(self.diff._b, self.b)

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

    def test_returns_all_characters(self):
        """
        Test if all characters are in the diff result.
        """
        self.fail('Not implemented yet')
        for char in self.a:
            self.assertIn(char, self.diff.a)
        for char in self.b:
            self.assertIn(char, self.diff.b)

    def test_number_of_blank_spaces(self):
        """
        Test the amount of fill spaces.
        """
        self.fail('Not implemented yet')
        self.assertEqual(3, self.da.count(EMPTY))
        self.assertEqual(2, self.db.count(EMPTY))

    def test_diffa_result(self):
        """
        Test the diff result of `a`.
        """
        self.fail('Not implemented yet')
        self.assertEqual(
            ['p', 'a', 'p', EMPTY, EMPTY, EMPTY, 'e', 'r'], self.da)

    def test_diffb_result(self):
        """
        Test the diff result of `b`.
        """
        self.fail('Not implemented yet')
        self.assertEqual(['p', EMPTY, EMPTY, 'o', 's', 't', 'e', 'r'], self.db)

    def test_compute_base_row(self):
        """
        Test the computation of the base row for the dynamic programming table.
        """
        self.fail('Not implemented yet')
