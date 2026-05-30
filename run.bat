@echo off
chcp 65001 >nul
echo ============================================================
echo  SENTINEL COMPANY - R+ COMPILER v3.0
echo ============================================================

if "%1"=="" (
    echo  Kullanim: run.bat ^<dosya.rsp^>
    echo  Ornek:    run.bat test_kodu.rsp
    echo.
    echo  Mevcut .rsp dosyalari:
    for %%f in (*.rsp) do echo    - %%f
    goto :end
)

python compiler.py %1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [HATA] Derleme basarisiz!
    exit /b 1
)

echo.
echo  NASM ile assemble etmek icin:
echo    nasm -f elf64 test_kodu.asm -o test_kodu.o
echo    ld test_kodu.o -o test_kodu
echo    ./test_kodu
echo.
echo  veya dogrudan Linux WSL'de calistirin:
echo    wsl nasm -f elf64 test_kodu.asm -o test_kodu.o ^&^& wsl ld test_kodu.o -o test_kodu ^&^& wsl ./test_kodu
echo.
:end
