from typing import Any, Optional
from .lexer import Lexer, Token
from .errors import InvalidSyntaxTreeError, UnexpectedTokenError
from .types import (
    ExpressionSyntax,
    BinaryExpressionSyntax,
    NumberExpressionSyntax,
    ParenthesizedExpression,
    SyntaxKind,
)


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

    def evaluate(self) -> Optional[int]:
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

    @staticmethod
    def _get_binary_operator_precedence(operator: Token):
        match operator.kind:
            case SyntaxKind.TWO_STAR:
                return 3
            case SyntaxKind.FORWARD_SLASH | SyntaxKind.STAR:
                return 2
            case SyntaxKind.PLUS | SyntaxKind.MINUS:
                return 1
            case _:
                return 0

    def parse_expression(self, parent_precedence=0):
        left = self._parse_primary_expression()

        while True:
            precedence = Parser._get_binary_operator_precedence(self.current_token)
            if precedence == 0 or precedence <= parent_precedence:
                break
            operator = self._next()
            right = self.parse_expression()
            left = BinaryExpressionSyntax(left, operator, right)
        return left

    def _parse_primary_expression(self) -> Any:
        if self.current_token.kind == SyntaxKind.NUMBER:
            return NumberExpressionSyntax(self._match(SyntaxKind.NUMBER))
        if self.current_token.kind == SyntaxKind.OPEN_PAREN:
            left = self._next()
            expression = self.parse_expression()
            right = self._match(SyntaxKind.CLOSE_PAREN)
            return ParenthesizedExpression(left, expression, right)
        return self._match(SyntaxKind.NUMBER_EXPRESSION)
