from src.token import Token, TokenType, KEYWORDS


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.line = line
        self.column = column
        super().__init__(f"[Lexer Hatası] Satır {line}, Sütun {column}: {message}")


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        while self.current < len(self.source):
            self.start = self.current
            c = self.source[self.current]
            col = self.column

            if c.isspace():
                if c == "\n":
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.current += 1
                continue

            if (
                c == "/"
                and self.current + 1 < len(self.source)
                and self.source[self.current + 1] == "/"
            ):
                self._skip_comment()
                continue

            tok = self._scan_token()
            if tok:
                self.tokens.append(tok)
            self.column += self.current - self.start

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

    def _skip_comment(self):
        while self.current < len(self.source) and self.source[self.current] != "\n":
            self.current += 1
        self.column += self.current - self.start

    def _scan_token(self) -> Token | None:
        c = self.source[self.current]
        col = self.column

        if c == '"':
            return self._string()
        if c.isdigit():
            return self._number()
        if c.isalpha() or c == "_":
            return self._identifier_or_keyword()

        self.current += 1

        if c == "+":
            return self._make_token(TokenType.PLUS, "+", col)
        if c == "-":
            return self._make_token(TokenType.MINUS, "-", col)
        if c == "*":
            return self._make_token(TokenType.STAR, "*", col)
        if c == "/":
            return self._make_token(TokenType.SLASH, "/", col)
        if c == "%":
            return self._make_token(TokenType.PERCENT, "%", col)
        if c == "(":
            return self._make_token(TokenType.LPAREN, "(", col)
        if c == ")":
            return self._make_token(TokenType.RPAREN, ")", col)
        if c == "{":
            return self._make_token(TokenType.LBRACE, "{", col)
        if c == "}":
            return self._make_token(TokenType.RBRACE, "}", col)
        if c == ";":
            return self._make_token(TokenType.SEMICOLON, ";", col)
        if c == ":":
            if self.current < len(self.source) and self.source[self.current] == ":":
                self.current += 1
                return self._make_token(TokenType.DOUBLE_COLON, "::", col)
            return self._make_token(TokenType.COLON, ":", col)
        if c == ",":
            return self._make_token(TokenType.COMMA, ",", col)

        if c == "=":
            if self.current < len(self.source) and self.source[self.current] == "=":
                self.current += 1
                return self._make_token(TokenType.EQ_EQ, "==", col)
            if self.current < len(self.source) and self.source[self.current] == ">":
                self.current += 1
                return self._make_token(TokenType.ARROW, "=>", col)
            return self._make_token(TokenType.ASSIGN, "=", col)

        if c == "!":
            if self.current < len(self.source) and self.source[self.current] == "=":
                self.current += 1
                return self._make_token(TokenType.NEQ, "!=", col)
            raise LexerError(
                "Beklenmeyen karakter '!' (belki '!=' kastettiniz?)", self.line, col
            )

        if c == ">":
            if self.current < len(self.source) and self.source[self.current] == "=":
                self.current += 1
                return self._make_token(TokenType.GTE, ">=", col)
            return self._make_token(TokenType.GT, ">", col)

        if c == "<":
            if self.current < len(self.source) and self.source[self.current] == "=":
                self.current += 1
                return self._make_token(TokenType.LTE, "<=", col)
            return self._make_token(TokenType.LT, "<", col)

        raise LexerError(f"Beklenmeyen karakter: '{c}'", self.line, col)

    def _string(self) -> Token:
        col = self.column
        self.current += 1
        result = []
        while self.current < len(self.source):
            c = self.source[self.current]
            if c == '"':
                self.current += 1
                val = "".join(result)
                return self._make_token(TokenType.STRING, val, col)
            if c == "\\" and self.current + 1 < len(self.source):
                n = self.source[self.current + 1]
                if n == "n":
                    result.append("\n")
                elif n == "t":
                    result.append("\t")
                elif n == '"':
                    result.append('"')
                elif n == "\\":
                    result.append("\\")
                else:
                    result.append(n)
                self.current += 2
                continue
            if c == "\n":
                raise LexerError("String sonlandırılmamış (satır sonu)", self.line, col)
            result.append(c)
            self.current += 1
        raise LexerError("String sonlandırılmamış (dosya sonu)", self.line, col)

    def _number(self) -> Token:
        col = self.column
        while self.current < len(self.source) and self.source[self.current].isdigit():
            self.current += 1
        val = int(self.source[self.start : self.current])
        return self._make_token(TokenType.INTEGER, val, col)

    def _identifier_or_keyword(self) -> Token:
        col = self.column
        while self.current < len(self.source) and (
            self.source[self.current].isalnum()
            or self.source[self.current] == "_"
            or self.source[self.current] == "!"
        ):
            self.current += 1
        word = self.source[self.start : self.current]
        if word == "println!":
            return self._make_token(TokenType.PRINTLN, word, col)
        tt = KEYWORDS.get(word, TokenType.IDENTIFIER)
        return self._make_token(tt, word, col)

    def _make_token(self, type_: TokenType, value: object, col: int) -> Token:
        return Token(type_, value, self.line, col)
