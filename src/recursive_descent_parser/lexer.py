from .errors import UnexpectedTokenError
from .SyntaxTypes import Token, SyntaxKind


class Lexer:
    """
    Stores a stream of tokens, which can be iterated over
    """

    def __init__(self, line: str) -> None:
        self.line = line
        self.position = 0
        self.end = len(line)
        self.errors: list[Exception] = []

    def _next(self, offset=1):
        self.position += offset

    def _peek(self, offset=1):
        if self.position + offset >= self.end:
            return "\0"
        return self.line[self.position + offset]

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
            isFloat = False
            if self.current == ".":
                if self._peek().isdigit():
                    self._next()
                    while self.current.isdigit():
                        self._next()
                        isFloat = True

            if isFloat:
                value = float(self.line[start : self.position])
            else:
                value = int(self.line[start : self.position])
            return Token(
                SyntaxKind.NUMBER,
                start,
                content=self.line[start : self.position],
                value=value,
            )

        if self.current.isspace():
            start = self.position
            while self.current.isspace():
                self._next()
            return Token(SyntaxKind.SPACE, start, content=" ")

        match self.current:
            case "+":
                self._next()
                return Token(SyntaxKind.PLUS, self.position - 1, "+")
            case "-":
                self._next()
                return Token(SyntaxKind.MINUS, self.position - 1, "-")
            case "*":
                if self._peek() == "*":
                    self._next(2)
                    return Token(SyntaxKind.TWO_STAR, self.position - 2, "*")
                self._next(1)
                return Token(SyntaxKind.STAR, self.position - 1, "*")
            case "/":
                self._next()
                return Token(SyntaxKind.FORWARD_SLASH, self.position - 1, "/")
            case "(":
                self._next()
                return Token(SyntaxKind.OPEN_PAREN, self.position - 1, "(")
            case ")":
                self._next()
                return Token(SyntaxKind.CLOSE_PAREN, self.position - 1, ")")
            case "&":
                self._next()
                return Token(SyntaxKind.AND, self.position - 1, "&")
            case "|":
                self._next()
                return Token(SyntaxKind.OR, self.position - 1, "|")
            case "~":
                self._next()
                return Token(SyntaxKind.NOT, self.position - 1, "~")
            case "^":
                self._next()
                return Token(SyntaxKind.XOR, self.position - 1, "^")

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
