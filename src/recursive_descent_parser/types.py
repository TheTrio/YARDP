from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional, Iterable
from abc import ABC, abstractmethod


class SyntaxKind(Enum):
    NUMBER = auto()
    STAR = auto()
    IMPLICIT_MULTIPLY = auto()
    FORWARD_SLASH = auto()
    PLUS = auto()
    MINUS = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    SPACE = auto()
    INVALID = auto()
    EOF = auto()
    START = auto()
    NUMBER_EXPRESSION = auto()
    BINARY_EXPRESSION = auto()
    PARENTHESIZED_EXPRESSION = auto()
    TWO_STAR = auto()
    UNARY_EXPRESSION = auto()
    DOT = auto()

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"{self.name}"


class SyntaxNode(ABC):
    @abstractmethod
    def children(self) -> Iterable["SyntaxNode"]:
        ...

    def __init__(self) -> None:
        super().__init__()
        self.kind = ""
        self.value = None


@dataclass
class Token(SyntaxNode):
    kind: SyntaxKind
    start: int
    content: Optional[str] = None
    value: Optional[int | float] = None

    def children(self) -> list[Any]:
        return []


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


@dataclass
class UnaryExpressionSyntax(ExpressionSyntax):
    operator: Token
    expression: ExpressionSyntax
    kind = SyntaxKind.UNARY_EXPRESSION

    def children(self) -> Iterable[Any]:
        yield self.operator
        yield self.expression
