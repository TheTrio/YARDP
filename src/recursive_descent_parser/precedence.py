from .types import Token, SyntaxKind


def get_binary_operator_precedence(operator: Token):
    match operator.kind:
        case SyntaxKind.TWO_STAR:
            return 5
        case SyntaxKind.FORWARD_SLASH | SyntaxKind.STAR | SyntaxKind.OPEN_PAREN:
            return 4
        case SyntaxKind.XOR:
            return 3
        case SyntaxKind.PLUS | SyntaxKind.MINUS:
            return 2
        case SyntaxKind.AND | SyntaxKind.OR:
            return 1
        case _:
            return 0


def get_unary_operator_precendence(operator: Token):
    match operator.kind:
        case SyntaxKind.PLUS | SyntaxKind.MINUS | SyntaxKind.NOT:
            return 4
        case _:
            return 0
