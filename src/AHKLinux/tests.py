import unittest
import main
import subprocess

BASE_DEBUG_CMD = "python3 cli.py --input {} -d"
BASE_CMD = "python3 cli.py --input {}"
MSGBOX_OUTPUT_FORMAT = "MsgBox with title: '{}' and text: '{}' is being displayed.\n"
ERROR_FORMAT = (
    "Traceback (most recent call last):\n File: '{}', line {}, in {}\n   {}\n{}\n"
)


class TestArithmetic(unittest.TestCase):
    def test_debug_add(self):
        file = "tests/arithmetic/add.ahk"
        debug_mode = True
        self.assertEqual(main.main(file, debug_mode), 0)
        cmd = BASE_DEBUG_CMD.format(file).split()
        result = subprocess.check_output(cmd).decode("UTF-8")
        expected_result = MSGBOX_OUTPUT_FORMAT.format(file, 30)
        self.assertEqual(result, expected_result)

    def test_add(self):
        file = "tests/arithmetic/add.ahk"
        debug_mode = False
        self.assertEqual(main.main(file, debug_mode), 0)

    def test_debug_subtract(self):
        file = "tests/arithmetic/subtract.ahk"
        debug_mode = True
        self.assertEqual(main.main(file, debug_mode), 0)
        cmd = BASE_DEBUG_CMD.format(file).split()
        result = subprocess.check_output(cmd).decode("UTF-8")
        expected_result = MSGBOX_OUTPUT_FORMAT.format(file, -10)
        self.assertEqual(result, expected_result)

    def test_subtract(self):
        file = "tests/arithmetic/subtract.ahk"
        debug_mode = False
        self.assertEqual(main.main(file, debug_mode), 0)

    def test_debug_multiply(self):
        file = "tests/arithmetic/multiply.ahk"
        debug_mode = True
        self.assertEqual(main.main(file, debug_mode), 0)
        cmd = BASE_DEBUG_CMD.format(file).split()
        result = subprocess.check_output(cmd).decode("UTF-8")
        expected_result = MSGBOX_OUTPUT_FORMAT.format(file, 100)
        self.assertEqual(result, expected_result)

    def test_multiply(self):
        file = "tests/arithmetic/multiply.ahk"
        debug_mode = False
        self.assertEqual(main.main(file, debug_mode), 0)

    def test_debug_divide(self):
        file = "tests/arithmetic/divide.ahk"
        debug_mode = True
        self.assertEqual(main.main(file, debug_mode), 0)
        cmd = BASE_DEBUG_CMD.format(file).split()
        result = subprocess.check_output(cmd).decode("UTF-8")
        expected_result = MSGBOX_OUTPUT_FORMAT.format(file, 1.0)
        self.assertEqual(result, expected_result)

    def test_divide(self):
        file = "tests/arithmetic/divide.ahk"
        debug_mode = False
        self.assertEqual(main.main(file, debug_mode), 0)

    def test_div_by_zero(self):
        file = "tests/errors/div_by_zero.ahk"
        debug_mode = False
        self.assertEqual(main.main(file, debug_mode), 1)
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
