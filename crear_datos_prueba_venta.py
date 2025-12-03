# -*- coding: utf-8 -*-
"""
Script para crear datos de prueba para el flujo de venta
"""

import datetime
from decimal import Decimal

print("=" * 80)
print("Creando datos de prueba para venta de divisas")
print("=" * 80)

try:
    # Verificar si ya existe un cliente de prueba
    cliente_prueba = db(db.clientes.cedula == 'V-12345678').select().first()
    
    if cliente_prueba:
        print(f"\n✓ Cliente de prueba ya existe: ID {cliente_prueba.id}")
    else:
        # Buscar o crear usuario de prueba
        usuario_prueba = db(db.auth_user.email == 'cliente.prueba@test.com').select().first()
        
        if not usuario_prueba:
            print("\nCreando usuario de prueba...")
            usuario_id = db.auth_user.insert(
                first_name='Cliente',
                last_name='Prueba',
                email='cliente.prueba@test.com',
                password=db.auth_user.password.validate('prueba123')[0]
            )
            usuario_prueba = db.auth_user[usuario_id]
            print(f"✓ Usuario creado: {usuario_prueba.email}")
            
            # Asignar rol de cliente
            grupo_cliente = db(db.auth_group.role == 'cliente').select().first()
            if not grupo_cliente:
                grupo_id = db.auth_group.insert(role='cliente', description='Cliente del sistema')
                grupo_cliente = db.auth_group[grupo_id]
            
            db.auth_membership.insert(
                user_id=usuario_prueba.id,
                group_id=grupo_cliente.id
            )
            print("✓ Rol de cliente asignado")
        else:
            print(f"\n✓ Usuario de prueba ya existe: {usuario_prueba.email}")
        
        # Crear cliente
        print("\nCreando perfil de cliente...")
        cliente_id = db.clientes.insert(
            user_id=usuario_prueba.id,
            cedula='V-12345678',
            fecha_registro=datetime.datetime.now()
        )
        cliente_prueba = db.clientes[cliente_id]
        print(f"✓ Cliente creado: ID {cliente_prueba.id}")
    
    # Verificar cuentas del cliente
    print("\nVerificando cuentas del cliente...")
    cuentas_existentes = db(
        (db.cuentas.cliente_id == cliente_prueba.id) &
        (db.cuentas.estado == 'activa')
    ).select()
    
    if cuentas_existentes:
        print(f"✓ El cliente ya tiene {len(cuentas_existentes)} cuenta(s)")
        for cuenta in cuentas_existentes:
            print(f"  - {cuenta.numero_cuenta}: {cuenta.moneda} - Saldo: {cuenta.saldo}")
    else:
        print("Creando cuentas de prueba...")
        
        # Crear cuenta VES
        numero_ves = f"VES-{cliente_prueba.id:08d}-001"
        cuenta_ves_id = db.cuentas.insert(
            cliente_id=cliente_prueba.id,
            numero_cuenta=numero_ves,
            tipo_cuenta='ahorro',
            moneda='VES',
            saldo=Decimal('100000.00'),
            estado='activa',
            fecha_creacion=datetime.datetime.now()
        )
        print(f"✓ Cuenta VES creada: {numero_ves} - Saldo: 100,000.00 VES")
        
        # Crear cuenta USD con saldo
        numero_usd = f"USD-{cliente_prueba.id:08d}-001"
        cuenta_usd_id = db.cuentas.insert(
            cliente_id=cliente_prueba.id,
            numero_cuenta=numero_usd,
            tipo_cuenta='ahorro',
            moneda='USD',
            saldo=Decimal('500.00'),
            estado='activa',
            fecha_creacion=datetime.datetime.now()
        )
        print(f"✓ Cuenta USD creada: {numero_usd} - Saldo: 500.00 USD")
        
        # Crear cuenta EUR con saldo
        numero_eur = f"EUR-{cliente_prueba.id:08d}-001"
        cuenta_eur_id = db.cuentas.insert(
            cliente_id=cliente_prueba.id,
            numero_cuenta=numero_eur,
            tipo_cuenta='ahorro',
            moneda='EUR',
            saldo=Decimal('300.00'),
            estado='activa',
            fecha_creacion=datetime.datetime.now()
        )
        print(f"✓ Cuenta EUR creada: {numero_eur} - Saldo: 300.00 EUR")
    
    db.commit()
    
    print("\n" + "=" * 80)
    print("✅ DATOS DE PRUEBA CREADOS EXITOSAMENTE")
    print("=" * 80)
    print("\nCredenciales de acceso:")
    print("  Email: cliente.prueba@test.com")
    print("  Password: prueba123")
    print("\nPuede ejecutar el test con:")
    print("  python web2py.py -S sistema_divisas -M -R test_flujo_venta_completo.py")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    db.rollback()
