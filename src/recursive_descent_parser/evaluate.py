from dataclasses import dataclass

from .lexer import SyntaxKind
from .errors import UnexpectedBinaryOperatorError
from .parser import SyntaxTree, ExpressionSyntax


@dataclass
class Evaluator:
    syntax_tree: SyntaxTree

    def evaluate(self) -> int:
        return self._evaluate(self.syntax_tree.root)

    def _evaluate(self, root: ExpressionSyntax) -> int:  # type: ignore
        if root.kind == SyntaxKind.NUMBER:
            return root.value  # type: ignore

        if root.kind == SyntaxKind.BINARY_EXPRESSION:
            left, operator, right = root.children()
            if operator.kind == SyntaxKind.PLUS:
                return self._evaluate(left) + self._evaluate(right)
            elif operator.kind == SyntaxKind.MINUS:
                return self._evaluate(left) - self._evaluate(right)
            elif operator.kind == SyntaxKind.STAR:
                return self._evaluate(left) * self._evaluate(right)
            elif operator.kind == SyntaxKind.FORWARD_SLASH:
                return self._evaluate(left) // self._evaluate(right)
            else:
                raise UnexpectedBinaryOperatorError(
                    f"Can't recognize {operator.kind} as binary operator"
                )
        elif root.kind == SyntaxKind.PARENTHESIZED_EXPRESSION:
            return self._evaluate(root.expression)  # type: ignore
        else:
            number_token = root.number_token  # type: ignore
            return self._evaluate(number_token)  # type: ignore
