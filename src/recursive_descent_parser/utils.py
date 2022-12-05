from .errors import UnexpectedBinaryOperatorError
from .lexer import SyntaxKind
from .parser import SyntaxTree
from .SyntaxTypes import SyntaxNode
from collections import defaultdict
from src import cprint

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


def cast(a: int | float, operator: SyntaxNode, b: int | float) -> float | int:
    match operator.kind:
        case SyntaxKind.PLUS:
            result = a + b
        case SyntaxKind.MINUS:
            result = a - b
        case SyntaxKind.STAR | SyntaxKind.IMPLICIT_MULTIPLY:
            result = a * b
        case SyntaxKind.FORWARD_SLASH:
            result = a / b
        case SyntaxKind.TWO_STAR:
            result = a**b
        case SyntaxKind.OR:
            result = a | b  # type: ignore
        case SyntaxKind.AND:
            result = a & b  # type: ignore
        case SyntaxKind.XOR:
            return a ^ b  # type: ignore
        case _:
            raise UnexpectedBinaryOperatorError()
    if type(result) is float and result % 1 == 0:
        return int(result)
    return result
