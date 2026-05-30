from src.ast import *
from typing import Optional


class CodegenError(Exception):
    def __init__(self, message: str, line: int = 0):
        parts = ["[Codegen Hatasi]"]
        if line:
            parts.append(f"Satir {line}:")
        parts.append(message)
        super().__init__(" ".join(parts))


class CodeGenerator:
    def __init__(self):
        self.output = []
        self.label_count = 0
        self.strings = {}
        self.functions = {}
        self.current_fn = None
        self.fn_var_offsets = {}
        self.exit_labels = {}
        self.has_return = False

    def new_label(self, prefix: str = "L") -> str:
        self.label_count += 1
        return f".{prefix}_{self.label_count}"

    def add_string(self, s: str) -> str:
        for lbl, val in self.strings.items():
            if val == s:
                return lbl
        lbl = f"str_{len(self.strings)}"
        self.strings[lbl] = s
        return lbl

    def generate(self, program: Program) -> str:
        self.output = []
        self.output.append("; ========================================================")
        self.output.append("; SENTINEL COMPANY - R+ COMPILER v3.0")
        self.output.append("; LISANS: SGU OZEL YAZILIM")
        self.output.append("; MIMARI: Lexer -> Parser (AST) -> Code Generator (NASM)")
        self.output.append("; ========================================================")
        self.output.append("")

        for use_stmt in program.globals:
            if isinstance(use_stmt, Use):
                self.output.append(f"; [Modul]: {use_stmt.module}")

        self.output.append("")

        for fn in program.functions:
            self.functions[fn.name] = fn

        if program.functions:
            self.output.append("section .text")
            self.output.append("global _start")
            self.output.append("")
            self._generate_start(program)
        else:
            self.output.append("section .text")
            self.output.append("")
        for fn in program.functions:
            self._generate_fn(fn)

        if self.strings:
            self.output.append("")
            self.output.append("section .data")
            for lbl, val in self.strings.items():
                encoded = (
                    val.replace("'", "\\'").replace("\n", "\\n").replace("\t", "\\t")
                )
                self.output.append(f"    {lbl} db '{encoded}', 0")

        return "\n".join(self.output)

    def _generate_start(self, program: Program):
        if not program.functions:
            return
        entry = None
        for fn in program.functions:
            if fn.name == "main" or fn.name == "ana_fonksiyon":
                entry = fn
                break
        if not entry:
            entry = program.functions[0]

        self.output.append("_start:")
        self.output.append("    ; Program giris noktasi")
        self.output.append(f"    call {entry.name}")
        self.output.append("    mov edi, eax        ; donus degeri => exit kodu")
        self.output.append("    mov eax, 60         ; sys_exit")
        self.output.append("    syscall")
        self.output.append("")

    def _generate_fn(self, fn: FnDef):
        self.current_fn = fn
        self.fn_var_offsets[fn.name] = {}
        self.has_return = False
        exit_label = self.new_label(f"{fn.name}_exit")
        self.exit_labels[fn.name] = exit_label

        for p in fn.params:
            offset = 8
            self.fn_var_offsets[fn.name][p] = offset

        self.output.append(f"{fn.name}:")
        self.output.append("    push rbp")
        self.output.append("    mov rbp, rsp")
        self.output.append("    sub rsp, 256        ; stack frame")

        for i, p in enumerate(fn.params):
            regs = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
            if i < len(regs):
                self.output.append(
                    f"    mov [rbp-{self.fn_var_offsets[fn.name][p]}], {regs[i]}"
                )

        for stmt in fn.body:
            self._generate_stmt(stmt)

        self.output.append(f"{exit_label}:")
        self.output.append("    mov rsp, rbp")
        self.output.append("    pop rbp")
        self.output.append("    ret")
        self.output.append("")

    def _get_var_offset(self, name: str) -> int:
        fn = self.current_fn
        if fn and name in self.fn_var_offsets.get(fn.name, {}):
            return self.fn_var_offsets[fn.name][name]
        for fn_name, offsets in self.fn_var_offsets.items():
            if name in offsets:
                return offsets[name]
        offset = len(self.fn_var_offsets.get(self.current_fn.name, {})) * 8 + 8
        self.fn_var_offsets[self.current_fn.name][name] = offset
        return offset

    def _alloc_var(self, name: str) -> int:
        fn = self.current_fn
        if not fn:
            raise CodegenError(f"Degisken '{name}' fonksiyon disinda tanimlanamaz")
        existing = self.fn_var_offsets.get(fn.name, {})
        if name in existing:
            return existing[name]
        offset = len(existing) * 8 + 8
        self.fn_var_offsets[fn.name][name] = offset
        return offset

    def _generate_stmt(self, stmt: Stmt):
        line = getattr(stmt, "line", 0)
        try:
            if isinstance(stmt, LetDecl):
                self._gen_let(stmt)
            elif isinstance(stmt, Assign):
                self._gen_assign(stmt)
            elif isinstance(stmt, If):
                self._gen_if(stmt)
            elif isinstance(stmt, Match):
                self._gen_match(stmt)
            elif isinstance(stmt, While):
                self._gen_while(stmt)
            elif isinstance(stmt, Return):
                self._gen_return(stmt)
            elif isinstance(stmt, Println):
                self._gen_println(stmt)
            elif isinstance(stmt, ExprStmt):
                self._gen_expr(stmt.expr)
            elif isinstance(stmt, Block):
                for s in stmt.statements:
                    self._generate_stmt(s)
            elif isinstance(stmt, Use):
                pass
        except CodegenError:
            raise
        except Exception as e:
            raise CodegenError(str(e), line)

    def _gen_let(self, stmt: LetDecl):
        offset = self._alloc_var(stmt.name)
        if stmt.initializer:
            if isinstance(stmt.initializer, StringExpr):
                lbl = self.add_string(stmt.initializer.value)
                self.output.append(f"    lea rax, [rel {lbl}]")
                self.output.append(f"    mov [rbp-{offset}], rax")
            else:
                self._gen_expr(stmt.initializer)
                self.output.append(f"    mov [rbp-{offset}], rax")
        else:
            self.output.append(f"    mov qword [rbp-{offset}], 0")

    def _gen_assign(self, stmt: Assign):
        offset = self._get_var_offset(stmt.name)
        self._gen_expr(stmt.value)
        self.output.append(f"    mov [rbp-{offset}], rax")

    def _gen_if(self, stmt: If):
        else_label = self.new_label("else")
        end_label = self.new_label("endif")
        self._gen_cond_jump(stmt.condition, else_label)
        for s in stmt.then_body:
            self._generate_stmt(s)
        self.output.append(f"    jmp {end_label}")
        self.output.append(f"{else_label}:")
        for s in stmt.else_body:
            self._generate_stmt(s)
        self.output.append(f"{end_label}:")

    def _gen_match(self, stmt: Match):
        end_label = self.new_label("match_end")
        if not stmt.arms:
            return
        if stmt.expr:
            self._gen_expr(stmt.expr)
            self.output.append(f"    push rax")
        first = True
        for arm in stmt.arms:
            next_label = self.new_label("match_arm")
            if first:
                first = False
                self.output.append(f"    pop rbx")
                self.output.append(f"    push rbx")
                self.output.append(f"    cmp rbx, {arm.value}")
            else:
                self.output.append(f"    pop rax")
                self.output.append(f"    push rax")
                self.output.append(f"    cmp rax, {arm.value}")
            self.output.append(f"    jne {next_label}")
            for s in arm.body:
                self._generate_stmt(s)
            self.output.append(f"    jmp {end_label}")
            self.output.append(f"{next_label}:")
        if stmt.expr:
            self.output.append(f"    pop rax")
        self.output.append(f"{end_label}:")

    def _gen_while(self, stmt: While):
        start_label = self.new_label("while")
        end_label = self.new_label("wend")
        self.output.append(f"{start_label}:")
        self._gen_cond_jump(stmt.condition, end_label)
        for s in stmt.body:
            self._generate_stmt(s)
        self.output.append(f"    jmp {start_label}")
        self.output.append(f"{end_label}:")

    def _gen_return(self, stmt: Return):
        self.has_return = True
        if stmt.value:
            self._gen_expr(stmt.value)
        else:
            self.output.append("    xor eax, eax")
        exit_label = self.exit_labels.get(self.current_fn.name, "")
        if exit_label:
            self.output.append(f"    jmp {exit_label}")
        else:
            self.output.append("    mov rsp, rbp")
            self.output.append("    pop rbp")
            self.output.append("    ret")

    def _gen_println(self, stmt: Println):
        text = stmt.format_str
        for arg in stmt.args:
            self._gen_expr(arg)
            self.output.append("    push rax")
        lbl = self.add_string(text + "\n")
        self.output.append("    mov rax, 1          ; sys_write")
        self.output.append("    mov rdi, 1          ; stdout")
        self.output.append(f"    lea rsi, [rel {lbl}]")
        self.output.append(f"    mov rdx, {len(text) + 1}")
        self.output.append("    syscall")
        for _ in stmt.args:
            self.output.append("    pop rax")

    def _gen_expr(self, expr: Optional["Expr"]):
        if expr is None:
            self.output.append("    xor eax, eax")
            return
        if isinstance(expr, Integer):
            self.output.append(f"    mov eax, {expr.value}")
        elif isinstance(expr, BoolExpr):
            self.output.append(f"    mov eax, {1 if expr.value else 0}")
        elif isinstance(expr, StringExpr):
            lbl = self.add_string(expr.value)
            self.output.append(f"    lea rax, [rel {lbl}]")
        elif isinstance(expr, Ident):
            offset = self._get_var_offset(expr.name)
            self.output.append(f"    mov rax, [rbp-{offset}]")
        elif isinstance(expr, Unary):
            self._gen_expr(expr.operand)
            if expr.op == "-":
                self.output.append("    neg eax")
        elif isinstance(expr, Binary):
            self._gen_binary(expr)
        elif isinstance(expr, Call):
            self._gen_call(expr)
        else:
            raise CodegenError(f"Bilinmeyen ifade turu: {type(expr).__name__}")

    def _gen_binary(self, expr: Binary):
        op = expr.op
        self._gen_expr(expr.left)
        self.output.append("    push rax")
        self._gen_expr(expr.right)
        self.output.append("    mov rbx, rax")
        self.output.append("    pop rax")
        if op == "+":
            self.output.append("    add eax, ebx")
        elif op == "-":
            self.output.append("    sub eax, ebx")
        elif op == "*":
            self.output.append("    imul eax, ebx")
        elif op == "/":
            self.output.append("    xor edx, edx")
            self.output.append("    idiv ebx")
        elif op == "%":
            self.output.append("    xor edx, edx")
            self.output.append("    idiv ebx")
            self.output.append("    mov eax, edx")
        elif op in (">", "<", ">=", "<=", "==", "!="):
            self.output.append("    cmp eax, ebx")
            cmp_map = {
                ">": "setg",
                "<": "setl",
                ">=": "setge",
                "<=": "setle",
                "==": "sete",
                "!=": "setne",
            }
            self.output.append(f"    {cmp_map[op]} al")
            self.output.append("    movzx eax, al")

    def _gen_cond_jump(self, expr: Optional["Expr"], false_label: str):
        if expr is None:
            return
        self._gen_expr(expr)
        self.output.append("    cmp eax, 0")
        self.output.append(f"    je {false_label}")

    def _gen_call(self, expr: Call):
        if (
            expr.callee == "String::from"
            and len(expr.args) == 1
            and isinstance(expr.args[0], (StringExpr, Integer))
        ):
            val = expr.args[0]
            if isinstance(val, StringExpr):
                lbl = self.add_string(val.value)
                self.output.append(f"    lea rax, [rel {lbl}]")
            elif isinstance(val, Integer):
                self.output.append(f"    mov eax, {val.value}")
            return
        for i, arg in enumerate(expr.args):
            self._gen_expr(arg)
            regs = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
            if i < len(regs):
                self.output.append(f"    mov {regs[i]}, rax")
            else:
                self.output.append("    push rax")
        self.output.append(f"    call {expr.callee}")
