from src.recursive_descent_parser import SyntaxTree
from src import cprint

if __name__ == "__main__":
    while True:
        line = input("$ ")
        if line.lower() in ("exit", "quit"):
            break
        syntax_tree = SyntaxTree.generate(line)
        for error in syntax_tree.errors:
            print(error)
            cprint(error, "red", attrs=["bold"])  # type: ignore
        syntax_tree.pretty_print()
        if not syntax_tree.errors:
            if result := syntax_tree.evaluate():
                print(result)
