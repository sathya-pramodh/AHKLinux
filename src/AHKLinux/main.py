import os
from lexer.lexer import Lexer
from parser.parser import Parser
from interpreter.interpreter import Interpreter
from base_classes.context import Context
from base_classes.symbol_table import SymbolTable


def start_interpreter(contents, input_file, debug_mode):
    global_symbol_table = SymbolTable()
    context = Context("<module>")
    context.symbol_table = global_symbol_table
    lexer = Lexer(contents, input_file, context)
    tokens, error = lexer.tokenize()
    if error:
        print(error.as_string())
        if input_file != "<stdin>":
            return 1
    if len(tokens) == 0:
        return 0
    parser = Parser(tokens, context)
    ast, error = parser.parse()
    if error:
        print(error.as_string())
        if input_file != "<stdin>":
            return 1
    if len(ast) == 0:
        return 0

    interpreter = Interpreter()
    for node in ast:
        result = interpreter.visit(node.node, context)
        if result.error:
            print(result.error.as_string())
            if input_file != "<stdin>":
                return 1
        if debug_mode and not result.error:
            print(result.value)
    return 0


def main(input_file, debug_mode):
    if input_file != "<stdin>":
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
        for line in contents.strip().split("\n"):
            code = start_interpreter(line, input_file, debug_mode)
            if code == 1:
                return 1
        return 0
    else:
        try:
            while True:
                contents = input(">> ")
                code = start_interpreter(contents, input_file, debug_mode)
                if code == 1:
                    return 1
        except KeyboardInterrupt:
            return 0
