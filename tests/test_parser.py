from src.recursive_descent_parser.SyntaxTypes import (
    BinaryExpressionSyntax,
    NumberExpressionSyntax,
    ParenthesizedExpression,
    SyntaxKind,
    Token,
)
from src.recursive_descent_parser import SyntaxTree
import pytest


class TestParser:
    @pytest.mark.parametrize(
        "tree,output",
        [
            (SyntaxTree.generate("1 + 1"), 2),
            (SyntaxTree.generate("2 * 3 + 5"), 11),
            (SyntaxTree.generate("3 * 15 / 5 * (10 - 3)"), 63),
        ],
    )
    def test_general_evaluation(self, tree: SyntaxTree, output: int | float):
        assert tree.evaluate() == output

    @pytest.mark.parametrize(
        "tree,output",
        [
            (SyntaxTree.generate("1 -- 1"), 2),
            (SyntaxTree.generate("2 -+1 + 3"), 4),
            (SyntaxTree.generate("-(-(-2)) + 10"), 8),
            (SyntaxTree.generate("-+-+-(1)"), -1),
            (SyntaxTree.generate("10 * (-5 + 3)"), -20),
            (SyntaxTree.generate("~10 + 10 + 1"), 0),
            (SyntaxTree.generate("~1"), -2),
            (SyntaxTree.generate("~0"), -1),
        ],
    )
    def test_unary_operators(self, tree: SyntaxTree, output: int | float):
        assert tree.evaluate() == output

    @pytest.mark.parametrize(
        "tree,output",
        [
            (SyntaxTree.generate("10 / 3"), 10 / 3),
            (SyntaxTree.generate("10 / 2 / 2"), 2.5),
            (SyntaxTree.generate("10 / 2 ** 2"), 2.5),
            (SyntaxTree.generate("2 ** 2 ** 3"), 64),
            (SyntaxTree.generate("2 ** (2 ** 3)"), 256),
            (SyntaxTree.generate("1 + 5 - 10 / 4"), 3.5),
            (SyntaxTree.generate("1 | 2 + 3"), 5),
            (SyntaxTree.generate("3 & 9"), 1),
            (SyntaxTree.generate("3 & ~3"), 0),
            (SyntaxTree.generate("3 | ~3"), -1),
            (SyntaxTree.generate("3 ^ 3"), 0),
            (SyntaxTree.generate("1 * 3 ^ 3"), 0),
            (SyntaxTree.generate("2 * 3 ^ 3"), 5),
        ],
    )
    def test_binary_operators(self, tree: SyntaxTree, output: int | float):
        assert tree.evaluate() == output

    @pytest.mark.parametrize(
        "tree,output",
        [
            (SyntaxTree.generate("10(3 + 1)/4"), 10),
            (SyntaxTree.generate("2(5)"), 10),
            (SyntaxTree.generate("2**3(5)"), 40),
            (SyntaxTree.generate("2 + 5(4)"), 22),
        ],
    )
    def test_implicit_multiplication(self, tree: SyntaxTree, output: int | float):
        assert tree.evaluate() == output

    def test_parse_tree(self):
        tree = SyntaxTree.generate("3**2 + (15 - 10) / 5")
        match tree.root:
            case BinaryExpressionSyntax(
                left=BinaryExpressionSyntax(
                    left=NumberExpressionSyntax(number_token=Token(value=3)),
                    operator=Token(SyntaxKind.TWO_STAR),
                    right=NumberExpressionSyntax(number_token=Token(value=2)),
                ),
                operator=Token(kind=SyntaxKind.PLUS),
                right=BinaryExpressionSyntax(
                    left=ParenthesizedExpression(
                        expression=BinaryExpressionSyntax(
                            left=NumberExpressionSyntax(number_token=Token(value=15)),
                            operator=Token(kind=SyntaxKind.MINUS),
                            right=NumberExpressionSyntax(number_token=Token(value=10)),
                        )
                    ),
                    operator=Token(kind=SyntaxKind.FORWARD_SLASH),
                    right=NumberExpressionSyntax(number_token=Token(value=5)),
                ),
            ):
                assert tree.evaluate() == 10
            case _:
                tree.pretty_print()
                assert False
