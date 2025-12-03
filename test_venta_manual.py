# -*- coding: utf-8 -*-
"""
Test manual del flujo de venta - Simula el proceso completo
"""

print("=" * 80)
print("TEST MANUAL: Flujo de Venta de Divisas")
print("=" * 80)

# Obtener cliente de prueba
cliente = db(db.clientes.cedula == 'V-12345678').select().first()

if not cliente:
    print("❌ No se encontró el cliente de prueba")
    print("Ejecute: python ..\\..\\web2py.py -S divisas2os_multiple -M -R crear_datos_prueba_venta.py")
    exit(1)

print(f"\n✓ Cliente encontrado: {cliente.cedula}")

# Obtener usuario
usuario = db(db.auth_user.id == cliente.user_id).select().first()
print(f"✓ Usuario: {usuario.email}")

# Obtener cuentas
cuentas = db(
    (db.cuentas.cliente_id == cliente.id) &
    (db.cuentas.estado == 'activa')
).select()

print(f"\n✓ Cuentas activas: {len(cuentas)}")
for cuenta in cuentas:
    print(f"  - {cuenta.numero_cuenta}: {cuenta.moneda} - Saldo: {cuenta.saldo}")

# Buscar cuenta USD con saldo
cuenta_usd = None
for cuenta in cuentas:
    if cuenta.moneda == 'USD' and cuenta.saldo > 0:
        cuenta_usd = cuenta
        break

if not cuenta_usd:
    print("\n❌ No hay cuenta USD con saldo")
    exit(1)

print(f"\n✓ Cuenta USD seleccionada: {cuenta_usd.numero_cuenta}")
print(f"  Saldo disponible: {cuenta_usd.saldo} USD")

# Simular venta
from decimal import Decimal

monto_venta = Decimal('50.00')  # Vender 50 USD

print(f"\n📤 Simulando venta de {monto_venta} USD...")

# Preparar request.vars
class FakeVars:
    def __init__(self):
        self.cuenta_id = str(cuenta_usd.id)
        self.moneda_origen = 'USD'
        self.cantidad_divisa = str(monto_venta)
        self.confirmar_venta = 'True'

# Simular autenticación (login real)
# En web2py, debemos hacer login real
from gluon.storage import Storage
auth.login_bare(usuario.email, 'prueba123')

# Guardar request.vars original
original_vars = request.vars
request.vars = FakeVars()

try:
    # Importar función de venta
    import sys
    import os
    
    # Ejecutar la función de procesamiento
    from applications.divisas2os_multiple.controllers.divisas import procesar_venta_divisa
    
    resultado = procesar_venta_divisa()
    
    if resultado['success']:
        print("\n✅ VENTA EXITOSA!")
        print(f"  Comprobante: {resultado['comprobante']}")
        print(f"  Transacción ID: {resultado['transaccion_id']}")
        print(f"  Monto vendido: {resultado['monto_origen']} USD")
        print(f"  Monto recibido: {resultado['monto_destino']} VES")
        print(f"  Comisión: {resultado['comision']} VES")
        print(f"  Tasa aplicada: {resultado['tasa_aplicada']}")
        
        # Verificar transacción en BD
        transaccion = db(db.transacciones.id == resultado['transaccion_id']).select().first()
        if transaccion:
            print(f"\n✓ Transacción registrada en BD")
            print(f"  Estado: {transaccion.estado}")
            print(f"  Comprobante: {transaccion.numero_comprobante}")
        
        # Verificar saldos actualizados
        cuenta_actualizada = db(db.cuentas.id == cuenta_usd.id).select().first()
        print(f"\n✓ Saldo actualizado:")
        print(f"  Anterior: {cuenta_usd.saldo} USD")
        print(f"  Actual: {cuenta_actualizada.saldo} USD")
        
        # Verificar que no hay tickets de error
        import os
        tickets = [f for f in os.listdir('errors') if f.endswith('.log')]
        if tickets:
            print(f"\n⚠️  Se generaron {len(tickets)} ticket(s) de error")
        else:
            print(f"\n✓ No se generaron tickets de error")
        
    else:
        print(f"\n❌ ERROR EN LA VENTA: {resultado['error']}")
        
except Exception as e:
    print(f"\n❌ EXCEPCIÓN: {str(e)}")
    import traceback
    traceback.print_exc()
    
finally:
    # Restaurar request.vars
    request.vars = original_vars

print("\n" + "=" * 80)
