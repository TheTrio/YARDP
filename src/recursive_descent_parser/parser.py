from typing import Any, Optional
from .lexer import Lexer, Token
from .errors import InvalidSyntaxTreeError, UnexpectedTokenError
from .SyntaxTypes import (
    ExpressionSyntax,
    BinaryExpressionSyntax,
    NumberExpressionSyntax,
    ParenthesizedExpression,
    SyntaxKind,
    UnaryExpressionSyntax,
)
from .precedence import get_unary_operator_precendence, get_binary_operator_precedence


class SyntaxTree:
    def __init__(self, root: ExpressionSyntax, errors: list[Exception]) -> None:
        self.errors = errors
        self.root = root

    @staticmethod
    def generate(line: str) -> "SyntaxTree":
        parser = Parser(line)
        return parser.parse()

    def pretty_print(self):
        from .utils import pretty_print

        pretty_print(self)

    def evaluate(self) -> Optional[int | float]:
        if self.errors:
            raise InvalidSyntaxTreeError()
        from .evaluate import Evaluator

        evaluator = Evaluator(self)
        return evaluator.evaluate()


class Parser:
    def __init__(self, line: str) -> None:
        lexer = Lexer(line)
        self.tokens = list(lexer.tokens())
        self.errors = lexer.errors
        self.position = 0

    @property
    def current_token(self):
        if self.position >= len(self.tokens):
            return Token(SyntaxKind.EOF, start=self.position)
        return self.tokens[self.position]

    def _next(self):
        """
        Returns the current token and moves to the next one
        """
        token = self.current_token
        self.position += 1
        while self.current_token.kind == SyntaxKind.SPACE:
            self.position += 1
        return token

    def _match(self, kind: SyntaxKind):
        if self.current_token.kind == kind:
            return self._next()

        self.errors.append(
            UnexpectedTokenError(
                f"Unexpected token {self.current_token.kind} '{self.current_token.content}'. Expected {kind}"
            )
        )
        return Token(kind, self.current_token.start)

    def parse(self):
        tree = self.parse_expression()
        self._match(SyntaxKind.EOF)
        return SyntaxTree(tree, self.errors)

    def parse_expression(self, parent_precedence=0):
        # check if unary first
        precedence = get_unary_operator_precendence(self.current_token)
        if precedence > 0 and precedence >= parent_precedence:
            operator = self._next()
            operand = self.parse_expression(precedence)
            left = UnaryExpressionSyntax(operator, operand)
        else:
            left = self._parse_primary_expression()

        while True:
            precedence = get_binary_operator_precedence(self.current_token)
            if precedence == 0 or precedence <= parent_precedence:
                break

            if self.current_token.kind == SyntaxKind.OPEN_PAREN:
                # this is for the case a(b) which should be equivalent to a * b
                operator = Token(SyntaxKind.IMPLICIT_MULTIPLY, 0, "")
            else:
                operator = self._next()

            right = self.parse_expression(precedence)
            left = BinaryExpressionSyntax(left, operator, right)
        return left

    def _parse_primary_expression(self) -> Any:
        match self.current_token.kind:
            case SyntaxKind.NUMBER:
                return NumberExpressionSyntax(self._match(SyntaxKind.NUMBER))
            case SyntaxKind.OPEN_PAREN:
                left = self._next()
                expression = self.parse_expression()
                right = self._match(SyntaxKind.CLOSE_PAREN)
                return ParenthesizedExpression(left, expression, right)
            case _:
                return self._match(SyntaxKind.NUMBER_EXPRESSION)
