import argparse
import os
import lexer.lexer as lexer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ifile", help="The input .ahk file for the interpreter.")
    args = parser.parse_args()
    input_file = args.ifile
    if "~" in input_file:
        input_file = os.path.expanduser(input_file)
    if not os.path.isfile(input_file):
        raise FileNotFoundError("The file {} does not exist.".format(input_file))
    with open(input_file) as file:
        contents = file.read()
    lexer_class = lexer.Lexer(contents)
    token_stream = lexer_class.lex()
    for token in token_stream:
        print(token._identifier)


if __name__ == "__main__":
    main()
