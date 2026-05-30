# RTA++ Compiler v3.0

RTA++ programlama dilini x86-64 NASM assembly'ye dönüştüren bir derleyici.

## Mimarı

```
Kaynak (.rsp) → Lexer → Tokens → Parser → AST → Code Generator → Assembly (.asm)
```

| Katman | Dosya | İşlev |
|--------|-------|-------|
| **Lexer** | `src/lexer.py` | Karakter akışını token'lara dönüştürür |
| **Parser** | `src/parser.py` | Token'lardan AST (Abstract Syntax Tree) oluşturur |
| **Code Generator** | `src/codegen.py` | AST'yi x86-64 NASM assembly'ye dönüştürür |
| **Compiler** | `src/compiler.py` | Tüm aşamaları yönetir, hata raporlaması yapar |

## Özellikler

- ✅ **Fonksiyon tanımı**: `fn name(params) { ... }`
- ✅ **Değişken bildirimi**: `let [mut] name = expr;`
- ✅ **Atama**: `name = expr;`
- ✅ **Aritmetik**: `+`, `-`, `*`, `/`, `%`
- ✅ **Karşılaştırma**: `>`, `<`, `>=`, `<=`, `==`, `!=`
- ✅ **Koşullar**: `if cond { ... } [else { ... }]`
- ✅ **Match**: `match expr { pattern => { ... } }`
- ✅ **Döngüler**: `while cond { ... }`
- ✅ **Fonksiyon çağrısı**: `name(args)`
- ✅ **String**: `String::from("...")`
- ✅ **Çıktı**: `println!("...");`
- ✅ **Yorumlar**: `// ...`
- ✅ **Modül bildirimi**: `use module::path;`
- ✅ **Gelişmiş hata mesajları**: satır ve sütun numarasıyla
- ✅ **51 test** ile doğrulama

## Kullanım

### Doğrudan (Python)

```bash
# Derleme
python compiler.py test_kodu.rsp

# Test suite
python tests/test_compiler.py

# Assembly'den çalıştırılabilir dosya oluşturma (Linux WSL)
nasm -f elf64 test_kodu.asm -o test_kodu.o
ld test_kodu.o -o test_kodu
./test_kodu
```

### Docker ile

```bash
# İmajı oluştur
docker build -t rplus-compiler .

# .rsp dosyasını derle (PowerShell)
docker run --rm -v "${PWD}:/app" rplus-compiler test_kodu.rsp

# .rsp dosyasını derle (CMD)
docker run --rm -v "%cd%:/app" rplus-compiler test_kodu.rsp

# .rsp dosyasını derle (Linux/Mac)
docker run --rm -v "$(pwd):/app" rplus-compiler test_kodu.rsp

# Testleri çalıştır
docker run --rm -v "${PWD}:/app" rplus-compiler python tests/test_compiler.py

# Assembly → Binary (Linux)
docker run --rm -v "${PWD}:/app" rplus-compiler sh -c " \
  python compiler.py test_kodu.rsp && \
  nasm -f elf64 test_kodu.asm -o test_kodu.o && \
  ld test_kodu.o -o test_kodu"

# İnteraktif shell
docker run --rm -it -v "${PWD}:/app" --entrypoint /bin/bash rplus-compiler
```

### Docker Compose ile

```bash
# Derleme
docker compose run --rm rplus-compiler test_kodu.rsp

# Tam binary oluşturma
docker compose run --rm rplus-build

# Test
docker compose run --rm rplus-test

# Shell
docker compose run --rm rplus-shell
```

## Örnek

```rust
fn fibonacci(n) {
    let mut a = 0;
    let mut b = 1;
    let mut temp = 0;

    while n > 0 {
        temp = a + b;
        a = b;
        b = temp;
        n = n - 1;
    }

    return a;
}

fn ana_fonksiyon() {
    let mut sonuc = fibonacci(10);

    match sonuc {
        55 => { println!("Fibonacci(10) = 55"); }
        0  => { println!("Hatali"); }
    }

    return sonuc;
}
```

## VS Code Desteği

`vs-code-eklenti/` klasörünü VS Code'a yükleyin:
- Sözdizimi vurgulama (syntax highlighting)
- Kod parçacıkları (snippets)
- Otomatik kapanma ve girintileme

## Lisans

MİT LİSANS
