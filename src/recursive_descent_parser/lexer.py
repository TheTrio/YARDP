from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional
from .errors import UnexpectedTokenError


class SyntaxKind(Enum):
    NUMBER = auto()
    STAR = auto()
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

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"{self.name}"


@dataclass
class Token:
    kind: SyntaxKind
    start: int
    content: Optional[str] = None
    value: Optional[int] = None

    def children(self) -> list[Any]:
        return []


class Lexer:
    """
    Stores a stream of tokens, which can be iterated over
    """

    def __init__(self, line: str) -> None:
        self.line = line
        self.position = 0
        self.end = len(line)
        self.errors: list[Exception] = []

    def _next(self):
        self.position += 1

    @property
    def current(self):
        if self.position >= self.end:
            return "\0"
        return self.line[self.position]

    def _next_token(self):
        # print(self.current)
        if self.current == "\0":
            return Token(SyntaxKind.EOF, self.position, "\0")
        if self.current.isdigit():
            start = self.position
            while self.current.isdigit():
                self._next()

            return Token(
                SyntaxKind.NUMBER,
                start,
                content=self.line[start : self.position],
                value=int(self.line[start : self.position]),
            )

        if self.current.isspace():
            start = self.position
            while self.current.isspace():
                self._next()
            return Token(SyntaxKind.SPACE, start, content=" ")

        if self.current == "+":
            self._next()
            return Token(SyntaxKind.PLUS, self.position - 1, "+")
        if self.current == "-":
            self._next()
            return Token(SyntaxKind.MINUS, self.position - 1, "-")
        if self.current == "*":
            self._next()
            return Token(SyntaxKind.STAR, self.position - 1, "*")
        if self.current == "/":
            self._next()
            return Token(SyntaxKind.FORWARD_SLASH, self.position - 1, "/")
        if self.current == "(":
            self._next()
            return Token(SyntaxKind.OPEN_PAREN, self.position - 1, "(")
        if self.current == ")":
            self._next()
            return Token(SyntaxKind.CLOSE_PAREN, self.position - 1, ")")

        self.errors.append(
            UnexpectedTokenError(f"ERROR: Bad character '{self.current}'")
        )
        self._next()
        return Token(
            SyntaxKind.INVALID, self.position - 1, self.line[self.position - 1]
        )

    def tokens(self):
        """
        Returns an iterator of all the tokens
        """
        token = Token(SyntaxKind.START, 0, "")
        while token.kind != SyntaxKind.EOF:
            token = self._next_token()
            yield token
        self.position = 0
