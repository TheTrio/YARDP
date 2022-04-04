# YARDP

Yet Another Recursive Descent Parser.

# About

Mostly a toy project to help me understand more about how parsers and compilers work. Currently(and possibly ever) this is a REPL. Features

1. Generates an XML like Syntax Tree
2. Provides an iterator based approach to loop over lexemes
3. Understands binary operators like `/`, `*`, `+`, `-`
4. Can evaluate expressions
5. Operator precedence works as expected
6. `(` and `)` are allowed

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

## One with errors

![image](https://user-images.githubusercontent.com/10794178/161539354-ec3530ee-69bd-4b4e-8769-f52ccf18a29d.png)

## One with no closing parenthesis

![image](https://user-images.githubusercontent.com/10794178/161539425-027ee732-9c03-41ae-840b-f970ecc45056.png)

# Implementation

Here are some of the implementation details

1. The parser supports infinite lookahead, although since the current grammar is so simple, this is not necessary
2. The grammar is LL1
3. The parser presently emits "ghost" tokens - these tokens are tokens which don't exist in the input but should be - this helps simplify the error handling
4. Whitespace is preserved by the lexer but the parser currently ignores it

# Run

There is only one dependency - [termcolor](https://pypi.org/project/termcolor/) for generating colored outputs. Install it, and then run

```
python src/main.py
```

If you use poetry, you can do

```
poetry install
poetry shell
python src/main.py
```
