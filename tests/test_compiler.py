import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.lexer import Lexer
from src.parser import Parser
from src.codegen import CodeGenerator


class RPlusTestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def run(self):
        self.test_lexer_basic()
        self.test_lexer_strings()
        self.test_lexer_operators()
        self.test_parser_fn()
        self.test_parser_let()
        self.test_parser_if()
        self.test_parser_while()
        self.test_parser_match()
        self.test_parser_arithmetic()
        self.test_parser_fn_call()
        self.test_codegen_simple()
        self.test_compiler_full()

        print(f"\n{'=' * 40}")
        print(f"  TOPLAM: {self.passed + self.failed}")
        print(f"  GECEN:  {self.passed}")
        print(f"  KALAN:  {self.failed}")
        print(f"{'=' * 40}")
        return self.failed == 0

    def assert_eq(self, actual, expected, msg=""):
        if actual != expected:
            self.failed += 1
            print(f"  [FAIL] {msg}")
            print(f"    Beklenen: {expected!r}")
            print(f"    Alinan:   {actual!r}")
        else:
            self.passed += 1
            print(f"  [PASS] {msg}")

    def assert_contains(self, text, substring, msg=""):
        if substring in text:
            self.passed += 1
            print(f"  [PASS] {msg}")
        else:
            self.failed += 1
            print(f"  [FAIL] {msg}")
            print(f"    Aranan:  {substring!r}")
            print(f"    Iceride: {text[:200]!r}")

    def tokenize(self, source):
        lexer = Lexer(source)
        return lexer.tokenize()

    def parse(self, source):
        tokens = self.tokenize(source)
        parser = Parser(tokens)
        return parser.parse()

    def compile(self, source):
        tokens = self.tokenize(source)
        parser = Parser(tokens)
        ast = parser.parse()
        cg = CodeGenerator()
        return cg.generate(ast)

    def test_lexer_basic(self):
        print("\n--- Lexer: Temel ---")
        tokens = self.tokenize("fn main() { return 42; }")
        types = [t.type.name for t in tokens]
        self.assert_eq("FN" in types, True, "fn tokeni")
        self.assert_eq("IDENTIFIER" in types, True, "identifier tokeni")
        self.assert_eq("LPAREN" in types, True, "( tokeni")
        self.assert_eq("INTEGER" in types, True, "integer tokeni")

    def test_lexer_strings(self):
        print("\n--- Lexer: String ---")
        tokens = self.tokenize(r'let x = "hello world";')
        types = [t.type.name for t in tokens]
        values = [t.value for t in tokens]
        self.assert_eq("STRING" in types, True, "string tokeni")
        self.assert_eq("hello world" in values, True, "string degeri")

    def test_lexer_operators(self):
        print("\n--- Lexer: Operatorler ---")
        tokens = self.tokenize("+ - * / % == != > < >= <= => ::")
        types = [t.type.name for t in tokens]
        checks = [
            "PLUS",
            "MINUS",
            "STAR",
            "SLASH",
            "PERCENT",
            "EQ_EQ",
            "NEQ",
            "GT",
            "LT",
            "GTE",
            "LTE",
            "ARROW",
            "DOUBLE_COLON",
        ]
        for op in checks:
            self.assert_eq(op in types, True, f"{op} tokeni")

    def test_parser_fn(self):
        print("\n--- Parser: Fonksiyon ---")
        ast = self.parse("fn test(a, b) { return a; }")
        self.assert_eq(len(ast.functions), 1, "1 fonksiyon")
        fn = ast.functions[0]
        self.assert_eq(fn.name, "test", "fonksiyon adi")
        self.assert_eq(fn.params, ["a", "b"], "parametreler")
        self.assert_eq(len(fn.body), 1, "govdede 1 ifade")

    def test_parser_let(self):
        print("\n--- Parser: Let ---")
        ast = self.parse("fn f() { let mut x = 5; let y = 10; }")
        fn = ast.functions[0]
        self.assert_eq(len(fn.body), 2, "2 let ifadesi")
        from src.ast import LetDecl

        self.assert_eq(isinstance(fn.body[0], LetDecl), True, "let decl")
        self.assert_eq(fn.body[0].name, "x", "degisken adi x")
        self.assert_eq(fn.body[0].mutable, True, "mut")
        self.assert_eq(fn.body[1].name, "y", "degisken adi y")

    def test_parser_if(self):
        print("\n--- Parser: If ---")
        ast = self.parse("fn f() { if x > 5 { return 1; } else { return 0; } }")
        fn = ast.functions[0]
        from src.ast import If

        self.assert_eq(isinstance(fn.body[0], If), True, "if ifadesi")

    def test_parser_while(self):
        print("\n--- Parser: While ---")
        ast = self.parse("fn f() { while x < 10 { x = x + 1; } }")
        fn = ast.functions[0]
        from src.ast import While

        self.assert_eq(isinstance(fn.body[0], While), True, "while ifadesi")

    def test_parser_match(self):
        print("\n--- Parser: Match ---")
        source = """fn f() {
            match x {
                1 => { return 10; }
                2 => { return 20; }
            }
        }"""
        ast = self.parse(source)
        fn = ast.functions[0]
        from src.ast import Match

        self.assert_eq(isinstance(fn.body[0], Match), True, "match ifadesi")
        self.assert_eq(len(fn.body[0].arms), 2, "2 match kolu")

    def test_parser_arithmetic(self):
        print("\n--- Parser: Aritmetik ---")
        ast = self.parse("fn f() { let x = a + b * c - d; }")
        from src.ast import LetDecl, Binary, Ident

        expr = ast.functions[0].body[0].initializer
        self.assert_eq(isinstance(expr, Binary), True, "binary ifade")
        self.assert_eq(expr.op, "-", "en distaki operator")

    def test_parser_fn_call(self):
        print("\n--- Parser: Fonksiyon Cagrisi ---")
        ast = self.parse("fn f() { x = foo(1, 2); }")
        from src.ast import Assign, Call

        assign = ast.functions[0].body[0]
        self.assert_eq(isinstance(assign, Assign), True, "assign ifadesi")
        self.assert_eq(isinstance(assign.value, Call), True, "fonksiyon cagrisi")
        self.assert_eq(assign.value.callee, "foo", "callee adi")
        self.assert_eq(len(assign.value.args), 2, "2 arguman")

    def test_codegen_simple(self):
        print("\n--- Codegen: Basit Fonksiyon ---")
        asm = self.compile("fn main() { return 42; }")
        self.assert_contains(asm, "main:", "fonksiyon labeli")
        self.assert_contains(asm, "mov eax, 42", "return degeri")
        self.assert_contains(asm, "ret", "return talimati")
        self.assert_contains(asm, "_start:", "giris noktasi")
        self.assert_contains(asm, "syscall", "syscall")

    def test_compiler_full(self):
        print("\n--- Compiler: Tam Program ---")
        source = """
        fn topla(a, b) {
            let mut sonuc = 0;
            sonuc = a + b;
            return sonuc;
        }

        fn main() {
            let mut x = 0;
            x = topla(5, 3);
            if x > 0 {
                println!("Pozitif");
            } else {
                println!("Negatif");
            }
            return x;
        }
        """
        asm = self.compile(source)
        checks = [
            "topla:",
            "main:",
            "mov [rbp-",
            "add eax",
            "call topla",
            "cmp eax, 0",
            "je .else_",
            "syscall",
        ]
        for c in checks:
            self.assert_contains(asm, c, f"assembly'de {c} bulundu")


if __name__ == "__main__":
    runner = RPlusTestRunner()
    success = runner.run()
    sys.exit(0 if success else 1)
