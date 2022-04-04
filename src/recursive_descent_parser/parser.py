from dataclasses import dataclass
from typing import Any, Iterable, Optional
from .lexer import Lexer, SyntaxKind, Token
from abc import ABC, abstractmethod
from .errors import InvalidSyntaxTreeError, UnexpectedTokenError


class SyntaxNode(ABC):
    @abstractmethod
    def children(self) -> Iterable[Any]:
        ...

    def __init__(self) -> None:
        super().__init__()
        self.kind = ""
        self.value = None


class ExpressionSyntax(SyntaxNode):
    ...


@dataclass
class NumberExpressionSyntax(ExpressionSyntax):
    number_token: Token
    kind = SyntaxKind.NUMBER_EXPRESSION

    def children(self):
        yield self.number_token


@dataclass
class BinaryExpressionSyntax(ExpressionSyntax):
    left: ExpressionSyntax
    operator: Token
    right: ExpressionSyntax
    kind = SyntaxKind.BINARY_EXPRESSION

    def children(self):
        yield self.left
        yield self.operator
        yield self.right


@dataclass
class ParenthesizedExpression(ExpressionSyntax):
    opening_paren: Token
    expression: ExpressionSyntax
    closing_paren: Token
    kind = SyntaxKind.PARENTHESIZED_EXPRESSION

    def children(self):
        yield self.opening_paren
        yield self.expression
        yield self.closing_paren


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
        tree = self._parse_add_subtract()
        self._match(SyntaxKind.EOF)
        return SyntaxTree(tree, self.errors)

    def _parse_add_subtract(self):
        left = self._parse_multiply_divide()
        while self.current_token.kind in (
            SyntaxKind.MINUS,
            SyntaxKind.PLUS,
        ):
            operator = self._next()
            right = self._parse_multiply_divide()
            left = BinaryExpressionSyntax(left, operator, right)
        return left

    def _parse_multiply_divide(self):
        left = self._parse_primary_expression()
        while self.current_token.kind in (
            SyntaxKind.STAR,
            SyntaxKind.FORWARD_SLASH,
        ):
            operator = self._next()
            right = self._parse_primary_expression()
            left = BinaryExpressionSyntax(left, operator, right)
        return left

    def _parse_primary_expression(self) -> Any:
        if self.current_token.kind == SyntaxKind.NUMBER:
            return NumberExpressionSyntax(self._match(SyntaxKind.NUMBER))
        if self.current_token.kind == SyntaxKind.OPEN_PAREN:
            left = self._next()
            expression = self._parse_add_subtract()
            right = self._match(SyntaxKind.CLOSE_PAREN)
            return ParenthesizedExpression(left, expression, right)
        return self._match(SyntaxKind.NUMBER_EXPRESSION)
