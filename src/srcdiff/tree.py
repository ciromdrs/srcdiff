import ast
import os


class Tree:
    """Tree structure representing representing Python projects, including abstract syntax trees of scripts and directory nodes.

    Attributes:
    - `type` is the type of the node, either 'Directory', 'File' or the name of an `ast.AST` subclass.
    - `value` provides additional useful information about a node. Ex.: for a node of type `Constant`, the `value` could be `3.14`.
    - `children` is a list of child `Tree` nodes.
    - `parent` is the parent `Tree` node. It is `None` if the node is the root of the tree.
    - `index` is the index of a node in the Tree. It is used by the tree-diff algorithm.
    """

    def __init__(self,
                 type_: str,
                 value: str | int | bool | float | None = None,
                 children: list['Tree'] = [],
                 parent: 'Tree | None' = None,
                 auto_set_index: bool = False,
                 last_index: int = 0):
        """Creates a Tree object.
        `type_`, `value`, and `children` correspond to the class' attributes.
        `must_set_index` is a boolean indicating whether it should recursively compute the index of the entire Tree (via the set_index method) or assign simply `last_index+1` to this node's `index`.
        `last_index` is the last index assigned in the construction of the tree.
        """
        self.type: str = type_
        self.value: str | int | bool | float | None = value
        self.children: list['Tree'] = children
        self.parent: 'Tree | None' = parent
        # To avoid unnecessary computing
        if auto_set_index:
            # Either computes the index of the entire Tree
            self.set_index(last_index)
        else:
            # Or simply assigns the value supplied
            self._index = last_index + 1

    @classmethod
    def from_AST(cls, astree: ast.AST, last_index: int = 0) -> 'Tree':
        """Recursively builds a `Tree` node from an abstract syntax tree.
        `astree` is the abstract syntax tree for a given Python script.
        Returns the `Tree` object.
        """
        # The astree node class name is the type of the new node
        type_ = type(astree).__name__
        # The value might come from many attributes of the astree
        value = None
        for attr in ['id', 'name', 'value', 'arg']:
            if hasattr(astree, attr):
                v = eval(f'astree.{attr}')
                if type(v) in [bool, str, int, float, type(None)]:
                    value = v
        # The children list is built recursively
        children = []
        for subastree in ast.iter_child_nodes(astree):
            child = cls.from_AST(subastree, last_index)
            children += [child]
            last_index = child.get_index() + 1
        node = cls(type_, value, children, last_index=last_index)
        return node

    @classmethod
    def from_file(cls, filename: str, last_index: int = 0) -> 'Tree':
        """Builds a `Tree` node from a Python script file.

        `filename` is the path to the Python script file.
        Returns the `Tree` object.
        """
        f = open(filename)
        contents = f.read()
        f.close()
        astree = ast.parse(contents)
        subtree = cls.from_AST(astree, last_index)
        last_index = subtree.get_index() + 1
        root = cls('File', filename, [subtree], last_index=last_index)
        return root

    @classmethod
    def from_dir(cls, path: str, last_index: int = 0, ignore: list[str] = ['__pycache__'], recursive=True) -> 'Tree':
        """Build a `Tree` node from a directory.

        `path` is the path to the directory.
        `last_index` is used to compute the index.
        `ignore` is a list of files and directories to ignore.
        `recursive` indicates if it must explore subdirectories recursively.
        Returns the `Tree` object.
        """
        children = []
        # List of files and directories
        files_dirs = [path + '/' + fd for fd in os.listdir(path)]
        files = [f for f in files_dirs if os.path.isfile(f)]
        # Parse files first
        for f in files:
            if f not in ignore:
                node = cls.from_file(f, last_index)
                children += [node]
                last_index = node.get_index() + 1
        dirs = [d for d in files_dirs if os.path.isdir(d)]
        # Parse directories
        for d in dirs:
            if d not in ignore:
                # By default, create a node non-recursively.
                # This avoids node from being None.
                node: Tree = Tree('Directory', path)
                if recursive:
                    # If recursive is True, recreate it.
                    node = cls.from_dir(d, last_index)
                    last_index = node.get_index() + 1
                children += [node]
        root = Tree('Directory', path, children, last_index=last_index)
        return root

    def __repr__(self, recursive=True, current_indent=0, indent_size=4) -> str:
        """Pretty-prints a `Tree` to `str`.

        `recursive` is a flag indicating if it should print also the children.
        `current_indent` is the current indentation level.
        `indent_size` is the indentation size, in number of spaces.
        Returns a `str` representing the `Tree` object.
        """
        # Left padding
        left_padding = current_indent * ' '
        # Type
        type_ = f"'{self.type}'"
        # Value
        value = ''
        if self.value is not None:
            aux = None
            if type(self.value) == str:
                aux = repr(self.value)  # Add quotes to strings
            value = f", value={aux}"
        # Index
        index = f", last_index={self.get_index()}"
        # Children
        children = ''
        if self.children:
            children = ', children=['
            if recursive:
                children += '\n'
                for child in self.children:
                    children += \
                        child.__repr__(
                            recursive, current_indent + indent_size, indent_size
                        ) + ',\n'
            else:
                children += '...'
            children += left_padding + ']'
        # Join everything
        out = left_padding + f'Tree({type_}{value}{index}{children})'
        return out

    def equals(self, another: 'Tree') -> tuple[bool, str | None, str | None]:
        """Compares this Tree to another.

        `another` is the other Tree object to compare to.
        Returns a boolean indicating if the trees are equal and the paths to the pair of differing nodes if the trees are different.
        """
        # These variables indicate the path to the first differing elements.
        # They are useful for debugging purposes.
        diff_self = f'{self.type}' + (f':{self.value}' if self.value else '')
        diff_another = f'{another.type}' + \
            (f':{another.value}' if another.value else '')
        # First, compare the type, value and number of children
        if self.type != another.type or \
                self.value != another.value or \
                len(self.children) != len(another.children):
            return False, diff_self, diff_another
        # Then, compare each children, in the same order
        for i in range(len(self.children)):
            res, diff_child_self, diff_child_another = self.children[i].equals(
                another.children[i])
            if not res:
                diff_self_complete = f'{diff_self}/{i}/{diff_child_self}'
                diff_another_complete = f'{diff_another}/{i}/{diff_child_another}'
                return False, diff_self_complete, diff_another_complete
        # If all checks passed, they are equal
        return True, None, None

    def set_index(self, last_index):
        """Recursively sets the indexes of this node and all its children based on the `last_index`.
        """
        # Assigns indices to children first
        updated_index = last_index
        for c in self.children:
            c.set_index(updated_index)
            updated_index = c.get_index()
        # Assigns the index to self
        self._index: int = updated_index + 1

    def get_index(self) -> int:
        """Returns the index of this node.
        If it has not yet been assigned via `set_index`, throws an assertion error.
        """
        assert self._index > 0, 'self._index not assigned yet'
        return self._index

    def keyroots(self) -> list['Tree']:
        """Returns the Tree's keyroots, used by the diff algorithm."""
        return self._keyroots(is_keyroot=True)

    def _keyroots(self, is_keyroot: bool) -> list['Tree']:
        """Recursively finds the keyroots of the Tree.
        Basically, we know a node is a keyroot if it is not the first child of a node.
        For the formal definition, consult:
        Zhang, K., & Shasha, D. (1989). Simple Fast Algorithms for the Editing Distance Between Trees and Related Problems. SIAM J. Comput., 18, 1245-1262.

        `is_keyroot` indicates whether this node is a keyroot.
        """
        keyroots: list['Tree'] = []
        if len(self.children) > 0:
            keyroots += self.children[0]._keyroots(is_keyroot=False)
            for c in self.children[1:]:
                keyroots += c._keyroots(is_keyroot=True)
        if is_keyroot:
            keyroots += [self]
        return keyroots

    def leftmost_leaf(self) -> 'Tree':
        """Returns the leftmost leaf of this node."""
        if len(self.children) == 0:
            return self
        return self.children[0].leftmost_leaf()