import argparse
import os
import sys


def start() -> int:
    working_dir: str = os.getcwd()
    sys.path.append(working_dir)
    project_root: str = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_root)
    from main import main

    input_file: str = "<stdin>"
    arg_parser: argparse.ArgumentParser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="The input .ahk file for the interpreter.",
    )
    arg_parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        const=input,
        help="To run the interpreter in debug mode.",
    )
    args: argparse.Namespace = arg_parser.parse_args()
    input_file: str = args.input
    debug_mode: bool = True if args.debug is not None else False

    return main(input_file, debug_mode)


if __name__ == "__main__":
    start()
