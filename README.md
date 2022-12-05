# YARDP

Yet Another Recursive Descent Parser.

# About

Mostly a toy project to help me understand more about how parsers and compilers work. Currently(and I don't imagine this changing) this is a REPL.

Features

1. Generates an XML like Syntax Tree
2. Provides an iterator based approach to loop over lexemes
3. Understands binary operators like `/`, `*`, `+`, `-`, `**`.
4. Understands `+` and `-` unary operators
5. Support for Bitwise operators `&`, `|`, `~` and `^`
6. Can evaluate expressions
7. Operator precedence works as expected
8. `(` and `)` are allowed and so are decimals

# Implementation

Here are some of the implementation details

1. The parser supports infinite lookahead - this is a property of Recursive Descent Parsers.
2. The grammar is LL1 - this means that the output tree is the leftmost derivation of the input string and that we need just 1 lookahead to parse the input.
3. The parser presently emits "ghost" tokens - these tokens are tokens which don't exist in the input but should be - this helps simplify the error handling
4. Whitespace is preserved by the lexer but the parser currently ignores it
5. Currently, only the Concrete Syntax Tree is generated - there isn't really any reason for this other than the fact that I found this easier to implement. In theory, it shouldn't be too difficult to convert this CST to an AST.

# Examples

## A simple expression

![image](https://user-images.githubusercontent.com/10794178/161538743-5540994b-b83f-4cdd-9f70-592a4f90fffa.png)

## One with operators of different precendence

![image](https://user-images.githubusercontent.com/10794178/161538856-ca3f4bbb-f271-4036-a688-47e18ad19ce1.png)

## A more complicated expression

![image](https://user-images.githubusercontent.com/10794178/161538949-bbbedcdb-9abb-474e-849c-57d7d44af927.png)

## One with parenthesis

![image](https://user-images.githubusercontent.com/10794178/161539039-80b8074f-bef2-4e8b-be22-98c57500c9c2.png)

## One with nested parenthesis

![image](https://user-images.githubusercontent.com/10794178/161539151-8ee049bb-f550-45a9-bebe-002b052578b1.png)

## One with the power operator

![image](https://user-images.githubusercontent.com/10794178/161633558-04c54288-fb50-47b5-bd82-8204657180d1.png)

## One with errors

![image](https://user-images.githubusercontent.com/10794178/161539354-ec3530ee-69bd-4b4e-8769-f52ccf18a29d.png)

## One with no closing parenthesis

![image](https://user-images.githubusercontent.com/10794178/161539425-027ee732-9c03-41ae-840b-f970ecc45056.png)

# Run

There is one optional dependency - [termcolor](https://pypi.org/project/termcolor/) for generating colored outputs. If you don't want colored outputs, you need not install anything.

```
git clone https://github.com/TheTrio/YARDP.git
cd YARDP
python -m src.main
```

If you use poetry, you can do

```
poetry install
poetry shell
python -m src.main
```

By default, color support is disabled. To enable it, ensure that the termcolor package is installed and then run the program with the `--color` flag.

```
python -m src.main --color
```

# Linting/Testing

The tests are in the `/tests` directory. To lint the code and run the tests, do

```
poetry shell
pytest
flake8
```
