@echo off
REM ========================================
REM Script de inicio - Sistema de Divisas
REM R4 Banco Microfinanciero
REM ========================================

echo.
echo ========================================
echo   Sistema de Divisas Bancario
echo   R4 Banco Microfinanciero
echo ========================================
echo.
echo Iniciando servidor web2py...
echo.

REM Cambiar al directorio de web2py
cd /d C:\web2py

REM Limpiar variables de entorno de Python embebido
set PYTHONHOME=
set PYTHONPATH=

REM Iniciar web2py con configuración específica
REM -a <password>: Contraseña del panel administrativo
REM -i 127.0.0.1: Solo acceso local (más seguro)
REM -p 8000: Puerto 8000
python.exe web2py.py -a admin123 -i 127.0.0.1 -p 8000

REM Si el servidor se detiene, pausar para ver mensajes de error
pause
