; ========================================================
; SENTINEL COMPANY - R+ COMPILER v3.0
; LISANS: SGU OZEL YAZILIM
; MIMARI: Lexer -> Parser (AST) -> Code Generator (NASM)
; ========================================================

; [Modul]: std::net::TcpStream
; [Modul]: std::string::String

section .text
global _start

_start:
    ; Program giris noktasi
    call ana_fonksiyon
    mov edi, eax        ; donus degeri => exit kodu
    mov eax, 60         ; sys_exit
    syscall

siber_giriş_ekranı:
    push rbp
    mov rbp, rsp
    sub rsp, 256        ; stack frame
    mov eax, 1
    mov [rbp-8], rax
    lea rax, [rel str_0]
    mov [rbp-16], rax
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_1]
    mov rdx, 21
    syscall
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_2]
    mov rdx, 24
    syscall
    mov rax, [rbp-8]
    jmp .siber_giriş_ekranı_exit_1
.siber_giriş_ekranı_exit_1:
    mov rsp, rbp
    pop rbp
    ret

toplama_islemi:
    push rbp
    mov rbp, rsp
    sub rsp, 256        ; stack frame
    mov eax, 500
    mov [rbp-8], rax
    mov eax, 250
    mov [rbp-16], rax
    mov eax, 0
    mov [rbp-24], rax
    mov rax, [rbp-8]
    push rax
    mov rax, [rbp-16]
    mov rbx, rax
    pop rax
    add eax, ebx
    mov [rbp-24], rax
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_3]
    mov rdx, 34
    syscall
    mov rax, [rbp-24]
    jmp .toplama_islemi_exit_2
.toplama_islemi_exit_2:
    mov rsp, rbp
    pop rbp
    ret

cikarma_islemi:
    push rbp
    mov rbp, rsp
    sub rsp, 256        ; stack frame
    mov eax, 1000
    mov [rbp-8], rax
    mov eax, 450
    mov [rbp-16], rax
    mov eax, 0
    mov [rbp-24], rax
    mov rax, [rbp-8]
    push rax
    mov rax, [rbp-16]
    mov rbx, rax
    pop rax
    sub eax, ebx
    mov [rbp-24], rax
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_4]
    mov rdx, 34
    syscall
    mov rax, [rbp-24]
    jmp .cikarma_islemi_exit_3
.cikarma_islemi_exit_3:
    mov rsp, rbp
    pop rbp
    ret

kripto_xor_simulasyon:
    push rbp
    mov rbp, rsp
    sub rsp, 256        ; stack frame
    mov eax, 120
    mov [rbp-8], rax
    mov eax, 35
    mov [rbp-16], rax
    mov eax, 0
    mov [rbp-24], rax
    mov rax, [rbp-8]
    push rax
    mov rax, [rbp-16]
    mov rbx, rax
    pop rax
    add eax, ebx
    mov [rbp-24], rax
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_5]
    mov rdx, 33
    syscall
    mov rax, [rbp-24]
    jmp .kripto_xor_simulasyon_exit_4
.kripto_xor_simulasyon_exit_4:
    mov rsp, rbp
    pop rbp
    ret

risk_gostergesi_hesapla:
    push rbp
    mov rbp, rsp
    sub rsp, 256        ; stack frame
    mov eax, 1850
    mov [rbp-8], rax
    mov eax, 1500
    mov [rbp-16], rax
    mov eax, 0
    mov [rbp-24], rax
    mov rax, [rbp-8]
    push rax
    mov rax, [rbp-16]
    mov rbx, rax
    pop rax
    cmp eax, ebx
    setg al
    movzx eax, al
    cmp eax, 0
    je .else_6
    mov eax, 1
    mov [rbp-24], rax
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_6]
    mov rdx, 28
    syscall
    mov rax, [rbp-24]
    jmp .risk_gostergesi_hesapla_exit_5
    jmp .endif_7
.else_6:
.endif_7:
    mov eax, 0
    mov [rbp-32], rax
    mov rax, [rbp-32]
    jmp .risk_gostergesi_hesapla_exit_5
.risk_gostergesi_hesapla_exit_5:
    mov rsp, rbp
    pop rbp
    ret

ana_fonksiyon:
    push rbp
    mov rbp, rsp
    sub rsp, 256        ; stack frame
    mov eax, 0
    mov [rbp-8], rax
    call siber_giriş_ekranı
    mov [rbp-8], rax
    mov eax, 0
    mov [rbp-16], rax
    call toplama_islemi
    mov [rbp-16], rax
    mov eax, 0
    mov [rbp-24], rax
    call cikarma_islemi
    mov [rbp-24], rax
    mov eax, 0
    mov [rbp-32], rax
    call kripto_xor_simulasyon
    mov [rbp-32], rax
    mov eax, 0
    mov [rbp-40], rax
    call risk_gostergesi_hesapla
    mov [rbp-40], rax
    mov rax, [rbp-40]
    push rax
    pop rbx
    push rbx
    cmp rbx, 1
    jne .match_arm_10
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_7]
    mov rdx, 24
    syscall
    jmp .match_end_9
.match_arm_10:
    pop rax
    push rax
    cmp rax, 0
    jne .match_arm_11
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_8]
    mov rdx, 23
    syscall
    jmp .match_end_9
.match_arm_11:
    pop rax
.match_end_9:
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    lea rsi, [rel str_9]
    mov rdx, 39
    syscall
    mov eax, 1
    mov [rbp-48], rax
    mov rax, [rbp-48]
    jmp .ana_fonksiyon_exit_8
.ana_fonksiyon_exit_8:
    mov rsp, rbp
    pop rbp
    ret


section .data
    str_0 db '--- Sentinel Company R+ Hesaplama Motoru ---', 0
    str_1 db 'Sistem Yukleniyor...\n', 0
    str_2 db 'Gis Kontrol Ediliyor...\n', 0
    str_3 db 'Toplama Islemi Basariyla Yapildi.\n', 0
    str_4 db 'Hafiza Cikarma Islemi Tamamlandi.\n', 0
    str_5 db 'Kripto Veri Hesaplamasi Yapildi.\n', 0
    str_6 db 'UYARI: Limit Degeri Asildi!\n', 0
    str_7 db 'Kritik Risk: 1 (Yuksek)\n', 0
    str_8 db 'Kritik Risk: 0 (Dusuk)\n', 0
    str_9 db 'Sentinel R+ Tum Hesaplamalari Bitirdi.\n', 0