#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de verificación de cambios en el modelo de datos
Verifica que los cambios se hayan aplicado correctamente en models/db.py
"""

import re

def verificar_cambios():
    """Verifica que todos los cambios requeridos estén en el archivo"""
    print("\n" + "="*70)
    print("VERIFICACIÓN DE CAMBIOS EN models/db.py")
    print("Task 4: Actualizar Modelo de Datos")
    print("="*70)
    
    with open('models/db.py', 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    verificaciones = []
    
    # Subtask 4.1: Modificar definición de tabla cuentas
    print("\n" + "-"*70)
    print("Subtask 4.1: Modificar definición de tabla 'cuentas'")
    print("-"*70)
    
    # Verificar campo moneda
    if "Field('moneda', 'string', length=10, required=True, default='VES')" in contenido:
        print("✓ Campo 'moneda' agregado correctamente")
        verificaciones.append(True)
    else:
        print("✗ Campo 'moneda' no encontrado o incorrecto")
        verificaciones.append(False)
    
    # Verificar campo saldo
    if "Field('saldo', 'decimal(15,4)', default=0, required=True)" in contenido:
        print("✓ Campo 'saldo' agregado correctamente")
        verificaciones.append(True)
    else:
        print("✗ Campo 'saldo' no encontrado o incorrecto")
        verificaciones.append(False)
    
    # Verificar que campos antiguos están marcados como deprecated
    if "# DEPRECATED: Campos antiguos del modelo multi-moneda" in contenido:
        print("✓ Campos antiguos marcados como DEPRECATED")
        verificaciones.append(True)
    else:
        print("✗ Campos antiguos no están marcados como deprecated")
        verificaciones.append(False)
    
    # Verificar campo fecha_actualizacion
    if "Field('fecha_actualizacion', 'datetime', update=request.now)" in contenido:
        print("✓ Campo 'fecha_actualizacion' agregado")
        verificaciones.append(True)
    else:
        print("✗ Campo 'fecha_actualizacion' no encontrado")
        verificaciones.append(False)
    
    # Verificar formato actualizado
    if "format='%(numero_cuenta)s - %(moneda)s'" in contenido:
        print("✓ Formato de tabla actualizado para incluir moneda")
        verificaciones.append(True)
    else:
        print("✗ Formato de tabla no actualizado")
        verificaciones.append(False)
    
    # Subtask 4.2: Agregar validaciones a nivel de modelo
    print("\n" + "-"*70)
    print("Subtask 4.2: Agregar validaciones a nivel de modelo")
    print("-"*70)
    
    # Verificar validación de moneda
    if "IS_IN_SET(['VES', 'USD', 'EUR', 'USDT']" in contenido and \
       "error_message='Moneda debe ser VES, USD, EUR o USDT')" in contenido:
        print("✓ Validación de campo 'moneda' agregada (VES, USD, EUR, USDT)")
        verificaciones.append(True)
    else:
        print("✗ Validación de campo 'moneda' no encontrada o incompleta")
        verificaciones.append(False)
    
    # Verificar validación de saldo
    if "db.cuentas.saldo.requires = IS_DECIMAL_IN_RANGE(0, 999999999999.9999" in contenido:
        print("✓ Validación de campo 'saldo' agregada (>= 0)")
        verificaciones.append(True)
    else:
        print("✗ Validación de campo 'saldo' no encontrada")
        verificaciones.append(False)
    
    # Verificar índice por moneda
    if "CREATE INDEX IF NOT EXISTS idx_cuentas_moneda ON cuentas(moneda)" in contenido:
        print("✓ Índice idx_cuentas_moneda creado")
        verificaciones.append(True)
    else:
        print("✗ Índice idx_cuentas_moneda no encontrado")
        verificaciones.append(False)
    
    # Verificar índice compuesto cliente + moneda
    if "CREATE INDEX IF NOT EXISTS idx_cuentas_cliente_moneda ON cuentas(cliente_id, moneda)" in contenido:
        print("✓ Índice idx_cuentas_cliente_moneda creado")
        verificaciones.append(True)
    else:
        print("✗ Índice idx_cuentas_cliente_moneda no encontrado")
        verificaciones.append(False)
    
    # Verificar constraint de unicidad
    if "CREATE UNIQUE INDEX IF NOT EXISTS idx_cuentas_cliente_moneda_activa" in contenido and \
       "WHERE estado = 'activa'" in contenido:
        print("✓ Constraint de unicidad agregado (cliente + moneda + estado activa)")
        verificaciones.append(True)
    else:
        print("✗ Constraint de unicidad no encontrado")
        verificaciones.append(False)
    
    # Subtask 4.3: Actualizar modelo de transacciones
    print("\n" + "-"*70)
    print("Subtask 4.3: Actualizar modelo de 'transacciones'")
    print("-"*70)
    
    # Verificar campo cuenta_origen_id
    if "Field('cuenta_origen_id', 'reference cuentas')" in contenido:
        print("✓ Campo 'cuenta_origen_id' agregado")
        verificaciones.append(True)
    else:
        print("✗ Campo 'cuenta_origen_id' no encontrado")
        verificaciones.append(False)
    
    # Verificar campo cuenta_destino_id
    if "Field('cuenta_destino_id', 'reference cuentas')" in contenido:
        print("✓ Campo 'cuenta_destino_id' agregado")
        verificaciones.append(True)
    else:
        print("✗ Campo 'cuenta_destino_id' no encontrado")
        verificaciones.append(False)
    
    # Verificar que cuenta_id está marcado como deprecated
    if "# DEPRECATED: Campo antiguo (mantener para compatibilidad)" in contenido:
        print("✓ Campo 'cuenta_id' marcado como DEPRECATED")
        verificaciones.append(True)
    else:
        print("✗ Campo 'cuenta_id' no está marcado como deprecated")
        verificaciones.append(False)
    
    # Verificar validaciones de moneda incluyen USDT
    patron_moneda_transacciones = r"db\.transacciones\.moneda_origen\.requires.*\['VES', 'USD', 'EUR', 'USDT'\]"
    if re.search(patron_moneda_transacciones, contenido, re.DOTALL):
        print("✓ Validaciones de moneda actualizadas para incluir USDT")
        verificaciones.append(True)
    else:
        print("✗ Validaciones de moneda no incluyen USDT")
        verificaciones.append(False)
    
    # Verificar índices para nuevos campos
    if "CREATE INDEX IF NOT EXISTS idx_transacciones_cuenta_origen ON transacciones(cuenta_origen_id)" in contenido:
        print("✓ Índice idx_transacciones_cuenta_origen creado")
        verificaciones.append(True)
    else:
        print("✗ Índice idx_transacciones_cuenta_origen no encontrado")
        verificaciones.append(False)
    
    if "CREATE INDEX IF NOT EXISTS idx_transacciones_cuenta_destino ON transacciones(cuenta_destino_id)" in contenido:
        print("✓ Índice idx_transacciones_cuenta_destino creado")
        verificaciones.append(True)
    else:
        print("✗ Índice idx_transacciones_cuenta_destino no encontrado")
        verificaciones.append(False)
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE VERIFICACIÓN")
    print("="*70)
    
    exitosas = sum(verificaciones)
    total = len(verificaciones)
    porcentaje = (exitosas / total * 100) if total > 0 else 0
    
    print(f"\nVerificaciones exitosas: {exitosas}/{total} ({porcentaje:.1f}%)")
    
    if exitosas == total:
        print("\n✓ TODOS LOS CAMBIOS IMPLEMENTADOS CORRECTAMENTE")
        print("\nResumen de cambios:")
        print("  • Tabla 'cuentas':")
        print("    - Campo 'moneda' agregado (VES, USD, EUR, USDT)")
        print("    - Campo 'saldo' agregado (decimal 15,4)")
        print("    - Campos antiguos marcados como DEPRECATED")
        print("    - Validaciones agregadas")
        print("    - Constraint de unicidad implementado")
        print("    - Índices optimizados")
        print("\n  • Tabla 'transacciones':")
        print("    - Campo 'cuenta_origen_id' agregado")
        print("    - Campo 'cuenta_destino_id' agregado")
        print("    - Campo 'cuenta_id' marcado como DEPRECATED")
        print("    - Validaciones actualizadas para USDT")
        print("    - Índices para nuevos campos")
        print("\n✓ Task 4 completada exitosamente")
        return 0
    else:
        print("\n✗ ALGUNOS CAMBIOS NO SE ENCONTRARON")
        print(f"Faltan {total - exitosas} verificaciones")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(verificar_cambios())
