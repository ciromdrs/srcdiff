import ast


class Tree:
    """Tree structure representing representing Python projects, including abstract syntax trees of scripts and directory nodes.

    `type_` is the type of the node, either 'Directory' or the name of an `ast.AST` subclass.
    `value` provides additional useful information about a node. Ex.: for a node of type `Constant`, the `value` could be `3.14`.
    `children` is a list of child `Tree` nodes.
    """
    type_: str = ''
    value: str | int | bool | float | None = None
    children: list['Tree'] = []

    def __init__(self,
                 type_,
                 value: str | int | bool | float | None = None,
                 children: list['Tree'] = []):
        self.type = type_
        self.value = value
        self.children = children

    @classmethod
    def from_AST(cls, astree: ast.AST) -> 'Tree':
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
            child = cls.from_AST(subastree)
            children += [child]
        node = cls(type_, value, children)
        return node

    @classmethod
    def from_file(cls, filename: str) -> 'Tree':
        """Builds a `Tree` node from a Python script file.

        `filename` is the path to the Python script file.
        Returns the `Tree` object.
        """
        f = open(filename)
        contents = f.read()
        f.close()
        astree = ast.parse(contents)
        return cls.from_AST(astree)

    @classmethod
    def from_dir(cls, path: str) -> 'Tree':
        """TODO: Build a `Tree` node from a directory.

        `path` is the path to the directory.
        Returns the `Tree` object.
        """
        raise Exception('Not implemented yet')

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
        out = left_padding + f'Tree({type_}{value}{children})'
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
