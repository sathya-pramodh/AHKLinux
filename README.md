# AHKLinux
An Interpreter for AutoHotKey on Linux

# Developer Instructions
## Startup Command
```
python3 init.py
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
