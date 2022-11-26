from dataclasses import dataclass
from typing import Optional

from .errors import UnexpectedUnaryOperatorError
from .parser import SyntaxTree
from .types import SyntaxKind, SyntaxNode
from .utils import cast
from src import cprint


@dataclass
class Evaluator:
    syntax_tree: SyntaxTree

    def evaluate(self) -> Optional[float | int]:
        try:
            return self._evaluate(self.syntax_tree.root)
        except ZeroDivisionError as e:
            cprint(e, "red", attrs=["bold"])  # type: ignore

    def _evaluate(self, root: SyntaxNode) -> float | int:  # type: ignore
        match root.kind:
            case SyntaxKind.NUMBER:
                return root.value  # type: ignore
            case SyntaxKind.BINARY_EXPRESSION:
                left, operator, right = root.children()
                return cast(self._evaluate(left), operator, self._evaluate(right))

            case SyntaxKind.UNARY_EXPRESSION:
                operator, expression = root.children()
                match operator.kind:
                    case SyntaxKind.PLUS:
                        return self._evaluate(expression)
                    case SyntaxKind.MINUS:
                        return -self._evaluate(expression)
                    case _:
                        raise UnexpectedUnaryOperatorError(
                            f"Can't recognize {operator.kind} as unary operator"
                        )
            case SyntaxKind.PARENTHESIZED_EXPRESSION:
                return self._evaluate(root.expression)  # type: ignore
            case SyntaxKind.NUMBER_EXPRESSION:
                number_token = root.number_token  # type: ignore
                return self._evaluate(number_token)  # type: ignore
