import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.compiler import RPlusCompiler


tests = [
    ("Boş dosya", ""),
    ("Sadece yorum", "// bu bir yorum"),
    ("Sadece use", "use std::test;"),
    ("Boş fonksiyon", "fn foo() {}"),
    ("İç içe if", "fn f() { if 1 { if 0 { return 1; } } return 0; }"),
    ("Karmaşık aritmetik", "fn f() { let x = (1 + 2) * 3 - 4 / 2; return x; }"),
    ("Eşitlik", "fn f(a, b) { if a == b { return 1; } if a != b { return 0; } }"),
    ("true/false", "fn f() { let a = true; let b = false; return 0; }"),
    ("String::from", 'fn f() { let s = String::from("test"); return 0; }'),
    (
        "while döngüsü",
        "fn f() { let mut x = 0; while x < 10 { x = x + 1; } return x; }",
    ),
    ("match", "fn f() { match 5 { 5 => { return 1; } 0 => { return 0; } } }"),
]

passed = 0
failed = 0

for name, src in tests:
    try:
        c = RPlusCompiler(src, name)
        asm = c.compile()
        lines = asm.strip().split("\n")
        lbl = f"[OK] {name} -> {len(lines)} satir, {len(asm)} byte"
        print(lbl)
        passed += 1
    except Exception as e:
        print(f"[FAIL] {name}: {e}")
        failed += 1

print(f"\n{passed} gecti, {failed} kaldi")
sys.exit(0 if failed == 0 else 1)
