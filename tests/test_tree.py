"""
Tests for the tree script.
"""
import unittest

from src.srcdiff.tree import Tree


class TestTree(unittest.TestCase):
    """Test case for the Tree class."""
    def setUp(self):
        super().setUp()
        
        self.example_tree = Tree('f', children=[
            Tree('d', children=[
                Tree('a'),
                Tree('c', children=[
                    Tree('b'),
                ]),
            ]),
            Tree('e'),
        ])

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
        self.assertEqual(tree._node_at, {1:tree})

    def test_parent(self):
        """Test if the parent attribute is set correctly."""
        tree = Tree('TheType', children=[
            Tree('TheType')
        ])
        child = tree.children[0]

        self.assertEqual(child.parent, tree)

    def test_from_file(self):
        """Test if it builds a Tree from a Python script file."""
        # Python scritps and their Tree representation to use in tests.
        data = [
            ['blank.py', Tree('File', value='tests/data/scripts/blank.py', children=[
                Tree('Module'),
            ])],
            ['str.py', Tree('File', value='tests/data/scripts/str.py', children=[
                Tree('Module', children=[
                    Tree('Expr', children=[
                        Tree('Constant', value='hello'),
                    ]),
                ]),
            ])],
            ['int.py', Tree('File', value='tests/data/scripts/int.py', children=[
                Tree('Module', children=[
                    Tree('Expr', children=[
                        Tree('Constant', value=123),
                    ]),
                ]),
            ])],
            ['bool.py', Tree('File', value='tests/data/scripts/bool.py', children=[
                Tree('Module', children=[
                    Tree('Expr', children=[
                        Tree('Constant', value=False),
                    ]),
                ]),
            ])],
            ['float.py', Tree('File', value='tests/data/scripts/float.py', children=[
                Tree('Module', children=[
                    Tree('Expr', children=[
                        Tree('Constant', value=3.14),
                    ]),
                ]),
            ])],
            ['none.py', Tree('File', value='tests/data/scripts/none.py', children=[
                Tree('Module', children=[
                    Tree('Expr', children=[
                        Tree('Constant'),
                    ]),
                ]),
            ])
            ],
            ['list.py', Tree('File', value='tests/data/scripts/list.py', children=[
                Tree('Module', children=[
                    Tree('Expr', children=[
                        Tree('List', children=[
                            Tree('Constant', value='just'),
                            Tree('Constant', value='a'),
                            Tree('Constant', value='list'),
                            Tree('Load'),
                        ]),
                    ]),
                ]),
            ])],
            ['dict.py', Tree('File', value='tests/data/scripts/dict.py', children=[
                Tree('Module', children=[
                    Tree('Expr', children=[
                        Tree('Dict', children=[
                            Tree('Constant', value='just'),
                            Tree('Constant', value='a dict'),
                        ]),
                    ]),
                ]),
            ])],
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
            ])],
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
                                Tree('arg', value='data', children=[
                                    Tree('Name', value='int', children=[
                                        Tree('Load'),
                                    ]),
                                ]),
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
                res, diff_a, diff_b = got.equals(expected)

                self.assertTrue(
                    res,
                    f'\nExpected:\n{expected}\nGot:\n{got}\nDiff:\n- {diff_a}\n+ {diff_b}')

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
                Tree('Module'), Tree('Module'), True, None, None, True],
            ['Different value.',
                Tree('Name', 'a'), Tree('Name', 'b'), False, 'Name:a', 'Name:b', True],
            ['Different children.',
                Tree('Name', 'a', [Tree('Expr')]),
                Tree('Name', 'a', [Tree('Constant')]),
                False, 'Name:a/0/Expr', 'Name:a/0/Constant', True],
            ['Different type.',
                Tree('Module'), Tree('Arg'), False, 'Module', 'Arg', True],
            ['Ignore different children.',
                Tree('Name', 'a', [Tree('Expr')]),
                Tree('Name', 'a', [Tree('Constant')]),
                True, None, None, False],
        ]

        for subtest_label, treea, treeb, expected, exp_diffa, exp_diffb, \
                compare_children in data:
            with self.subTest(subtest_label):
                got, got_diffa, got_diffb = treea.equals(
                    treeb, compare_children)

                self.assertEqual(expected, got)
                self.assertEqual(exp_diffa, got_diffa)
                self.assertEqual(exp_diffb, got_diffb)

    def test_keyroots(self):
        tree = self.example_tree
        f = tree
        c = tree.children[0].children[1]
        e = tree.children[1]

        self.assertEqual([c, e, f], tree.keyroots())

    def test_leftmost_leaf(self):
        f = self.example_tree
        d = f.children[0]
        a = d.children[0]
        c = d.children[1]
        b = c.children[0]
        e = f.children[1]

        self.assertEqual(a, f.leftmost_leaf())
        self.assertEqual(a, d.leftmost_leaf())
        self.assertEqual(a, a.leftmost_leaf())
        self.assertEqual(b, c.leftmost_leaf())
        self.assertEqual(b, b.leftmost_leaf())
        self.assertEqual(e, e.leftmost_leaf())

    def test_size(self):
        f = self.example_tree
        d = f.children[0]
        a = d.children[0]
        c = d.children[1]
        b = c.children[0]
        e = f.children[1]

        self.assertEqual(6, f.size())
        self.assertEqual(4, d.size())
        self.assertEqual(1, a.size())
        self.assertEqual(2, c.size())
        self.assertEqual(1, b.size())
        self.assertEqual(1, e.size())
        self.assertEqual(6, len(f))
        self.assertEqual(4, len(d))
        self.assertEqual(1, len(a))
        self.assertEqual(2, len(c))
        self.assertEqual(1, len(b))
        self.assertEqual(1, len(e))

    def test_node_at(self):
        """Test the _node_at attribute."""
        f = self.example_tree
        d = f.children[0]
        a = d.children[0]
        c = d.children[1]
        b = c.children[0]
        e = f.children[1]

        self.assertEqual({1:a, 2:b, 3:c, 4:d, 5:e, 6:f},
                         self.example_tree._node_at)

    def test_index_of(self):
        """Test the index_of attribute."""
        tree = self.example_tree
        f = tree
        d = f.children[0]
        a = d.children[0]
        c = d.children[1]
        b = c.children[0]
        e = f.children[1]

        self.assertEqual(1, tree.index_of[a])
        self.assertEqual(2, tree.index_of[b])
        self.assertEqual(3, tree.index_of[c])
        self.assertEqual(4, tree.index_of[d])
        self.assertEqual(5, tree.index_of[e])
        self.assertEqual(6, tree.index_of[f])

    def test_getitem(self):
        """Test the __getitem__ magic method."""
        tree = self.example_tree
        d = tree.children[0]
        a = d.children[0]
        c = d.children[1]
        b = c.children[0]

        self.assertEqual(a, tree[1])
        self.assertEqual(b, tree[2])
        self.assertEqual(c, tree[3])
        self.assertEqual(d, tree[4])
        self.assertEqual(a, d[1])
        self.assertEqual(b, d[2])
        self.assertEqual(c, d[3])
        self.assertEqual(d, d[4])
        self.assertEqual(b, c[1])

    def test_forest(self):
        """Test the _forest method."""
        tree = self.example_tree
        f = tree
        d = f.children[0]
        a = d.children[0]
        c = d.children[1]
        b = c.children[0]
        e = f.children[1]

        # Expected forest, first index, last index
        data = [
            [[a], 1, 1],
            [[a, b], 1, 2],
            [[a, c], 1, 3],
            [[d], 1, 4],
            [[d, e], 1, 5],
            [[f], 1, 6],
        ]
        for expected, first, last in data:
            subtest_label = f'First: {first}, last: {last}'
            with self.subTest(subtest_label):
                self.assertEqual(expected, tree.forest(first, last))