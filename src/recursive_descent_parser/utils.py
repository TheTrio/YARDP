from recursive_descent_parser.lexer import SyntaxKind
from .parser import SyntaxNode, SyntaxTree
from termcolor import cprint
from collections import defaultdict

colors = defaultdict(
    lambda: "red",
    {
        SyntaxKind.BINARY_EXPRESSION: "yellow",
        SyntaxKind.NUMBER_EXPRESSION: "cyan",
        SyntaxKind.PARENTHESIZED_EXPRESSION: "magenta",
        SyntaxKind.NUMBER: "blue",
    },
)


def _pretty_print(syntax: SyntaxNode, indent: int = 0):
    print(" " * indent, end="")
    children = syntax.children()
    if children:
        cprint(f"<{syntax.kind}>", colors[syntax.kind])  # type: ignore
        for child in children:
            if child is not None:
                _pretty_print(child, indent + 2)
        print(" " * indent, end="")
        cprint(f"</{syntax.kind}>", colors[syntax.kind])  # type: ignore
    else:
        cprint(
            f"<{syntax.kind} {f'value={syntax.value}' if syntax.value is not None else ''} />",
            colors[syntax.kind],  # type: ignore
        )


def pretty_print(syntax_tree: SyntaxTree):
    _pretty_print(syntax_tree.root)
