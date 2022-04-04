from recursive_descent_parser import SyntaxTree
from termcolor import cprint

if __name__ == "__main__":
    while True:
        line = input("$ ")
        syntax_tree = SyntaxTree.generate(line)
        for error in syntax_tree.errors:
            cprint(error, "red")  # type: ignore
        syntax_tree.pretty_print()
        if not syntax_tree.errors:
            print(syntax_tree.evaluate())
