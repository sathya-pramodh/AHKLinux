import os
from lexer.lexer import Lexer
from parser.parser import Parser
from interpreter.interpreter import Interpreter
from base_classes.context import Context
from base_classes.symbol_table import SymbolTable


def print_result_list(results, debug_mode):
    if not isinstance(results, list):
        print(results)
        return
    for result in results:
        print_result_list(result, debug_mode)
    return


def main(input_file, debug_mode):
    if "~" in input_file:
        input_file = os.path.expanduser(input_file)
    if not os.path.isfile(input_file):
        print("File not found: '{}'.".format(input_file))
        return 1
    with open(input_file) as file:
        contents = file.read()
    if contents == "":
        print("The file '{}' is empty.".format(input_file))
        return 1
    global_symbol_table = SymbolTable()
    context = Context("<module>")
    context.symbol_table = global_symbol_table
    lexer = Lexer(contents, input_file, context)
    tokens, error = lexer.tokenize()
    if error:
        print(error.as_string())
        return 1
    parser = Parser(tokens, context)
    ast, error = parser.parse()
    if error:
        print(error.as_string())
        return 1

    interpreter = Interpreter()
    for node in ast:
        result = interpreter.visit(node.node, context)
        if result.error:
            print(result.error.as_string())
            return 1
        if isinstance(result.value, list):
            print_result_list(result.value, debug_mode)
        else:
            if debug_mode:
                print(result.value)
            elif not debug_mode and not isinstance(result.value, str):
                print(result.value)
    return 0
