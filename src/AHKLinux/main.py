import os
import sys
from typing import Any

from base_classes.context import Context
from base_classes.symbol_table import SymbolTable
from interpreter.interpreter import Interpreter
from lexer.lexer import Lexer
from parser.parser import Parser


def print_result_list(results: list[list] | list[Any], debug_mode: bool) -> None:
    if not isinstance(results, list):
        if debug_mode:
            print(results)
        return
    for result in results:
        print_result_list(result, debug_mode)
    return


def print_error(*args: str, **kwargs: dict) -> None:
    print(*args, file=sys.stderr, **kwargs)


def main(input_file: str, debug_mode: bool) -> int:
    if "~" in input_file:
        input_file = os.path.expanduser(input_file)
    if not os.path.isfile(input_file):
        print_error("File not found: '{}'".format(input_file))
        return 1
    with open(input_file) as file:
        contents: str = file.read()
    if contents == "":
        print_error("The file '{}' is empty.".format(input_file))
        return 1
    global_symbol_table: SymbolTable = SymbolTable()
    context: Context = Context("<module>")
    context.symbol_table = global_symbol_table
    lexer = Lexer(contents, input_file, context)
    tokens, error = lexer.tokenize()
    if error:
        print_error(error.as_string())
        return 1
    parser = Parser(tokens, context)
    ast, error = parser.parse()
    if error:
        print_error(error.as_string())
        return 1

    interpreter = Interpreter()
    for node in ast:
        result = interpreter.visit(node.node, context)
        if result.error:
            print_error(result.error.as_string())
            return 1
        if isinstance(result.value, list):
            print_result_list(result.value, debug_mode)
        else:
            if debug_mode:
                print(result.value)
    return 0
