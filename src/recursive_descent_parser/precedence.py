from .types import Token, SyntaxKind


def get_binary_operator_precedence(operator: Token):
    match operator.kind:
        case SyntaxKind.TWO_STAR:
            return 3
        case SyntaxKind.FORWARD_SLASH | SyntaxKind.STAR:
            return 2
        case SyntaxKind.PLUS | SyntaxKind.MINUS:
            return 1
        case _:
            return 0


def get_unary_operator_precendence(operator: Token):
    match operator.kind:
        case SyntaxKind.PLUS | SyntaxKind.MINUS:
            return 4
        case _:
            return 0
