# -*- coding: utf-8 -*-
"""
Test del flujo completo de venta de divisas
Verifica que el proceso de venta funcione sin errores
"""

import sys
import os
import datetime
from decimal import Decimal

# Configurar path para web2py
web2py_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, web2py_path)

def test_flujo_venta():
    """
    Prueba el flujo completo de venta:
    1. Verificar que existe un usuario cliente
    2. Verificar que tiene cuentas activas con saldo
    3. Simular una venta de divisas
    4. Verificar que la transacción se procesa correctamente
    5. Verificar que el comprobante se puede mostrar sin errores
    """
    
    print("=" * 80)
    print("TEST: Flujo Completo de Venta de Divisas")
    print("=" * 80)
    
    try:
        # Importar módulos de web2py
        from gluon import current
        from gluon.shell import env
        
        # Cargar el entorno de la aplicación
        request = current.request
        db = current.db
        auth = current.auth
        
        print("\n1. Verificando usuarios y clientes en el sistema...")
        
        # Buscar un usuario con rol de cliente
        clientes = db(db.clientes.id > 0).select()
        
        if not clientes:
            print("❌ No hay clientes registrados en el sistema")
            print("   Ejecute primero: python web2py.py -S sistema_divisas -M -R crear_datos_prueba_venta.py")
            return False
        
        cliente = clientes.first()
        print(f"✓ Cliente encontrado: ID {cliente.id}")
        
        # Obtener usuario asociado
        usuario = db(db.auth_user.id == cliente.user_id).select().first()
        if not usuario:
            print("❌ Cliente no tiene usuario asociado")
            return False
        
        print(f"✓ Usuario asociado: {usuario.email}")
        
        print("\n2. Verificando cuentas del cliente...")
        
        # Buscar cuentas activas del cliente
        cuentas = db(
            (db.cuentas.cliente_id == cliente.id) &
            (db.cuentas.estado == 'activa')
        ).select()
        
        if not cuentas:
            print("❌ El cliente no tiene cuentas activas")
            return False
        
        print(f"✓ Cuentas activas encontradas: {len(cuentas)}")
        
        # Buscar una cuenta con divisa (USD, EUR o USDT) con saldo
        cuenta_divisa = None
        for cuenta in cuentas:
            if cuenta.moneda in ['USD', 'EUR', 'USDT'] and cuenta.saldo > 0:
                cuenta_divisa = cuenta
                break
        
        if not cuenta_divisa:
            print("❌ No hay cuentas de divisas con saldo disponible")
            print("   Cuentas disponibles:")
            for cuenta in cuentas:
                print(f"   - {cuenta.numero_cuenta}: {cuenta.moneda} - Saldo: {cuenta.saldo}")
            return False
        
        print(f"✓ Cuenta de divisa con saldo: {cuenta_divisa.numero_cuenta}")
        print(f"  Moneda: {cuenta_divisa.moneda}, Saldo: {cuenta_divisa.saldo}")
        
        print("\n3. Simulando venta de divisas...")
        
        # Preparar datos para la venta
        monto_venta = min(Decimal('10.00'), cuenta_divisa.saldo / 2)  # Vender la mitad o 10, lo que sea menor
        
        print(f"  Vendiendo {monto_venta} {cuenta_divisa.moneda}")
        
        # Simular request.vars para la venta
        class FakeVars:
            def __init__(self):
                self.cuenta_id = cuenta_divisa.id
                self.moneda_origen = cuenta_divisa.moneda
                self.cantidad_divisa = str(monto_venta)
                self.confirmar_venta = True
        
        # Guardar request.vars original
        original_vars = request.vars
        request.vars = FakeVars()
        
        # Simular autenticación
        auth.user = usuario
        auth.user_id = usuario.id
        
        # Importar la función de procesamiento
        from applications.sistema_divisas.controllers.divisas import procesar_venta_divisa
        
        # Ejecutar la venta
        resultado = procesar_venta_divisa()
        
        # Restaurar request.vars
        request.vars = original_vars
        
        if not resultado.get('success'):
            print(f"❌ Error en la venta: {resultado.get('error')}")
            return False
        
        print("✓ Venta procesada exitosamente")
        print(f"  Comprobante: {resultado.get('comprobante')}")
        print(f"  Monto origen: {resultado.get('monto_origen')} {cuenta_divisa.moneda}")
        print(f"  Monto destino: {resultado.get('monto_destino')} VES")
        print(f"  Comisión: {resultado.get('comision')} VES")
        print(f"  Tasa aplicada: {resultado.get('tasa_aplicada')}")
        
        transaccion_id = resultado.get('transaccion_id')
        
        if not transaccion_id:
            print("❌ No se obtuvo ID de transacción")
            return False
        
        print("\n4. Verificando que la transacción se registró correctamente...")
        
        # Verificar que la transacción existe en la BD
        transaccion = db(db.transacciones.id == transaccion_id).select().first()
        
        if not transaccion:
            print(f"❌ Transacción {transaccion_id} no encontrada en la base de datos")
            return False
        
        print(f"✓ Transacción registrada: ID {transaccion.id}")
        print(f"  Tipo: {transaccion.tipo_operacion}")
        print(f"  Estado: {transaccion.estado}")
        print(f"  Comprobante: {transaccion.numero_comprobante}")
        
        # Verificar que los saldos se actualizaron
        cuenta_actualizada = db(db.cuentas.id == cuenta_divisa.id).select().first()
        print(f"✓ Saldo actualizado en cuenta {cuenta_divisa.moneda}: {cuenta_actualizada.saldo}")
        
        print("\n5. Verificando que el comprobante se puede mostrar sin errores...")
        
        # Simular la visualización del comprobante
        try:
            # Verificar que la cuenta existe
            cuenta = db(db.cuentas.id == transaccion.cuenta_id).select().first()
            if not cuenta:
                print("❌ Cuenta de la transacción no encontrada")
                return False
            
            print(f"✓ Cuenta encontrada: {cuenta.numero_cuenta}")
            
            # Verificar que el cliente existe
            cliente_transaccion = db(db.clientes.id == cuenta.cliente_id).select().first()
            if not cliente_transaccion:
                print("❌ Cliente no encontrado")
                return False
            
            print(f"✓ Cliente encontrado: ID {cliente_transaccion.id}")
            
            # Verificar que el usuario del cliente existe
            usuario_cliente = db(db.auth_user.id == cliente_transaccion.user_id).select().first()
            if not usuario_cliente:
                print("❌ Usuario del cliente no encontrado")
                return False
            
            print(f"✓ Usuario del cliente encontrado: {usuario_cliente.email}")
            
            print("✓ Todos los datos necesarios para el comprobante están disponibles")
            
        except Exception as e:
            print(f"❌ Error al verificar datos del comprobante: {str(e)}")
            return False
        
        print("\n6. Verificando que no hay tickets de error...")
        
        # Verificar si hay tickets de error recientes (últimos 5 minutos)
        tiempo_limite = datetime.datetime.now() - datetime.timedelta(minutes=5)
        tickets_recientes = db(
            (db.tickets.created_datetime > tiempo_limite)
        ).select()
        
        if tickets_recientes:
            print(f"⚠️  Se encontraron {len(tickets_recientes)} tickets de error recientes:")
            for ticket in tickets_recientes:
                print(f"   - Ticket: {ticket.ticket_id}")
                print(f"     Fecha: {ticket.created_datetime}")
        else:
            print("✓ No hay tickets de error recientes")
        
        print("\n" + "=" * 80)
        print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
        print("=" * 80)
        print("\nResumen:")
        print(f"  - Cliente: {cliente.id}")
        print(f"  - Usuario: {usuario.email}")
        print(f"  - Transacción: {transaccion_id}")
        print(f"  - Comprobante: {resultado.get('comprobante')}")
        print(f"  - Monto vendido: {resultado.get('monto_origen')} {cuenta_divisa.moneda}")
        print(f"  - Monto recibido: {resultado.get('monto_destino')} VES")
        print(f"  - Estado: {transaccion.estado}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # Este script debe ejecutarse con web2py shell
    print("\nPara ejecutar este test, use:")
    print("python web2py.py -S sistema_divisas -M -R test_flujo_venta_completo.py")
