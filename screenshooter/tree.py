#!/usr/bin/env python3
# tree.py

"""Top-level package for RP Tree.

Based on: https://realpython.com/directory-tree-generator-python/
"""

import os
import pathlib
import sys
import click  # Changing from Argparse to Click

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "

# Command-Line Interface
@click.command()
@click.argument("directory")
@click.option("--debug/--no-debug", default=False)
def cli(directory, debug):
    # Debug
    click.echo("Debug mode is %s" % ("on" if debug else "off"))

    if debug:
        print("Debug set but not doing anything")

    # Directory
    root_dir = pathlib.Path(directory)
    if not root_dir.is_dir():
        print("The specified root directory doesn't exist")
        sys.exit()

    # Do the stuff...
    tree = DirectoryTree(root_dir)
    tree.generate()


# Initiate the generation of a  Directory Tree
class DirectoryTree:
    def __init__(self, root_dir):
        self._generator = _TreeGenerator(root_dir)

    def generate(self):
        """This method creates a local variable called tree that holds
        the result of calling .build_tree() on the tree generator object."""
        tree = self._generator.build_tree()

        for entry in tree:
            print(entry)


# Generate the entries within the Directory Tree
class _TreeGenerator:
    def __init__(self, root_dir, dir_only=False):
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._tree = []

    def build_tree(self):
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self):
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory, prefix=""):
        entries = directory.iterdir()
        entries = sorted(entries, key=lambda entry: entry.is_file())
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(entry, index, entries_count, prefix, connector)
            else:
                self._add_file(entry, prefix, connector)

    def _add_directory(self, directory, index, entries_count, prefix, connector):
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(
            directory=directory,
            prefix=prefix,
        )
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        self._tree.append(f"{prefix}{connector} {file.name}")


if __name__ == "__main__":
    cli()
