# This project is still in development
# AHKLinux
An Interpreter for AutoHotKey on Linux **(planned only for X11)**.
- The idea of the project is to convert all the AHK Win API calls into X11 server calls.
- This does need reimplementation of the whole scripting language itself because a native/non-native compiler/interpreter doesn't exist on Linux for AHK(even with Wine, it doesn't seem to work the same way as it would on Windows).

# Features
- Language features
  - Literals
    - Number
      - Decimal
      - Hexadecimal
      - Floating points
    - String
      - Quoted
      - Unquoted (Legacy)
    - Array
      - Array indexing
    - Associative array
      - Associative array indexing through keys

  - Variables
    - Initialization
      - Initialization using ':=' operator to an expression
      - Initialization using '=' operator to an unquoted string
    - Access
      - Access from within expressions
      - Access by enclosing in '%' signs to embed into unquoted strings (Legacy)

  - Expressions
    - Arithmetic (+,-,*,/)
    - Boolean (or, and, not)
    - Ternary operator (?:)

  - Statements
    - if
    - if-else
  
  - Comments
    - Single line comment (';')
    - Multi-line comment ('/* ... */')

- Error printing
  - Better python-like error printing with proper tracebacks.
  - Errors printed to stderr rather than an alert box.

# Differences between AHK on Windows and this interpreter
- Concatenation of two strings doesn't require spaces preceeding the dot operator and the second string.
- Example:
```
a := "Hello " . "World" ; On Windows, this is the only accepted way.

a := "Hello "."World" ; But, with this interpreter, this works too!
```
- Usage of the dot operator or an object access method (square brackets) as a variable name inside '%' doesn't throw an error.
- Example:
```
/*
This line below would throw an error on Windows 
But doesn't while using this interpreter.
*/
b = %a.a% ; b would be assigned to the string value '%a.a%'
```

# Developer Instructions
## Startup Command
```
cd src/AHKLinux/
python3 init.py [options]
```

## Options
### Debug Mode
- Description
  - Prints out debug-friendly steps that the interpreter has taken. Example:
  ```
  a := 10
  a
  ```
   - This would output:
  ```
  'a' has been assigned the value 10.
  10
  ```
- Option trigger
```
python3 init.py -d
```
### Input File
- Description
  - The full path to the .ahk file that you want to interpret.

- Option trigger
```
python3 init.py -i <path_to_ahk_file>
```
- This is a **required** option.
### Help
- Description
  - Prints out a description of all the options.

- Option trigger
```
python3 init.py -h
```

# Contribution
- Code should be written in Python3 ONLY and must follow PEP8 conventions as far as possible.
- Code must be formatted using black.
- Make sure to update grammar rules in parser/parser.py while adding or removing parser parameters.
