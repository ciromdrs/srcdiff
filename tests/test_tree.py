"""
Tests for the tree script.
"""
import unittest

from src.srcdiff.tree import Tree


class TestTree(unittest.TestCase):
    """Test case for the Tree class."""

    def test_init(self):
        """Test if a Tree is instantiated correctly using the constructor."""
        type_ = 'TheType'
        value = 'the_value'
        children = []
        tree = Tree(type_, value, children)

        self.assertEqual(tree.type, type_)
        self.assertEqual(tree.value, value)
        self.assertEqual(tree.children, children)

    def test_init_with_missing_parameters(self):
        """Test if a Tree is instantiated correctly with missing parameters."""
        type_ = 'TheType'
        tree = Tree(type_)

        self.assertEqual(tree.type, type_)
        self.assertEqual(tree.value, None)
        self.assertEqual(tree.children, [])

    def test_from_file(self):
        """Test if it builds a Tree from a Python script file."""
        # Python scritps and their Tree representation to use in tests.
        data = [
            ['blank.py', Tree('Module')],
            ['str.py', Tree('Module', children=[
                Tree('Expr', children=[
                    Tree('Constant', value='hello'),
                ]),
            ])],
            ['int.py', Tree('Module', children=[
                Tree('Expr', children=[
                    Tree('Constant', value=123),
                ]),
            ])],
            ['bool.py', Tree('Module', children=[
                Tree('Expr', children=[
                    Tree('Constant', value=False),
                ]),
            ])],
            ['float.py', Tree('Module', children=[
                Tree('Expr', children=[
                    Tree('Constant', value=3.14),
                ]),
            ])],
            ['none.py', Tree('Module', children=[
                Tree('Expr', children=[
                    Tree('Constant', value=None),
                ]),
            ])],
            [
                'function.py',
                Tree('Module', children=[
                    Tree('FunctionDef', value='return_a', children=[
                        Tree('arguments', children=[
                            Tree('arg', value='a', children=[
                                Tree('Name', value='int', children=[
                                    Tree('Load'),
                                ]),
                            ]),
                            Tree('arg', value='b', children=[
                                Tree('Name', value='int', children=[
                                    Tree('Load'),
                                ]),
                            ]),
                        ]),
                        Tree('Return', children=[
                            Tree('Name', value='a', children=[
                                Tree('Load'),
                            ]),
                        ]),
                        Tree('Name', value='int', children=[
                            Tree('Load'),
                        ]),
                    ]),
                ])
            ],
            ['class.py', Tree('Module', children=[
                Tree('ClassDef', value='Dummy', children=[
                    Tree('Pass'),
                ]),
                Tree('ClassDef', value='Dumber', children=[
                    Tree('Name', value='Dummy', children=[
                        Tree('Load'),
                    ]),
                    Tree('FunctionDef', value='do_nothing', children=[
                        Tree('arguments', children=[
                            Tree('arg', value='self'),
                        ]),
                        Tree('Pass'),
                    ]),
                ]),
            ])],
        ]

        for file, expected in data:
            path = 'tests/data/' + file
            with self.subTest(path):
                got = Tree.from_file(path)
                res, diffa, diffb = got.equals(expected)

                self.assertTrue(
                    res,
                    f'Expected:\n{expected}\ngot:\n{got}\n')

    def test_equals(self):
        """Test the equals method."""
        # Subtest label, treea, treeb, expected_res, diffa, diffb
        data = [
            ['Equal type, value and children.',
                Tree('Module'), Tree('Module'), True, None, None],
            ['Different value.',
                Tree('Name', 'a'), Tree('Name', 'b'), False, 'Name:a', 'Name:b'],
            ['Different children.',
                Tree('Name', 'a', [Tree('Expr')]),
                Tree('Name', 'a', [Tree('Constant')]),
                False, 'Name:a/0/Expr', 'Name:a/0/Constant'],
            ['Different type.',
                Tree('Module'), Tree('Arg'), False, 'Module', 'Arg'],
        ]

        for subtest_label, treea, treeb, expected, exp_diffa, exp_diffb in data:
            with self.subTest(subtest_label):
                got, got_diffa, got_diffb = treea.equals(treeb)

                self.assertEqual(expected, got)
                self.assertEqual(exp_diffa, got_diffa)
                self.assertEqual(exp_diffb, got_diffb)
