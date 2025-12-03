@echo off
REM ========================================
REM Script de inicio con navegador automático
REM Sistema de Divisas - R4 Banco
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

REM Iniciar web2py en segundo plano
start /B C:\web2py\applications\divisas2os\Python\Python312-32\python.exe web2py.py -a 12345 -i 127.0.0.1 -p 8000
rem start /B python.exe web2py.py -a 12345 -i 127.0.0.1 -p 8000
REM Esperar 5 segundos para que el servidor inicie
echo Esperando que el servidor inicie...
timeout /t 5 /nobreak >nul

REM Abrir el navegador automáticamente
echo Abriendo navegador...
start http://127.0.0.1:8000/divisas2os

echo.
echo ========================================
echo   Servidor iniciado correctamente
echo ========================================
echo.
echo URL: http://127.0.0.1:8000/divisas2os
echo.
echo Para detener el servidor, cierre esta ventana
echo o presione Ctrl+C
echo.
pause
