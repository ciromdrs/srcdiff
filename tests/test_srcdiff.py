'''Tests for the srcdiff script.'''

import unittest
import src.srcdiff


class TestSrcDiff(unittest.TestCase):
    def test_loads_class(self):
        d = src.srcdiff.SrcDiff()
        self.assertIsInstance(d, src.srcdiff.SrcDiff)