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
        last_index = 10
        tree = Tree(type_, value, children, last_index=last_index, auto_set_index=True)

        self.assertEqual(tree.type, type_)
        self.assertEqual(tree.value, value)
        self.assertEqual(tree.children, children)
        self.assertEqual(tree.get_index(), last_index + 1)

    def test_init_with_missing_parameters(self):
        """Test if a Tree is instantiated correctly with missing parameters."""
        type_ = 'TheType'
        tree = Tree(type_)

        self.assertEqual(tree.type, type_)
        self.assertEqual(tree.value, None)
        self.assertEqual(tree.children, [])
        self.assertEqual(tree.get_index(), 1)

    def test_from_file(self):
        """Test if it builds a Tree from a Python script file."""
        # Python scritps and their Tree representation to use in tests.
        data = [
            ['blank.py', Tree('File', value='tests/data/scripts/blank.py', children=[
                Tree('Module'),
            ])
            ],
            ['str.py', Tree('File', value='tests/data/scripts/str.py', children=[
                Tree('Module', children=[
                    Tree('Expr', children=[
                        Tree('Constant', value='hello'),
                    ]),
                ]),
            ])
            ],
            ['int.py', Tree('File', value='tests/data/scripts/int.py', children=[
                Tree('Module', children=[
                    Tree('Expr', children=[
                        Tree('Constant', value=123),
                    ]),
                ]),
            ])
            ],
            ['bool.py', Tree('File', value='tests/data/scripts/bool.py', children=[
                Tree('Module', children=[
                    Tree('Expr', children=[
                        Tree('Constant', value=False),
                    ]),
                ]),
            ])
            ],
            ['float.py', Tree('File', value='tests/data/scripts/float.py', children=[
                Tree('Module', children=[
                    Tree('Expr', children=[
                        Tree('Constant', value=3.14),
                    ]),
                ]),
            ])
            ],
            ['none.py', Tree('File', value='tests/data/scripts/none.py', children=[
                Tree('Module', children=[
                    Tree('Expr', children=[
                        Tree('Constant'),
                    ]),
                ]),
            ])
            ],
            ['function.py', Tree('File', value='tests/data/scripts/function.py', children=[
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
                ]),
            ])
            ],
            ['class.py', Tree('File', value='tests/data/scripts/class.py', children=[
                Tree('Module', children=[
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
                ]),
            ])]
        ]

        for file, expected in data:
            path = 'tests/data/scripts/' + file
            with self.subTest(path):
                got = Tree.from_file(path)
                res, _, _ = got.equals(expected)

                self.assertTrue(
                    res,
                    f'Expected:\n{expected}\ngot:\n{got}\n')

    def test_from_dir(self):
        """Test if it builds a Tree from a directory."""
        # Directories and their Tree representation to use in tests.
        data = [
            ['dirs/ab', Tree('Directory', value='tests/data/dirs/ab', children=[
                Tree('File', value='tests/data/dirs/ab/a.py', children=[
                    Tree('Module'),
                ]),
                Tree('File', value='tests/data/dirs/ab/b.py', children=[
                    Tree('Module'),
                ]),
            ])],
            ['dirs/with_subdir', Tree('Directory', value='tests/data/dirs/with_subdir', children=[
                Tree('File', value='tests/data/dirs/with_subdir/at_parent.py', children=[
                    Tree('Module'),
                ]),
                Tree('Directory', value='tests/data/dirs/with_subdir/subdir', children=[
                    Tree('File', value='tests/data/dirs/with_subdir/subdir/at_subdir.py', children=[
                        Tree('Module'),
                    ]),
                ]),
            ])
            ],
        ]
        for directory, expected in data:
            path = 'tests/data/' + directory
            with self.subTest(path):
                got = Tree.from_dir(path)
                res, diffa, diffb = got.equals(expected)

                msg = f'\nExpected:\n{expected}\ngot:\n{got}\n' + \
                    f'First differing elements:\n- {diffa}\n+ {diffb}'
                self.assertTrue(res, msg)

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

    def test_set_index(self):
        tree = Tree('ClassDef', value='Dumber', children=[
            Tree('Name', value='Dummy', children=[
                Tree('Load'),
            ]),
            Tree('FunctionDef', value='do_nothing', children=[
                Tree('arguments', children=[
                    Tree('arg', value='self'),
                ]),
                Tree('Pass'),
            ]),
        ],
        auto_set_index=True)
        name = tree.children[0]
        load = name.children[0]
        function_def = tree.children[1]
        arguments = function_def.children[0]
        arg = arguments.children[0]
        pass_ = function_def.children[1]

        self.assertEqual(1, load.get_index())
        self.assertEqual(2, name.get_index())
        self.assertEqual(3, arg.get_index())
        self.assertEqual(4, arguments.get_index())
        self.assertEqual(5, pass_.get_index())
        self.assertEqual(6, function_def.get_index())
        self.assertEqual(7, tree.get_index())