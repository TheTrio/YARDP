from src.recursive_descent_parser import SyntaxTree
from src import cprint

if __name__ == "__main__":
    while True:
        line = input("$ ")
        if line.lower() in ("exit", "quit"):
            break
        syntax_tree = SyntaxTree.generate(line)
        for error in syntax_tree.errors:
            cprint(error, "red", attrs=["bold"])  # type: ignore
        syntax_tree.pretty_print()
        if not syntax_tree.errors:
            try:
                if (result := syntax_tree.evaluate()) is not None:
                    print(result)
            except Exception as e:
                cprint(
                    "Received the following error while evaluating the expression",
                    "red",
                    attrs=["bold"],
                    end="",
                )
                cprint(f": {e}", "magenta")
