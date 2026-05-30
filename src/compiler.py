import sys
import os

from src.lexer import Lexer, LexerError
from src.parser import Parser, ParseError
from src.codegen import CodeGenerator, CodegenError


class CompilerError(Exception):
    pass


class RPlusCompiler:
    def __init__(self, source: str, filename: str = "<giris>"):
        self.source = source
        self.filename = filename

    def compile(self) -> str:
        lexer = Lexer(self.source)
        try:
            tokens = lexer.tokenize()
        except LexerError as e:
            raise CompilerError(str(e))

        parser = Parser(tokens)
        try:
            ast = parser.parse()
        except ParseError as e:
            raise CompilerError(str(e))

        cg = CodeGenerator()
        try:
            assembly = cg.generate(ast)
        except CodegenError as e:
            raise CompilerError(str(e))

        return assembly


def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("  SENTINEL COMPANY - R+ COMPILER v3.0")
        print("  Kullanim: python compiler.py <dosya.rsp>")
        print("  Ornek:    python compiler.py test_kodu.rsp")
        print("=" * 60)
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"[HATA] Dosya bulunamadi: {input_file}")
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8") as f:
        source = f.read()

    compiler = RPlusCompiler(source, input_file)
    try:
        assembly = compiler.compile()
    except CompilerError as e:
        print(f"\n[DERLEME HATASI]")
        print(f"  {e}")
        sys.exit(1)

    output_file = os.path.splitext(input_file)[0] + ".asm"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(assembly)

    print("\n" + "=" * 60)
    print(f"  [OK] R+ v3.0 DERLEME BASARILI!")
    print(f"  [+] Kaynak:   {input_file}")
    print(f"  [+] Cikti:    {output_file}")
    print(f"  [+] Satir:    {len(source.splitlines())} satir kaynak")
    print(f"  [+] Boyut:    {len(assembly)} byte assembly")
    print("=" * 60)


if __name__ == "__main__":
    main()
