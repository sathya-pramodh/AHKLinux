from ply.lex import lex


def main(contents):
    reserved = {
        "if": "IF",
        "else": "ELSE",
        "global": "GLOBAL",
        "and": "AND",
        "or": "OR",
        "not": "NOT",
    }
    tokens = [
        "KEYWORD",
        "PLUS",
        "MINUS",
        "MULTIPLY",
        "DIVIDE",
        "LPAREN",
        "RPAREN",
        "LBRACE",
        "RBRACE",
        "VARIABLE",
        "DECIMAL",
        "HEXADECIMAL",
        "FLOATING",
        "ASSIGNMENT",
        "STRING",
        "SINGLE_COMMENT",
        "MULTI_COMMENT",
        "LESS",
        "LESS_EQUAL",
        "GREATER",
        "GREATER_EQUAL",
        "EQUAL",
        "NOT_EQUAL",
    ] + list(reserved.values())

    t_ignore = " "
    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_MULTIPLY = r"\*"
    t_DIVIDE = r"/"
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_LBRACE = r"{"
    t_RBRACE = r"}"
    t_FLOATING = r"\d+.\d+"
    t_HEXADECIMAL = r"0x\d[^\.]"
    t_DECIMAL = r"\d+[^.]"
    t_ASSIGNMENT = r":="
    t_STRING = r'".+"'
    t_LESS = r"<"
    t_LESS_EQUAL = r"<="
    t_GREATER = r">"
    t_GREATER_EQUAL = r">="
    t_EQUAL = r"=="
    t_NOT_EQUAL = r"!="

    def t_SINGLE_COMMENT(t):
        r";.+"
        pass

    def t_MULTI_COMMENT(t):
        r"/\*\n[\s\S]*\n\*/"
        pass

    def t_VARIABLE(t):
        r"[a-zA-Z_$][a-zA-Z_$0-9]*"
        t.type = reserved.get(t.value, "VARIABLE")
        return t

    def t_ignore_new_line(t):
        r"\n+"
        t.lexer.lineno += t.value.count("\n")

    def t_error(t):
        t.lexer.skip(1)
        print(f"Value error {t.value[0]!r} at line {t.lineno}")

    lexer = lex()
    lexer.input(contents)
    token_stream = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        token_stream.append(tok)
    return token_stream
