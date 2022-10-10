import os
import subprocess
import unittest

import main


os.chdir(os.path.dirname(__file__))
BASE_DEBUG_CMD: str = "python3 cli.py --input {} -d"
BASE_CMD: str = "python3 cli.py --input {}"
MSGBOX_OUTPUT_FORMAT: str = (
    "MsgBox with title: '{}' and text: '{}' is being displayed.\n"
)
ASSIGN_OUTPUT_FORMAT: str = "'{}' inside '{}' has been assigned the value '{}'.\n"
KEY_ASSIGN_OUTPUT_FORMAT: str = "Key '{}' was assigned the value {}.\n"
FUNC_DECLARE_OUTPUT_FORMAT: str = "Function with name '{}' has been declared.\n"
ERROR_FORMAT: str = (
    "Traceback (most recent call last):\n File: '{}', line {}, in {}\n   {}\n{}\n"
)
TEST_FORMAT: str = "Testing unit '{}'. Press Enter whenever the message box appears"


def exec_msgbox_debug_cmd(file: str, value: int | float | str) -> tuple[str, str]:
    cmd: list[str] = BASE_DEBUG_CMD.format(file).split()
    proc: subprocess.Popen[bytes] = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate()
    expected_result: str = MSGBOX_OUTPUT_FORMAT.format(file, value)
    if stderr:
        return stderr.decode("UTF-8"), expected_result
    result: str = stdout.decode("UTF-8")
    return result, expected_result


class TestArithmetic(unittest.TestCase):
    def test_debug_add(self) -> None:
        file: str = "tests/arithmetic/add.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 30)
        self.assertEqual(result, expected_result)

    def test_add(self) -> None:
        file: str = "tests/arithmetic/add.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_subtract(self) -> None:
        file: str = "tests/arithmetic/subtract.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, -10)
        self.assertEqual(result, expected_result)

    def test_subtract(self) -> None:
        file: str = "tests/arithmetic/subtract.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_multiply(self) -> None:
        file: str = "tests/arithmetic/multiply.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 100)
        self.assertEqual(result, expected_result)

    def test_multiply(self) -> None:
        file: str = "tests/arithmetic/multiply.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_divide(self) -> None:
        file: str = "tests/arithmetic/divide.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1.0)
        self.assertEqual(result, expected_result)

    def test_divide(self) -> None:
        file: str = "tests/arithmetic/divide.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestBoolean(unittest.TestCase):
    def test_debug_and_op(self) -> None:
        file: str = "tests/boolean/and.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "true")
        self.assertEqual(result, expected_result)

    def test_and_op(self) -> None:
        file: str = "tests/boolean/and.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_or_op(self) -> None:
        file: str = "tests/boolean/or.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "false")
        self.assertEqual(result, expected_result)

    def test_or_op(self) -> None:
        file: str = "tests/boolean/or.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_not_op(self) -> None:
        file: str = "tests/boolean/not.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "true")
        self.assertEqual(result, expected_result)

    def test_not_op(self) -> None:
        file: str = "tests/boolean/not.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_ternary_op(self) -> None:
        file: str = "tests/boolean/ternary.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "This is true.")
        self.assertEqual(result, expected_result)

    def test_ternary_op(self) -> None:
        file: str = "tests/boolean/ternary.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestStrings(unittest.TestCase):
    def test_debug_declaration(self) -> None:
        file: str = "tests/string/declare.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "This is a test.")
        self.assertEqual(result, expected_result)

    def test_declaration(self) -> None:
        file: str = "tests/string/declare.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_concat(self) -> None:
        file: str = "tests/string/concat.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "Hello, World!")
        self.assertEqual(result, expected_result)

    def test_concat(self) -> None:
        file: str = "tests/string/concat.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_multi_concat(self) -> None:
        file: str = "tests/string/multi_concat.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "Hello, World!")
        self.assertEqual(result, expected_result)

    def test_multi_concat(self) -> None:
        file: str = "tests/string/multi_concat.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestArrays(unittest.TestCase):
    def test_debug_declaration(self) -> None:
        file: str = "tests/array/declare.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "[1,2,3]")
        self.assertEqual(result, expected_result)

    def test_declaration(self) -> None:
        file: str = "tests/array/declare.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_access(self) -> None:
        file: str = "tests/array/access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)

    def test_access(self) -> None:
        file: str = "tests/array/access.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_nested_access(self) -> None:
        file: str = "tests/array/nested_access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)

    def test_nested_access(self) -> None:
        file: str = "tests/array/nested_access.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestAssociativeArrays(unittest.TestCase):
    def test_debug_declaration(self) -> None:
        file: str = "tests/associative_array/declare.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "{a:1,b:2}")
        self.assertEqual(result, expected_result)

    def test_declaration(self) -> None:
        file: str = "tests/associative_array/declare.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_dot_access(self) -> None:
        file: str = "tests/associative_array/dot_access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)

    def test_dot_access(self) -> None:
        file: str = "tests/associative_array/dot_access.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_nested_dot_access(self) -> None:
        file: str = "tests/associative_array/nested_dot_access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)

    def test_nested_dot_access(self) -> None:
        file: str = "tests/associative_array/nested_dot_access.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_bracket_access(self) -> None:
        file: str = "tests/associative_array/bracket_access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)

    def test_bracket_access(self) -> None:
        file: str = "tests/associative_array/bracket_access.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_nested_bracket_access(self) -> None:
        file: str = "tests/associative_array/nested_bracket_access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)

    def test_nested_bracket_access(self) -> None:
        file: str = "tests/associative_array/nested_bracket_access.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_combined_access(self) -> None:
        file: str = "tests/associative_array/combined_access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)

    def test_combined_access(self) -> None:
        file: str = "tests/associative_array/combined_access.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_combined_alt_access(self) -> None:
        file: str = "tests/associative_array/combined_alt_access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)

    def test_combined_alt_access(self) -> None:
        file: str = "tests/associative_array/combined_alt_access.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_assign(self) -> None:
        file: str = "tests/associative_array/assign.ahk"
        cmd: list[str] = BASE_DEBUG_CMD.format(file).split()
        proc: subprocess.Popen[bytes] = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        expected_result: str = (
            ASSIGN_OUTPUT_FORMAT.format("a", "<module>", "{}")
            + KEY_ASSIGN_OUTPUT_FORMAT.format("a", "{b:1}")
            + KEY_ASSIGN_OUTPUT_FORMAT.format("b", 10)
        )
        if stderr:
            self.assertEqual(stderr.decode("UTF-8"), expected_result)
        else:
            self.assertEqual(stdout.decode("UTF-8"), expected_result)

    def test_assign(self) -> None:
        file: str = "tests/associative_array/assign.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestVariable(unittest.TestCase):
    def test_debug_assignment(self) -> None:
        file: str = "tests/variable/assignment.ahk"
        cmd: list[str] = BASE_DEBUG_CMD.format(file).split()
        proc: subprocess.Popen[bytes] = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        expected_result: str = ASSIGN_OUTPUT_FORMAT.format("a", "<module>", 10)
        if stderr:
            self.assertEqual(stderr.decode("UTF-8"), expected_result)
        else:
            result: str = stdout.decode("UTF-8")
            self.assertEqual(result, expected_result)

    def test_assignment(self) -> None:
        file: str = "tests/variable/assignment.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_expr(self) -> None:
        file: str = "tests/variable/expr.ahk"
        cmd: list[str] = BASE_DEBUG_CMD.format(file).split()
        proc: subprocess.Popen[bytes] = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        expected_result: str = (
            ASSIGN_OUTPUT_FORMAT.format("a", "<module>", 20)
            + MSGBOX_OUTPUT_FORMAT.format(file, 10.0)
            + ASSIGN_OUTPUT_FORMAT.format("a", "<module>", "[1,2,3]")
            + MSGBOX_OUTPUT_FORMAT.format(file, 1)
            + ASSIGN_OUTPUT_FORMAT.format("a", "<module>", "[[1,2,3],[4,5,6]]")
            + MSGBOX_OUTPUT_FORMAT.format(file, 1)
            + ASSIGN_OUTPUT_FORMAT.format("a", "<module>", "{a:1}")
            + MSGBOX_OUTPUT_FORMAT.format(file, 1)
            + ASSIGN_OUTPUT_FORMAT.format("a", "<module>", "{a:{b:1}}")
            + MSGBOX_OUTPUT_FORMAT.format(file, 1)
            + ASSIGN_OUTPUT_FORMAT.format("a", "<module>", "Hello, World!")
            + MSGBOX_OUTPUT_FORMAT.format(file, "Hello, World!")
            + ASSIGN_OUTPUT_FORMAT.format("a", "<module>", "Hello, World!")
            + MSGBOX_OUTPUT_FORMAT.format(file, "Hello, World!")
            + ASSIGN_OUTPUT_FORMAT.format("a", "<module>", "Hello")
            + MSGBOX_OUTPUT_FORMAT.format(file, "Hello, World!")
            + ASSIGN_OUTPUT_FORMAT.format("a", "<module>", ", World!")
            + MSGBOX_OUTPUT_FORMAT.format(file, "Hello, World!")
        )
        if stderr:
            self.assertEqual(stderr.decode("UTF-8"), expected_result)
        else:
            result: str = stdout.decode("UTF-8")
            self.assertEqual(result, expected_result)

    def test_expr(self) -> None:
        file: str = "tests/variable/expr.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_embed(self) -> None:
        file: str = "tests/variable/embed.ahk"
        cmd: str = BASE_DEBUG_CMD.format(file).split()
        proc: subprocess.Popen[bytes] = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        expected_output = (
            ASSIGN_OUTPUT_FORMAT.format("a", "<module>", 10)
            + MSGBOX_OUTPUT_FORMAT.format(file, "This is a test for embeds 10 .")
            + ASSIGN_OUTPUT_FORMAT.format(
                "a", "<module>", " This is a test for embeds 10."
            )
            + MSGBOX_OUTPUT_FORMAT.format(file, " This is a test for embeds 10.")
        )
        stdout, stderr = proc.communicate()
        if stderr:
            self.assertEqual(stderr.decode("UTF-8"), expected_output)
        else:
            self.assertEqual(stdout.decode("UTF-8"), expected_output)

    def test_embed(self) -> None:
        file: str = "tests/variable/embed.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestExpressions(unittest.TestCase):
    def test_debug_arith_expression(self) -> None:
        file: str = "tests/expressions/arith_expression.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 10.0)
        self.assertEqual(result, expected_result)

    def test_arith_expression(self) -> None:
        file: str = "tests/expressions/arith_expression.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_bool_expression(self) -> None:
        file: str = "tests/expressions/bool_expression.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "false")
        self.assertEqual(result, expected_result)

    def test_bool_expression(self) -> None:
        file: str = "tests/expressions/bool_expression.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestStatements(unittest.TestCase):
    def test_debug_if(self) -> None:
        file: str = "tests/statements/if.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "Printing in if")
        self.assertEqual(result, expected_result)

    def test_if(self) -> None:
        file: str = "tests/statements/if.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_if_else(self) -> None:
        file: str = "tests/statements/if_else.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "Printing in else")
        self.assertEqual(result, expected_result)

    def test_if_else(self) -> None:
        file: str = "tests/statements/if_else.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestFunctions(unittest.TestCase):
    def test_debug_declare(self) -> None:
        file: str = "tests/functions/declare.ahk"
        cmd: list[str] = BASE_DEBUG_CMD.format(file).split()
        proc: subprocess.Popen[bytes] = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        expected_result: str = FUNC_DECLARE_OUTPUT_FORMAT.format("func")
        if stderr:
            self.assertEqual(stderr.decode("UTF-8"), expected_result)
        self.assertEqual(stdout.decode("UTF-8"), expected_result)

    def test_declare(self) -> None:
        file: str = "tests/functions/declare.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_access(self) -> None:
        file: str = "tests/functions/access.ahk"
        cmd: list[str] = BASE_DEBUG_CMD.format(file).split()
        proc: subprocess.Popen[bytes] = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        expected_result: str = FUNC_DECLARE_OUTPUT_FORMAT.format("func") + "\n"
        if stderr:
            self.assertEqual(stderr.decode("UTF-8"), expected_result)
        self.assertEqual(stdout.decode("UTF-8"), expected_result)

    def test_access(self) -> None:
        file: str = "tests/functions/access.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_scope(self) -> None:
        file: str = "tests/functions/scope.ahk"
        cmd: list[str] = BASE_DEBUG_CMD.format(file).split()
        proc: subprocess.Popen[bytes] = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        expected_result: str = (
            ASSIGN_OUTPUT_FORMAT.format("c", "<module>", 10)
            + FUNC_DECLARE_OUTPUT_FORMAT.format("func")
            + ASSIGN_OUTPUT_FORMAT.format("c", "func", 30)
            + "\n"
            + MSGBOX_OUTPUT_FORMAT.format(file, 30)
        )
        if stderr:
            self.assertEqual(stderr.decode("UTF-8"), expected_result)
        self.assertEqual(stdout.decode("UTF-8"), expected_result)

    def test_scope(self) -> None:
        file: str = "tests/functions/scope.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestComments(unittest.TestCase):
    def test_debug_line_comment(self) -> None:
        file: str = "tests/comments/line_comment.ahk"
        cmd: list[str] = BASE_DEBUG_CMD.format(file).split()
        proc: subprocess.Popen[bytes] = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        stdout, stderr = proc.communicate()
        expected_result: str = ""
        if stderr:
            self.assertEqual(stderr.decode("UTF-8"), expected_result)
        else:
            result: str = stdout.decode("UTF-8")
            self.assertEqual(result, expected_result)

    def test_line_comment(self) -> None:
        file: str = "tests/comments/line_comment.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_block_comment(self) -> None:
        file: str = "tests/comments/block_comment.ahk"
        cmd: list[str] = BASE_DEBUG_CMD.format(file).split()
        proc: subprocess.Popen[bytes] = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        expected_result: str = ""
        if stderr:
            self.assertEqual(stderr.decode("UTF-8"), expected_result)
        else:
            result: str = stdout.decode("UTF-8")
            self.assertEqual(result, expected_result)

    def test_block_comment(self) -> None:
        file: str = "tests/comments/block_comment.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestErrors(unittest.TestCase):
    def test_div_by_zero(self) -> None:
        file: str = "tests/errors/div_by_zero.ahk"
        cmd: list[str] = BASE_CMD.format(file).split()
        proc: subprocess.Popen[bytes] = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        expected_result: str = ERROR_FORMAT.format(
            file,
            1,
            "<module>",
            "MsgBox % 10/0",
            "Runtime Error: Division by zero not allowed.\n",
        )
        self.assertEqual(stderr.decode("UTF-8"), expected_result)


if __name__ == "__main__":
    unittest.main()
