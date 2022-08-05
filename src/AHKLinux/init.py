import os
import sys
import argparse


def start():
    working_dir = os.getcwd()
    sys.path.append(working_dir)
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_root)
    from main import main

    input_file = "<stdin>"
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-i",
        nargs="?",
        help="The input .ahk file for the interpreter.",
    )
    arg_parser.add_argument(
        "-d",
        action="store_const",
        const=input,
        help="To run the interpreter in debug mode.",
    )
    args = arg_parser.parse_args()
    input_file = args.i if args.i is not None else input_file
    debug_mode = True if args.d is not None else False

    return main(input_file, debug_mode)


if __name__ == "__main__":
    start()
