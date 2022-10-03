import unittest
import main
import subprocess
import os


os.chdir(os.path.dirname(__file__))
BASE_DEBUG_CMD = "python3 cli.py --input {} -d"
BASE_CMD = "python3 cli.py --input {}"
MSGBOX_OUTPUT_FORMAT = "MsgBox with title: '{}' and text: '{}' is being displayed.\n"
ASSIGN_OUTPUT_FORMAT = "'{}' inside '{}' has been assigned the value {}.\n"
ERROR_FORMAT = (
    "Traceback (most recent call last):\n File: '{}', line {}, in {}\n   {}\n{}\n"
)


def exec_msgbox_debug_cmd(file, value):
    cmd = BASE_DEBUG_CMD.format(file).split()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    expected_result = MSGBOX_OUTPUT_FORMAT.format(file, value)
    if stderr:
        return stderr.decode("UTF-8"), expected_result
    result = stdout.decode("UTF-8")
    return result, expected_result


class TestArithmetic(unittest.TestCase):
    def test_debug_add(self):
        file = "tests/arithmetic/add.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 30)
        self.assertEqual(result, expected_result)

    def test_add(self):
        file = "tests/arithmetic/add.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_subtract(self):
        file = "tests/arithmetic/subtract.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, -10)
        self.assertEqual(result, expected_result)

    def test_subtract(self):
        file = "tests/arithmetic/subtract.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_multiply(self):
        file = "tests/arithmetic/multiply.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 100)
        self.assertEqual(result, expected_result)

    def test_multiply(self):
        file = "tests/arithmetic/multiply.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_divide(self):
        file = "tests/arithmetic/divide.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1.0)
        self.assertEqual(result, expected_result)

    def test_divide(self):
        file = "tests/arithmetic/divide.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestBoolean(unittest.TestCase):
    def test_debug_and_op(self):
        file = "tests/boolean/and.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "true")
        self.assertEqual(result, expected_result)

    def test_and_op(self):
        file = "tests/boolean/and.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_or_op(self):
        file = "tests/boolean/or.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "false")
        self.assertEqual(result, expected_result)

    def test_or_op(self):
        file = "tests/boolean/or.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_not_op(self):
        file = "tests/boolean/not.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "true")
        self.assertEqual(result, expected_result)

    def test_not_op(self):
        file = "tests/boolean/not.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestArrays(unittest.TestCase):
    def test_debug_declaration(self):
        file = "tests/array/declare.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "[1,2,3]")
        self.assertEqual(result, expected_result)

    def test_declaration(self):
        file = "tests/array/declare.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_access(self):
        file = "tests/array/access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)

    def test_access(self):
        file = "tests/array/access.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_nested_access(self):
        file = "tests/array/nested_access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)

    def test_nested_access(self):
        file = "tests/array/nested_access.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestAssociativeArrays(unittest.TestCase):
    def test_debug_declaration(self):
        file = "tests/associative_array/declare.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "{a:1,b:2}")
        self.assertEqual(result, expected_result)

    def test_declaration(self):
        file = "tests/associative_array/declare.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_dot_access(self):
        file = "tests/associative_array/dot_access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)

    def test_dot_access(self):
        file = "tests/associative_array/dot_access.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_nested_dot_access(self):
        file = "tests/associative_array/nested_dot_access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)

    def test_nested_dot_access(self):
        file = "tests/associative_array/nested_dot_access.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_bracket_access(self):
        file = "tests/associative_array/bracket_access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)

    def test_bracket_access(self):
        file = "tests/associative_array/bracket_access.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_nested_bracket_access(self):
        file = "tests/associative_array/nested_bracket_access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)

    def test_nested_bracket_access(self):
        file = "tests/associative_array/nested_bracket_access.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_combined_access(self):
        file = "tests/associative_array/combined_access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)

    def test_combined_access(self):
        file = "tests/associative_array/combined_access.ahk"
        self.assertEqual(main.main(file, False), 0)
    
    def test_debug_combined_alt_access(self):
        file = "tests/associative_array/combined_alt_access.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 1)
        self.assertEqual(result, expected_result)
    
    def test_combined_alt_access(self):
        file = "tests/associative_array/combined_alt_access.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestVariable(unittest.TestCase):
    def test_debug_assignment(self):
        file = "tests/variable/assignment.ahk"
        cmd = BASE_DEBUG_CMD.format(file).split()
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        expected_result = ASSIGN_OUTPUT_FORMAT.format("a", "<module>", 10)
        if stderr:
            self.assertEqual(stderr.decode("UTF-8"), expected_result)
        else:
            result = stdout.decode("UTF-8")
            self.assertEqual(result, expected_result)

    def test_assignment(self):
        file = "tests/variable/assignment.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_expr(self):
        file = "tests/variable/expr.ahk"
        cmd = BASE_DEBUG_CMD.format(file).split()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        expected_result = ASSIGN_OUTPUT_FORMAT.format(
            "a", "<module>", 20
        ) + MSGBOX_OUTPUT_FORMAT.format(file, 10.0)
        if stderr:
            self.assertEqual(stderr.decode("UTF-8"), expected_result)
        else:
            result = stdout.decode("UTF-8")
            self.assertEqual(result, expected_result)

    def test_expr(self):
        file = "tests/variable/expr.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestExpressions(unittest.TestCase):
    def test_debug_arith_expression(self):
        file = "tests/expressions/arith_expression.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, 10.0)
        self.assertEqual(result, expected_result)

    def test_arith_expression(self):
        file = "tests/expressions/arith_expression.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_bool_expression(self):
        file = "tests/expressions/bool_expression.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "false")
        self.assertEqual(result, expected_result)

    def test_bool_expression(self):
        file = "tests/expressions/bool_expression.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestStatements(unittest.TestCase):
    def test_debug_if(self):
        file = "tests/statements/if.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "Printing in if")
        self.assertEqual(result, expected_result)

    def test_if(self):
        file = "tests/statements/if.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_if_else(self):
        file = "tests/statements/if_else.ahk"
        result, expected_result = exec_msgbox_debug_cmd(file, "Printing in else")
        self.assertEqual(result, expected_result)

    def test_if_else(self):
        file = "tests/statements/if_else.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestComments(unittest.TestCase):
    def test_debug_line_comment(self):
        file = "tests/comments/line_comment.ahk"
        cmd = BASE_DEBUG_CMD.format(file).split()
        proc = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        stdout, stderr = proc.communicate()
        expected_result = ""
        if stderr:
            self.assertEqual(stderr.decode("UTF-8"), expected_result)
        else:
            result = stdout.decode("UTF-8")
            self.assertEqual(result, expected_result)

    def test_line_comment(self):
        file = "tests/comments/line_comment.ahk"
        self.assertEqual(main.main(file, False), 0)

    def test_debug_block_comment(self):
        file = "tests/comments/block_comment.ahk"
        cmd = BASE_DEBUG_CMD.format(file).split()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        expected_result = ""
        if stderr:
            self.assertEqual(stderr.decode("UTF-8"), expected_result)
        else:
            result = stdout.decode("UTF-8")
            self.assertEqual(result, expected_result)

    def test_block_comment(self):
        file = "tests/comments/block_comment.ahk"
        self.assertEqual(main.main(file, False), 0)


class TestErrors(unittest.TestCase):
    def test_div_by_zero(self):
        file = "tests/errors/div_by_zero.ahk"
        cmd = BASE_CMD.format(file).split()
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        expected_result = ERROR_FORMAT.format(
            file,
            1,
            "<module>",
            "MsgBox % 10/0",
            "Runtime Error: Division by zero not allowed.\n",
        )
        self.assertEqual(stderr.decode("UTF-8"), expected_result)


if __name__ == "__main__":
    unittest.main()
