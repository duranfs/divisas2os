@echo off
REM ========================================
REM Script de inicio AUTOMÁTICO
REM Sistema de Divisas - R4 Banco
REM Detecta Python automáticamente
REM ========================================

echo.
echo ========================================
echo   Sistema de Divisas Bancario
echo   R4 Banco Microfinanciero
echo ========================================
echo.

REM Limpiar variables de entorno de Python embebido
set PYTHONHOME=
set PYTHONPATH=

REM Verificar si Python está disponible en el PATH
where python.exe >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH del sistema
    echo.
    echo Por favor instala Python desde: https://www.python.org/downloads/
    echo O agrega Python al PATH del sistema
    pause
    exit /b 1
)

REM Mostrar versión de Python
echo Detectando Python...
python.exe --version
echo.

REM Cambiar al directorio de web2py
cd /d C:\web2py

REM Verificar que web2py.py existe
if not exist web2py.py (
    echo ERROR: No se encuentra web2py.py en C:\web2py
    echo Verifica que web2py esté instalado correctamente
    pause
    exit /b 1
)

echo Iniciando servidor web2py...
echo URL: http://127.0.0.1:8000/divisas2os
echo.
echo Para detener el servidor, presiona Ctrl+C
echo.

REM Iniciar web2py
python.exe web2py.py -a admin123 -i 127.0.0.1 -p 8000

REM Si el servidor se detiene, pausar
pause
