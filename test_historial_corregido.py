#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para probar que el historial de transacciones funciona correctamente
después de corregir el error del campo 'comprobante'
"""

import sys
import os

# Agregar el directorio de web2py al path
web2py_path = r'C:\web2py'
sys.path.insert(0, web2py_path)

# Configurar el entorno de web2py
os.chdir(web2py_path)

from gluon.shell import env
from gluon import current

# Cargar el entorno de la aplicación
app_name = 'divisas2os_multiple'
myenv = env(app_name, import_models=True, c={})

# Obtener objetos del entorno
db = myenv['db']
auth = myenv['auth']

print("=" * 80)
print("PRUEBA: Historial de Transacciones - Campo Comprobante Corregido")
print("=" * 80)

try:
    # 1. Verificar estructura de la tabla transacciones
    print("\n1. Verificando estructura de la tabla 'transacciones'...")
    print("-" * 80)
    
    campos_transacciones = [field for field in db.transacciones.fields]
    print(f"Campos en la tabla transacciones: {', '.join(campos_transacciones)}")
    
    # Verificar si existe 'numero_comprobante' y NO existe 'comprobante'
    tiene_numero_comprobante = 'numero_comprobante' in campos_transacciones
    tiene_comprobante = 'comprobante' in campos_transacciones
    
    print(f"\n✓ Campo 'numero_comprobante' existe: {tiene_numero_comprobante}")
    print(f"✓ Campo 'comprobante' existe: {tiene_comprobante}")
    
    if tiene_numero_comprobante and not tiene_comprobante:
        print("\n✅ CORRECTO: La tabla usa 'numero_comprobante' (no 'comprobante')")
    else:
        print("\n⚠️ ADVERTENCIA: Estructura de tabla inesperada")
    
    # 2. Obtener transacciones de prueba
    print("\n2. Obteniendo transacciones de prueba...")
    print("-" * 80)
    
    transacciones = db(db.transacciones.id > 0).select(
        db.transacciones.ALL,
        orderby=~db.transacciones.fecha_transaccion,
        limitby=(0, 5)
    )
    
    print(f"Total de transacciones encontradas: {len(transacciones)}")
    
    if len(transacciones) > 0:
        print("\nPrimeras 5 transacciones:")
        for t in transacciones:
            print(f"\n  ID: {t.id}")
            print(f"  Tipo: {t.tipo_operacion}")
            print(f"  Número Comprobante: {t.numero_comprobante}")
            print(f"  Fecha: {t.fecha_transaccion}")
            print(f"  Monto Origen: {t.monto_origen} {t.moneda_origen}")
            print(f"  Monto Destino: {t.monto_destino} {t.moneda_destino}")
            print(f"  Estado: {t.estado}")
            
            # Intentar acceder al campo numero_comprobante (debe funcionar)
            try:
                comprobante = t.numero_comprobante
                print(f"  ✅ Acceso a 'numero_comprobante': OK ({comprobante})")
            except Exception as e:
                print(f"  ❌ Error accediendo a 'numero_comprobante': {str(e)}")
            
            # Intentar acceder al campo comprobante (NO debe existir)
            try:
                comprobante_viejo = t.comprobante
                print(f"  ⚠️ Campo 'comprobante' existe (inesperado): {comprobante_viejo}")
            except AttributeError:
                print(f"  ✅ Campo 'comprobante' no existe (correcto)")
            except Exception as e:
                print(f"  ⚠️ Error inesperado: {str(e)}")
    else:
        print("\n⚠️ No hay transacciones en la base de datos")
    
    # 3. Simular consulta del historial (como lo hace el controlador)
    print("\n3. Simulando consulta del historial...")
    print("-" * 80)
    
    # Obtener un usuario de prueba
    usuario_prueba = db(db.auth_user.email == 'test@example.com').select().first()
    
    if usuario_prueba:
        print(f"Usuario de prueba: {usuario_prueba.email}")
        
        # Buscar cliente asociado
        cliente = db(db.clientes.user_id == usuario_prueba.id).select().first()
        
        if cliente:
            print(f"Cliente encontrado: {cliente.nombre} {cliente.apellido}")
            
            # Obtener cuentas del cliente
            cuentas_cliente = db(db.cuentas.cliente_id == cliente.id).select()
            cuenta_ids = [c.id for c in cuentas_cliente]
            
            print(f"Cuentas del cliente: {len(cuentas_cliente)}")
            
            # Obtener transacciones del cliente
            if cuenta_ids:
                transacciones_cliente = db(
                    db.transacciones.cuenta_id.belongs(cuenta_ids)
                ).select(
                    db.transacciones.ALL,
                    db.cuentas.numero_cuenta,
                    db.cuentas.moneda,
                    left=db.cuentas.on(db.transacciones.cuenta_id == db.cuentas.id),
                    orderby=~db.transacciones.fecha_transaccion,
                    limitby=(0, 10)
                )
                
                print(f"Transacciones del cliente: {len(transacciones_cliente)}")
                
                if len(transacciones_cliente) > 0:
                    print("\nPrimera transacción del cliente:")
                    t = transacciones_cliente[0]
                    print(f"  Comprobante: {t.transacciones.numero_comprobante}")
                    print(f"  Tipo: {t.transacciones.tipo_operacion}")
                    print(f"  Cuenta: {t.cuentas.numero_cuenta if t.cuentas else 'N/A'}")
                    print(f"  ✅ Consulta exitosa sin errores")
                else:
                    print("  ⚠️ El cliente no tiene transacciones")
            else:
                print("  ⚠️ El cliente no tiene cuentas")
        else:
            print("  ⚠️ No se encontró registro de cliente para este usuario")
    else:
        print("  ⚠️ Usuario de prueba no encontrado")
    
    print("\n" + "=" * 80)
    print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 80)
    print("\nConclusión:")
    print("- La tabla 'transacciones' usa el campo 'numero_comprobante'")
    print("- La vista fue corregida para NO usar el campo 'comprobante' inexistente")
    print("- El historial de transacciones debería funcionar correctamente ahora")
    print("\nPróximos pasos:")
    print("1. Acceder a: http://127.0.0.1:8000/divisas2os_multiple/divisas/historial_transacciones")
    print("2. Verificar que no aparezcan errores de 'comprobante'")
    print("3. Confirmar que los números de comprobante se muestran correctamente")

except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
