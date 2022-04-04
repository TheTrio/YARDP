from dataclasses import dataclass

from .errors import UnexpectedBinaryOperatorError, UnexpectedUnaryOperatorError
from .parser import SyntaxTree, ExpressionSyntax
from .types import SyntaxKind


@dataclass
class Evaluator:
    syntax_tree: SyntaxTree

    def evaluate(self) -> int:
        return self._evaluate(self.syntax_tree.root)

    def _evaluate(self, root: ExpressionSyntax) -> int:  # type: ignore
        match root.kind:
            case SyntaxKind.NUMBER:
                return root.value  # type: ignore
            case SyntaxKind.BINARY_EXPRESSION:
                left, operator, right = root.children()
                match operator.kind:
                    case SyntaxKind.PLUS:
                        return self._evaluate(left) + self._evaluate(right)
                    case SyntaxKind.MINUS:
                        return self._evaluate(left) - self._evaluate(right)
                    case SyntaxKind.STAR:
                        return self._evaluate(left) * self._evaluate(right)
                    case SyntaxKind.FORWARD_SLASH:
                        return self._evaluate(left) // self._evaluate(right)
                    case SyntaxKind.TWO_STAR:
                        return self._evaluate(left) ** self._evaluate(right)
                    case _:
                        raise UnexpectedBinaryOperatorError(
                            f"Can't recognize {operator.kind} as binary operator"
                        )
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
