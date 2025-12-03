@echo off
REM =========================================================================
REM Script Batch para Limpiar el Sistema de Divisas
REM =========================================================================

echo.
echo ========================================================================
echo   LIMPIEZA AUTOMATICA DEL SISTEMA DE DIVISAS
echo ========================================================================
echo.
echo   Este script eliminara:
echo   - Todas las transacciones
echo   - Todos los saldos (se pondran en 0)
echo   - Todas las remesas y limites
echo.
echo   ADVERTENCIA: Esta accion no se puede deshacer
echo.
echo ========================================================================
echo.

pause

echo.
echo Ejecutando limpieza...
echo.

python limpiar_sistema_simple.py

echo.
echo ========================================================================
echo   Proceso completado
echo ========================================================================
echo.

pause
