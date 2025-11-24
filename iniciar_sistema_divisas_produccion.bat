@echo off
REM ========================================
REM Script de inicio - MODO PRODUCCIÓN
REM Sistema de Divisas - R4 Banco
REM ========================================

echo.
echo ========================================
echo   Sistema de Divisas Bancario
echo   MODO PRODUCCION
echo   R4 Banco Microfinanciero
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

echo Iniciando servidor en modo producción...
echo.

REM Cambiar al directorio de web2py
cd /d C:\web2py

REM Limpiar variables de entorno de Python embebido
set PYTHONHOME=
set PYTHONPATH=

REM Iniciar web2py en modo producción
REM -a <password>: Contraseña del panel administrativo (CAMBIAR EN PRODUCCIÓN)
REM -i 0.0.0.0: Acceso desde cualquier IP de la red
REM -p 8000: Puerto 8000
REM --no-banner: Sin banner de inicio
python.exe web2py.py -a TuPasswordSeguro2025! -i 0.0.0.0 -p 8000 --no-banner

REM Si el servidor se detiene, pausar para ver mensajes de error
pause
