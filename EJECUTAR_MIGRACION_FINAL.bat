@echo off
REM =========================================================================
REM Script de Ejecución de Migración en Producción
REM Sistema de Divisas Bancario
REM =========================================================================

echo.
echo =========================================================================
echo MIGRACION DE CUENTAS MULTI-MONEDA A CUENTAS INDIVIDUALES
echo Sistema de Divisas Bancario
echo =========================================================================
echo.
echo ADVERTENCIA: Este proceso realizara cambios permanentes en la base de datos
echo.
echo Pasos que se ejecutaran:
echo   1. Backup completo de la base de datos
echo   2. Migracion de cuentas
echo   3. Validacion de integridad de datos
echo   4. Verificacion de cuentas creadas
echo   5. Generacion de reporte completo
echo.
echo =========================================================================
echo.

pause

echo.
echo [PASO 1] Ejecutando backup de la base de datos...
echo.
python backup_bd_antes_migracion.py

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo realizar el backup
    echo Abortando migracion...
    pause
    exit /b 1
)

echo.
echo =========================================================================
echo [PASO 2] Ejecutando migracion completa...
echo =========================================================================
echo.
echo IMPORTANTE: El script solicitara confirmacion antes de realizar cambios
echo.

python web2py.py -S sistema_divisas -M -R applications/sistema_divisas/ejecutar_migracion_produccion.py

if errorlevel 1 (
    echo.
    echo ERROR: La migracion fallo
    echo Revise los reportes generados para mas detalles
    pause
    exit /b 1
)

echo.
echo =========================================================================
echo MIGRACION COMPLETADA
echo =========================================================================
echo.
echo Revise los reportes generados:
echo   - reporte_migracion_produccion_*.txt
echo   - validacion_migracion_*.txt
echo.
echo Backups disponibles en: applications\sistema_divisas\backups\
echo.
echo =========================================================================
echo.

pause
