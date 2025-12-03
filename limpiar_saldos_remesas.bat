@echo off
REM Script para limpiar saldos, movimientos, remesas y limites
REM Sistema de Divisas Bancario

echo ========================================
echo LIMPIEZA DE SALDOS, MOVIMIENTOS, REMESAS Y LIMITES
echo Sistema de Divisas Bancario
echo ========================================
echo.
echo ADVERTENCIA: Este script limpiara:
echo   - Movimientos de cuenta
echo   - Remesas diarias
echo   - Movimientos de remesas
echo   - Limites de venta
echo   - Alertas de limites
echo   - Saldos de cuentas (reseteo a 0.00)
echo.
echo Se mantendran:
echo   - Clientes
echo   - Cuentas (estructura)
echo   - Usuarios
echo   - Transacciones (historial)
echo   - Tasas de cambio
echo.
pause

echo.
echo Ejecutando script de limpieza...
python ..\..\web2py.py -S divisas2os_multiple -M -R applications\divisas2os_multiple\limpiar_saldos_movimientos_remesas_limites.py

echo.
echo ========================================
echo Proceso completado
echo ========================================
pause
