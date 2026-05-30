from src.token import Token, TokenType
from src.ast import (
    Program,
    Stmt,
    FnDef,
    LetDecl,
    Assign,
    If,
    Match,
    MatchArm,
    While,
    Return,
    ExprStmt,
    Println,
    Use,
    Block,
    Expr,
    Integer,
    StringExpr,
    BoolExpr,
    Ident,
    Binary,
    Unary,
    Call,
)


class ParseError(Exception):
    def __init__(self, message: str, token: Token):
        self.line = token.line
        self.column = token.column
        super().__init__(
            f"[Parse Hatası] Satır {token.line}, Sütun {token.column}: {message}"
        )


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def previous(self) -> Token:
        return self.tokens[self.pos - 1]

    def advance(self) -> Token:
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    def check(self, *types: TokenType) -> bool:
        return self.peek().type in types

    def match(self, *types: TokenType) -> Token | None:
        if self.peek().type in types:
            return self.advance()
        return None

    def expect(self, type_: TokenType, msg: str = "") -> Token:
        if self.peek().type == type_:
            return self.advance()
        t = self.peek()
        raise ParseError(
            msg or f"Beklenen: {type_.name}, bulunan: {t.type.name} ({t.value})", t
        )

    def parse(self) -> Program:
        program = Program()
        while self.peek().type != TokenType.EOF:
            if self.peek().type == TokenType.USE:
                program.globals.append(self._parse_use())
            elif self.peek().type == TokenType.FN:
                program.functions.append(self._parse_fn())
            else:
                raise ParseError(f"Beklenmeyen üst seviye ifade", self.peek())
        return program

    def _parse_use(self) -> Stmt:
        tok = self.expect(TokenType.USE)
        parts = []
        while self.peek().type in (TokenType.IDENTIFIER, TokenType.DOUBLE_COLON):
            if self.peek().type == TokenType.DOUBLE_COLON:
                self.advance()
            else:
                parts.append(self.advance().value)
        self.expect(TokenType.SEMICOLON, "';' bekleniyor (use deyimi)")
        return Use(module="::".join(parts), line=tok.line)

    def _parse_fn(self) -> FnDef:
        tok = self.expect(TokenType.FN)
        name = self.expect(TokenType.IDENTIFIER, "Fonksiyon adı bekleniyor").value
        self.expect(TokenType.LPAREN, "'(' bekleniyor")
        params = []
        if self.peek().type == TokenType.IDENTIFIER:
            params.append(self.advance().value)
            while self.match(TokenType.COMMA):
                params.append(
                    self.expect(TokenType.IDENTIFIER, "Parametre adı bekleniyor").value
                )
        self.expect(TokenType.RPAREN, "')' bekleniyor")
        body = self._parse_block()
        return FnDef(name=name, params=params, body=body, line=tok.line)

    def _parse_block(self) -> list[Stmt]:
        self.expect(TokenType.LBRACE, "'{' bekleniyor")
        stmts = []
        while self.peek().type not in (TokenType.RBRACE, TokenType.EOF):
            stmts.append(self._parse_stmt())
        self.expect(TokenType.RBRACE, "'}' bekleniyor")
        return stmts

    def _parse_stmt(self) -> Stmt:
        tok = self.peek()
        if tok.type == TokenType.LET:
            return self._parse_let()
        if tok.type == TokenType.IF:
            return self._parse_if()
        if tok.type == TokenType.MATCH:
            return self._parse_match()
        if tok.type == TokenType.WHILE:
            return self._parse_while()
        if tok.type == TokenType.RETURN:
            return self._parse_return()
        if tok.type == TokenType.PRINTLN:
            return self._parse_println()
        if tok.type == TokenType.LBRACE:
            return Block(statements=self._parse_block())
        return self._parse_expr_or_assign()

    def _parse_let(self) -> Stmt:
        tok = self.expect(TokenType.LET)
        mutable = self.match(TokenType.MUT) is not None
        name = self.expect(TokenType.IDENTIFIER, "Değişken adı bekleniyor").value
        self.expect(TokenType.ASSIGN, "'=' bekleniyor")
        expr = self._parse_expr()
        self.expect(TokenType.SEMICOLON, "';' bekleniyor")
        return LetDecl(name=name, mutable=mutable, initializer=expr, line=tok.line)

    def _parse_if(self) -> Stmt:
        tok = self.expect(TokenType.IF)
        cond = self._parse_expr()
        then_body = self._parse_block()
        else_body = []
        if self.match(TokenType.ELSE):
            if self.peek().type == TokenType.IF:
                wrapped = If(
                    condition=None, then_body=[self._parse_if()], line=tok.line
                )
                else_body = [wrapped]
            else:
                else_body = self._parse_block()
        return If(
            condition=cond, then_body=then_body, else_body=else_body, line=tok.line
        )

    def _parse_match(self) -> Stmt:
        tok = self.expect(TokenType.MATCH)
        expr = self._parse_expr()
        self.expect(TokenType.LBRACE, "'{' bekleniyor")
        arms = []
        while (
            self.peek().type != TokenType.RBRACE and self.peek().type != TokenType.EOF
        ):
            val = self.expect(TokenType.INTEGER, "match kolunda sayı bekleniyor").value
            self.expect(TokenType.ARROW, "'=>' bekleniyor")
            body = (
                self._parse_block()
                if self.peek().type == TokenType.LBRACE
                else [self._parse_stmt()]
            )
            arms.append(MatchArm(value=val, body=body))
        self.expect(TokenType.RBRACE, "'}' bekleniyor")
        return Match(expr=expr, arms=arms, line=tok.line)

    def _parse_while(self) -> Stmt:
        tok = self.expect(TokenType.WHILE)
        cond = self._parse_expr()
        body = self._parse_block()
        return While(condition=cond, body=body, line=tok.line)

    def _parse_return(self) -> Stmt:
        tok = self.expect(TokenType.RETURN)
        if self.peek().type == TokenType.SEMICOLON:
            self.advance()
            return Return(value=None, line=tok.line)
        expr = self._parse_expr()
        self.expect(TokenType.SEMICOLON, "';' bekleniyor")
        return Return(value=expr, line=tok.line)

    def _parse_println(self) -> Stmt:
        tok = self.expect(TokenType.PRINTLN)
        self.expect(TokenType.LPAREN, "'(' bekleniyor")
        fmt = self.expect(TokenType.STRING, "String ifadesi bekleniyor").value
        args = []
        while self.match(TokenType.COMMA):
            args.append(self._parse_expr())
        self.expect(TokenType.RPAREN, "')' bekleniyor")
        self.expect(TokenType.SEMICOLON, "';' bekleniyor")
        return Println(format_str=fmt, args=args, line=tok.line)

    def _parse_expr_or_assign(self) -> Stmt:
        tok = self.peek()
        if tok.type == TokenType.IDENTIFIER:
            name = tok.value
            save = self.pos
            self.advance()
            if self.peek().type == TokenType.ASSIGN:
                self.advance()
                expr = self._parse_expr()
                self.expect(TokenType.SEMICOLON, "';' bekleniyor")
                return Assign(name=name, value=expr, line=tok.line)
            self.pos = save
        expr = self._parse_expr()
        self.expect(TokenType.SEMICOLON, "';' bekleniyor")
        return ExprStmt(expr=expr, line=tok.line)

    # --- Expression parsing (recursive descent, operator precedence) ---

    def _parse_expr(self) -> Expr:
        return self._parse_equality()

    def _parse_equality(self) -> Expr:
        left = self._parse_comparison()
        while self.match(TokenType.EQ_EQ, TokenType.NEQ):
            op = self.previous().value
            right = self._parse_comparison()
            left = Binary(op=op, left=left, right=right)
        return left

    def _parse_comparison(self) -> Expr:
        left = self._parse_addition()
        while self.match(TokenType.GT, TokenType.LT, TokenType.GTE, TokenType.LTE):
            op = self.previous().value
            right = self._parse_addition()
            left = Binary(op=op, left=left, right=right)
        return left

    def _parse_addition(self) -> Expr:
        left = self._parse_term()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous().value
            right = self._parse_term()
            left = Binary(op=op, left=left, right=right)
        return left

    def _parse_term(self) -> Expr:
        left = self._parse_unary()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.previous().value
            right = self._parse_unary()
            left = Binary(op=op, left=left, right=right)
        return left

    def _parse_unary(self) -> Expr:
        if self.match(TokenType.MINUS):
            op = self.previous().value
            right = self._parse_unary()
            return Unary(op=op, operand=right)
        return self._parse_primary()

    def _parse_primary(self) -> Expr:
        tok = self.advance()
        if tok.type == TokenType.INTEGER:
            return Integer(value=tok.value)
        if tok.type == TokenType.STRING:
            return StringExpr(value=tok.value)
        if tok.type == TokenType.TRUE:
            return BoolExpr(value=True)
        if tok.type == TokenType.FALSE:
            return BoolExpr(value=False)
        if tok.type == TokenType.IDENTIFIER:
            name = tok.value
            while self.peek().type == TokenType.DOUBLE_COLON:
                self.advance()
                part = self.expect(
                    TokenType.IDENTIFIER, "Path'de isim bekleniyor"
                ).value
                name += "::" + part
            if self.peek().type == TokenType.LPAREN:
                self.advance()
                args = []
                if self.peek().type != TokenType.RPAREN:
                    args.append(self._parse_expr())
                    while self.match(TokenType.COMMA):
                        args.append(self._parse_expr())
                self.expect(TokenType.RPAREN, "')' bekleniyor")
                return Call(callee=name, args=args)
            return Ident(name=name)
        if tok.type == TokenType.LPAREN:
            expr = self._parse_expr()
            self.expect(TokenType.RPAREN, "')' bekleniyor")
            return expr
        raise ParseError(f"Beklenmeyen token: {tok.type.name} ('{tok.value}')", tok)
