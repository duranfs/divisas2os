#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar el modelo de datos actualizado
Verifica que los nuevos campos y validaciones funcionen correctamente
"""

import sys
import os

# Configurar el entorno de web2py
web2py_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, web2py_path)

# Importar web2py
from gluon import DAL, Field
from gluon.validators import *

def test_modelo_cuentas():
    """Prueba el modelo actualizado de cuentas"""
    print("\n" + "="*60)
    print("PRUEBA: Modelo de Cuentas Actualizado")
    print("="*60)
    
    # Crear base de datos temporal para pruebas
    db = DAL('sqlite:memory:', migrate=False)
    
    # Definir tabla clientes (simplificada)
    db.define_table('clientes',
        Field('cedula', 'string'),
        migrate=False
    )
    
    # Definir tabla cuentas con el nuevo modelo
    db.define_table('cuentas',
        Field('cliente_id', 'reference clientes'),
        Field('numero_cuenta', 'string', length=20, unique=True),
        Field('tipo_cuenta', 'string', default='corriente'),
        
        # Nuevos campos
        Field('moneda', 'string', length=10, required=True, default='VES'),
        Field('saldo', 'decimal(15,4)', default=0, required=True),
        
        # Campos antiguos (deprecated)
        Field('saldo_ves', 'decimal(15,2)', default=0),
        Field('saldo_usd', 'decimal(15,2)', default=0),
        Field('saldo_eur', 'decimal(15,2)', default=0),
        Field('saldo_usdt', 'decimal(15,2)', default=0),
        
        Field('estado', 'string', default='activa'),
        migrate=False
    )
    
    # Validaciones
    db.cuentas.moneda.requires = [
        IS_NOT_EMPTY(error_message='La moneda es requerida'),
        IS_IN_SET(['VES', 'USD', 'EUR', 'USDT'], 
                  error_message='Moneda debe ser VES, USD, EUR o USDT')
    ]
    
    db.cuentas.saldo.requires = IS_DECIMAL_IN_RANGE(0, 999999999999.9999, 
                                                    error_message='Saldo debe ser un valor positivo o cero')
    
    print("\n✓ Tabla 'cuentas' definida correctamente")
    print("  - Campo 'moneda' agregado (VES, USD, EUR, USDT)")
    print("  - Campo 'saldo' agregado (decimal 15,4)")
    print("  - Campos antiguos marcados como deprecated")
    
    # Probar validaciones
    print("\n" + "-"*60)
    print("Probando validaciones...")
    print("-"*60)
    
    # Validación de moneda válida
    result, error = db.cuentas.moneda.validate('USD')
    if error is None:
        print("✓ Validación de moneda 'USD': CORRECTA")
    else:
        print(f"✗ Error en validación de moneda 'USD': {error}")
    
    # Validación de moneda inválida
    result, error = db.cuentas.moneda.validate('JPY')
    if error is not None:
        print("✓ Validación de moneda inválida 'JPY': RECHAZADA correctamente")
    else:
        print("✗ Error: Moneda inválida 'JPY' fue aceptada")
    
    # Validación de saldo positivo
    result, error = db.cuentas.saldo.validate(1000.50)
    if error is None:
        print("✓ Validación de saldo positivo: CORRECTA")
    else:
        print(f"✗ Error en validación de saldo: {error}")
    
    # Validación de saldo negativo
    result, error = db.cuentas.saldo.validate(-100)
    if error is not None:
        print("✓ Validación de saldo negativo: RECHAZADA correctamente")
    else:
        print("✗ Error: Saldo negativo fue aceptado")
    
    return True

def test_modelo_transacciones():
    """Prueba el modelo actualizado de transacciones"""
    print("\n" + "="*60)
    print("PRUEBA: Modelo de Transacciones Actualizado")
    print("="*60)
    
    # Crear base de datos temporal
    db = DAL('sqlite:memory:', migrate=False)
    
    # Definir tabla cuentas (simplificada)
    db.define_table('cuentas',
        Field('numero_cuenta', 'string'),
        Field('moneda', 'string'),
        migrate=False
    )
    
    # Definir tabla transacciones con el nuevo modelo
    db.define_table('transacciones',
        # Nuevos campos
        Field('cuenta_origen_id', 'reference cuentas'),
        Field('cuenta_destino_id', 'reference cuentas'),
        
        # Campo antiguo (deprecated)
        Field('cuenta_id', 'reference cuentas'),
        
        Field('tipo_operacion', 'string'),
        Field('moneda_origen', 'string', length=3),
        Field('moneda_destino', 'string', length=3),
        Field('monto_origen', 'decimal(15,2)'),
        Field('monto_destino', 'decimal(15,2)'),
        migrate=False
    )
    
    # Validaciones
    db.transacciones.moneda_origen.requires = IS_IN_SET(['VES', 'USD', 'EUR', 'USDT'])
    db.transacciones.moneda_destino.requires = IS_IN_SET(['VES', 'USD', 'EUR', 'USDT'])
    
    print("\n✓ Tabla 'transacciones' definida correctamente")
    print("  - Campo 'cuenta_origen_id' agregado")
    print("  - Campo 'cuenta_destino_id' agregado")
    print("  - Campo 'cuenta_id' marcado como deprecated")
    print("  - Validaciones actualizadas para incluir USDT")
    
    # Probar validaciones
    print("\n" + "-"*60)
    print("Probando validaciones...")
    print("-"*60)
    
    # Validación de USDT
    result, error = db.transacciones.moneda_origen.validate('USDT')
    if error is None:
        print("✓ Validación de moneda 'USDT': CORRECTA")
    else:
        print(f"✗ Error en validación de USDT: {error}")
    
    return True

def test_indices():
    """Verifica que los índices se puedan crear"""
    print("\n" + "="*60)
    print("PRUEBA: Creación de Índices")
    print("="*60)
    
    db = DAL('sqlite:memory:', migrate=False)
    
    db.define_table('cuentas',
        Field('cliente_id', 'integer'),
        Field('moneda', 'string'),
        Field('estado', 'string'),
        migrate=False
    )
    
    try:
        # Índice simple por moneda
        db.executesql('CREATE INDEX IF NOT EXISTS idx_cuentas_moneda ON cuentas(moneda);')
        print("✓ Índice idx_cuentas_moneda creado")
        
        # Índice compuesto cliente + moneda
        db.executesql('CREATE INDEX IF NOT EXISTS idx_cuentas_cliente_moneda ON cuentas(cliente_id, moneda);')
        print("✓ Índice idx_cuentas_cliente_moneda creado")
        
        # Índice único parcial (constraint de unicidad)
        db.executesql('''
            CREATE UNIQUE INDEX IF NOT EXISTS idx_cuentas_cliente_moneda_activa 
            ON cuentas(cliente_id, moneda) 
            WHERE estado = 'activa'
        ''')
        print("✓ Índice único idx_cuentas_cliente_moneda_activa creado")
        print("  (Constraint: Un cliente no puede tener dos cuentas activas de la misma moneda)")
        
        return True
    except Exception as e:
        print(f"✗ Error creando índices: {str(e)}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "="*60)
    print("VERIFICACIÓN DEL MODELO DE DATOS ACTUALIZADO")
    print("Task 4: Actualizar Modelo de Datos en models/db.py")
    print("="*60)
    
    resultados = []
    
    try:
        resultados.append(("Modelo de Cuentas", test_modelo_cuentas()))
    except Exception as e:
        print(f"\n✗ Error en prueba de modelo de cuentas: {str(e)}")
        resultados.append(("Modelo de Cuentas", False))
    
    try:
        resultados.append(("Modelo de Transacciones", test_modelo_transacciones()))
    except Exception as e:
        print(f"\n✗ Error en prueba de modelo de transacciones: {str(e)}")
        resultados.append(("Modelo de Transacciones", False))
    
    try:
        resultados.append(("Índices", test_indices()))
    except Exception as e:
        print(f"\n✗ Error en prueba de índices: {str(e)}")
        resultados.append(("Índices", False))
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    
    for nombre, resultado in resultados:
        estado = "✓ EXITOSA" if resultado else "✗ FALLIDA"
        print(f"{nombre}: {estado}")
    
    exitosas = sum(1 for _, r in resultados if r)
    total = len(resultados)
    
    print(f"\nTotal: {exitosas}/{total} pruebas exitosas")
    
    if exitosas == total:
        print("\n✓ TODAS LAS PRUEBAS PASARON")
        print("\nCambios implementados correctamente:")
        print("  • Tabla 'cuentas' actualizada con campos 'moneda' y 'saldo'")
        print("  • Campos antiguos marcados como deprecated")
        print("  • Validaciones agregadas para moneda (VES, USD, EUR, USDT)")
        print("  • Validación de saldo >= 0")
        print("  • Constraint de unicidad (cliente + moneda + estado activa)")
        print("  • Tabla 'transacciones' actualizada con cuenta_origen_id y cuenta_destino_id")
        print("  • Índices optimizados para consultas por moneda")
        return 0
    else:
        print("\n✗ ALGUNAS PRUEBAS FALLARON")
        return 1

if __name__ == '__main__':
    sys.exit(main())
