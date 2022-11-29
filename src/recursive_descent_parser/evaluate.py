from dataclasses import dataclass
from typing import Optional

from .errors import UnexpectedUnaryOperatorError, UnexpectedDataTypeError
from .parser import SyntaxTree
from .types import SyntaxKind, SyntaxNode
from .utils import cast


@dataclass
class Evaluator:
    syntax_tree: SyntaxTree

    def evaluate(self) -> Optional[float | int]:
        return self._evaluate(self.syntax_tree.root)

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
                    case SyntaxKind.NOT:
                        val = self._evaluate(expression)
                        if not isinstance(val, int):
                            raise UnexpectedDataTypeError(
                                f"Can't use NOT operator on {type(val)} "
                            )
                        return ~val
                    case _:
                        raise UnexpectedUnaryOperatorError(
                            f"Can't recognize {operator.kind} as unary operator"
                        )
            case SyntaxKind.PARENTHESIZED_EXPRESSION:
                return self._evaluate(root.expression)  # type: ignore
            case SyntaxKind.NUMBER_EXPRESSION:
                number_token = root.number_token  # type: ignore
                return self._evaluate(number_token)  # type: ignore
