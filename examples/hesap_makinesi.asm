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

topla:
    push rbp
    mov rbp, rsp
    sub rsp, 256        ; stack frame
    mov [rbp-8], rdi
    mov [rbp-8], rsi
    mov rax, [rbp-8]
    push rax
    mov rax, [rbp-8]
    mov rbx, rax
    pop rax
    add eax, ebx
    mov [rbp-24], rax
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_0]
    mov rdx, 9
    syscall
    mov rax, [rbp-24]
    jmp .topla_exit_1
.topla_exit_1:
    mov rsp, rbp
    pop rbp
    ret

cikar:
    push rbp
    mov rbp, rsp
    sub rsp, 256        ; stack frame
    mov [rbp-8], rdi
    mov [rbp-8], rsi
    mov rax, [rbp-8]
    push rax
    mov rax, [rbp-8]
    mov rbx, rax
    pop rax
    sub eax, ebx
    mov [rbp-24], rax
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_1]
    mov rdx, 9
    syscall
    mov rax, [rbp-24]
    jmp .cikar_exit_2
.cikar_exit_2:
    mov rsp, rbp
    pop rbp
    ret

carp:
    push rbp
    mov rbp, rsp
    sub rsp, 256        ; stack frame
    mov [rbp-8], rdi
    mov [rbp-8], rsi
    mov rax, [rbp-8]
    push rax
    mov rax, [rbp-8]
    mov rbx, rax
    pop rax
    imul eax, ebx
    mov [rbp-24], rax
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_2]
    mov rdx, 8
    syscall
    mov rax, [rbp-24]
    jmp .carp_exit_3
.carp_exit_3:
    mov rsp, rbp
    pop rbp
    ret

bol:
    push rbp
    mov rbp, rsp
    sub rsp, 256        ; stack frame
    mov [rbp-8], rdi
    mov [rbp-8], rsi
    mov eax, 0
    mov [rbp-24], rax
    mov rax, [rbp-8]
    push rax
    mov eax, 0
    mov rbx, rax
    pop rax
    cmp eax, ebx
    setg al
    movzx eax, al
    cmp eax, 0
    je .else_5
    mov rax, [rbp-8]
    push rax
    mov rax, [rbp-8]
    mov rbx, rax
    pop rax
    xor edx, edx
    idiv ebx
    mov [rbp-24], rax
    jmp .endif_6
.else_5:
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_3]
    mov rdx, 20
    syscall
    mov eax, 0
    jmp .bol_exit_4
.endif_6:
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_4]
    mov rdx, 7
    syscall
    mov rax, [rbp-24]
    jmp .bol_exit_4
.bol_exit_4:
    mov rsp, rbp
    pop rbp
    ret

ana_fonksiyon:
    push rbp
    mov rbp, rsp
    sub rsp, 256        ; stack frame
    mov eax, 0
    mov [rbp-8], rax
    mov eax, 0
    mov [rbp-16], rax
    mov eax, 0
    mov [rbp-24], rax
    mov eax, 100
    mov [rbp-8], rax
    mov eax, 25
    mov [rbp-16], rax
    mov rax, [rbp-8]
    mov rdi, rax
    mov rax, [rbp-16]
    mov rsi, rax
    call topla
    mov [rbp-24], rax
    mov rax, [rbp-8]
    mov rdi, rax
    mov rax, [rbp-16]
    mov rsi, rax
    call cikar
    mov [rbp-24], rax
    mov rax, [rbp-8]
    mov rdi, rax
    mov rax, [rbp-16]
    mov rsi, rax
    call carp
    mov [rbp-24], rax
    mov rax, [rbp-8]
    mov rdi, rax
    mov rax, [rbp-16]
    mov rsi, rax
    call bol
    mov [rbp-24], rax
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_5]
    mov rdx, 27
    syscall
    mov rax, [rbp-24]
    jmp .ana_fonksiyon_exit_7
.ana_fonksiyon_exit_7:
    mov rsp, rbp
    pop rbp
    ret


section .data
    str_0 db 'Toplama:\n', 0
    str_1 db 'Cikarma:\n', 0
    str_2 db 'Carpma:\n', 0
    str_3 db 'HATA: Sifira bolum!\n', 0
    str_4 db 'Bolme:\n', 0
    str_5 db 'Hesap Makinesi Tamamlandi.\n', 0