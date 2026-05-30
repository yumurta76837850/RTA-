; ========================================================
; SENTINEL COMPANY - R+ COMPILER v3.0
; LISANS: SGU OZEL YAZILIM
; MIMARI: Lexer -> Parser (AST) -> Code Generator (NASM)
; ========================================================


section .text
global _start

_start:
    ; Program giris noktasi
    call ana_fonksiyon
    mov edi, eax        ; donus degeri => exit kodu
    mov eax, 60         ; sys_exit
    syscall

fibonacci:
    push rbp
    mov rbp, rsp
    sub rsp, 256        ; stack frame
    mov [rbp-8], rdi
    mov eax, 0
    mov [rbp-16], rax
    mov eax, 1
    mov [rbp-24], rax
    mov eax, 0
    mov [rbp-32], rax
.while_2:
    mov rax, [rbp-8]
    push rax
    mov eax, 0
    mov rbx, rax
    pop rax
    cmp eax, ebx
    setg al
    movzx eax, al
    cmp eax, 0
    je .wend_3
    mov rax, [rbp-16]
    push rax
    mov rax, [rbp-24]
    mov rbx, rax
    pop rax
    add eax, ebx
    mov [rbp-32], rax
    mov rax, [rbp-24]
    mov [rbp-16], rax
    mov rax, [rbp-32]
    mov [rbp-24], rax
    mov rax, [rbp-8]
    push rax
    mov eax, 1
    mov rbx, rax
    pop rax
    sub eax, ebx
    mov [rbp-8], rax
    jmp .while_2
.wend_3:
    mov rax, [rbp-16]
    jmp .fibonacci_exit_1
.fibonacci_exit_1:
    mov rsp, rbp
    pop rbp
    ret

ana_fonksiyon:
    push rbp
    mov rbp, rsp
    sub rsp, 256        ; stack frame
    mov eax, 0
    mov [rbp-8], rax
    mov eax, 10
    mov rdi, rax
    call fibonacci
    mov [rbp-8], rax
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_0]
    mov rdx, 22
    syscall
    mov rax, [rbp-8]
    push rax
    pop rax
    push rax
    cmp rax, 55
    jne .match_arm_6
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_1]
    mov rdx, 26
    syscall
    jmp .match_end_5
.match_arm_6:
    pop rax
    push rax
    cmp rax, 0
    jne .match_arm_7
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_2]
    mov rdx, 33
    syscall
    jmp .match_end_5
.match_arm_7:
    pop rax
.match_end_5:
    mov rax, [rbp-8]
    jmp .ana_fonksiyon_exit_4
.ana_fonksiyon_exit_4:
    mov rsp, rbp
    pop rbp
    ret


section .data
    str_0 db 'Fibonacci(10) sonucu:\n', 0
    str_1 db 'Dogru! Fibonacci(10) = 55\n', 0
    str_2 db 'Hata: Fibonacci hesabi basarisiz\n', 0