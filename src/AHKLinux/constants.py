T_IDENTIFIER: str = "IDENTIFIER"
T_KEYWORD: str = "KEYWORD"
T_COMMAND: str = "COMMAND"
T_ASSIGNMENT: str = "ASSIGNMENT"
T_L_ASSIGNMENT: str = "L_ASSIGNMENT"
T_DECIMAL: str = "DECIMAL"
T_HEXADECIMAL: str = "HEXADECIMAL"
T_FLOAT: str = "FLOAT"
T_BOOLEAN: str = "BOOLEAN"
T_PLUS: str = "PLUS"
T_MINUS: str = "MINUS"
T_MULTIPLY: str = "MULTIPLY"
T_DIVIDE: str = "DIVIDE"
T_LPAREN: str = "LPAREN"
T_RPAREN: str = "RPAREN"
T_STRING: str = "STRING"
T_U_STRING: str = "U_STRING"
T_DOT: str = "DOT"
T_PERCENT: str = "PERCENT"
T_QUESTION_MARK: str = "QUESTION_MARK"
T_LSQUARE: str = "LSQUARE"
T_RSQUARE: str = "RSQUARE"
T_LCURVE: str = "LCURVE"
T_RCURVE: str = "RCURVE"
T_COMMA: str = "COMMA"
T_COLON: str = "COLON"
T_SEMICOLON: str = "SEMICOLON"
T_LCOMMENT: str = "LCOMMENT"
T_BCOMMENT_START: str = "BCOMMENT_START"
T_BCOMMENT_END: str = "BCOMMENT_END"
T_SOF: str = "SOF"
T_EOF: str = "EOF"
T_EOL: str = "EOL"
T_UNKNOWN: str = "UNKNOWN"
DIGITS: str = "0123456789"
LETTERS: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
KEYWORDS: list[str] = ["global", "and", "or", "not", "if", "else", "return"]
BOOLEANS: list[str] = ["true", "false"]
COMMANDS: list[str] = ["MsgBox"]
ESCAPE_CHARS: dict[str, str] = {"`n": "\n", "`t": "\t", "`r": "\r"}
