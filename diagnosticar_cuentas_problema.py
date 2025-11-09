#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Diagnóstico del problema de "Todas las Cuentas"
Debe ejecutarse desde web2py: python web2py.py -S divisas2os -M -R diagnosticar_cuentas_problema.py
"""

def diagnosticar_problema_cuentas():
    """Diagnostica por qué no aparecen las cuentas"""
    
    print("=== DIAGNÓSTICO DEL PROBLEMA DE CUENTAS ===")
    
    try:
        # 1. Verificar que hay datos en las tablas
        print("1. VERIFICANDO DATOS EN TABLAS:")
        
        total_cuentas = db(db.cuentas.id > 0).count()
        total_clientes = db(db.clientes.id > 0).count()
        total_usuarios = db(db.auth_user.id > 0).count()
        
        print(f"   - Cuentas: {total_cuentas}")
        print(f"   - Clientes: {total_clientes}")
        print(f"   - Usuarios: {total_usuarios}")
        
        if total_cuentas == 0:
            print("❌ PROBLEMA: No hay cuentas en la base de datos")
            return False
        
        # 2. Verificar la consulta JOIN
        print("\n2. VERIFICANDO CONSULTA JOIN:")
        
        query = (db.cuentas.cliente_id == db.clientes.id) & \
                (db.clientes.user_id == db.auth_user.id)
        
        cuentas_join = db(query).select(
            db.cuentas.ALL,
            db.clientes.cedula,
            db.auth_user.first_name,
            db.auth_user.last_name,
            db.auth_user.email,
            limitby=(0, 3)
        )
        
        print(f"   - Cuentas con JOIN: {len(cuentas_join)}")
        
        if len(cuentas_join) == 0:
            print("❌ PROBLEMA: El JOIN no devuelve resultados")
            
            # Verificar relaciones
            print("\n   Verificando relaciones:")
            
            # Verificar cuentas sin cliente
            cuentas_sin_cliente = db(~db.cuentas.cliente_id.belongs(db(db.clientes.id > 0)._select(db.clientes.id))).select()
            print(f"   - Cuentas sin cliente válido: {len(cuentas_sin_cliente)}")
            
            # Verificar clientes sin usuario
            clientes_sin_usuario = db(~db.clientes.user_id.belongs(db(db.auth_user.id > 0)._select(db.auth_user.id))).select()
            print(f"   - Clientes sin usuario válido: {len(clientes_sin_usuario)}")
            
            return False
        else:
            print("✓ JOIN funciona correctamente")
            for cuenta in cuentas_join:
                print(f"   - Cuenta {cuenta.cuentas.numero_cuenta}: {cuenta.auth_user.first_name} {cuenta.auth_user.last_name}")
        
        # 3. Verificar permisos de usuario
        print("\n3. VERIFICANDO PERMISOS:")
        
        # Buscar usuario administrador
        admin_users = db(db.auth_membership.group_id.belongs(
            db(db.auth_group.role == 'administrador')._select(db.auth_group.id)
        )).select(db.auth_membership.user_id, distinct=True)
        
        print(f"   - Usuarios con rol administrador: {len(admin_users)}")
        
        if len(admin_users) == 0:
            print("❌ PROBLEMA: No hay usuarios con rol administrador")
            return False
        
        # 4. Simular la función del controlador
        print("\n4. SIMULANDO FUNCIÓN DEL CONTROLADOR:")
        
        try:
            # Simular parámetros por defecto
            buscar = ''
            numero_cuenta = ''
            estado = 'todos'
            tipo = 'todos'
            saldo_min = ''
            saldo_max = ''
            moneda_saldo = 'VES'
            page = 1
            
            # Query base
            query = (db.cuentas.cliente_id == db.clientes.id) & \
                    (db.clientes.user_id == db.auth_user.id)
            
            # Paginación
            items_per_page = 25
            
            cuentas = db(query).select(
                db.cuentas.ALL,
                db.clientes.cedula,
                db.auth_user.first_name,
                db.auth_user.last_name,
                db.auth_user.email,
                orderby=~db.cuentas.fecha_creacion,
                limitby=((page-1)*items_per_page, page*items_per_page)
            )
            
            print(f"   - Cuentas obtenidas: {len(cuentas)}")
            
            if len(cuentas) > 0:
                print("✓ La consulta del controlador funciona")
                return True
            else:
                print("❌ PROBLEMA: La consulta del controlador no devuelve datos")
                return False
                
        except Exception as e:
            print(f"❌ ERROR en simulación del controlador: {str(e)}")
            return False
        
    except Exception as e:
        print(f"❌ ERROR GENERAL: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def crear_datos_prueba():
    """Crea datos de prueba si no existen"""
    
    print("\n=== CREANDO DATOS DE PRUEBA ===")
    
    try:
        # Verificar si ya hay datos
        if db(db.cuentas.id > 0).count() > 0:
            print("✓ Ya existen cuentas en el sistema")
            return True
        
        print("Creando datos de prueba...")
        
        # Crear usuario de prueba
        user_id = db.auth_user.insert(
            first_name='Cliente',
            last_name='Prueba',
            email='cliente.prueba@test.com',
            password=db.auth_user.password.validate('test123')[0]
        )
        
        # Crear cliente de prueba
        cliente_id = db.clientes.insert(
            user_id=user_id,
            cedula='V-12345678',
            fecha_registro=datetime.now()
        )
        
        # Crear cuenta de prueba
        cuenta_id = db.cuentas.insert(
            cliente_id=cliente_id,
            numero_cuenta='20011234567890123456',
            tipo_cuenta='corriente',
            saldo_ves=1000.00,
            saldo_usd=50.00,
            saldo_eur=25.00,
            saldo_usdt=30.00,
            estado='activa',
            fecha_creacion=datetime.now()
        )
        
        db.commit()
        
        print(f"✓ Datos de prueba creados:")
        print(f"   - Usuario ID: {user_id}")
        print(f"   - Cliente ID: {cliente_id}")
        print(f"   - Cuenta ID: {cuenta_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear datos de prueba: {str(e)}")
        db.rollback()
        return False

if __name__ == "__main__":
    print("DIAGNÓSTICO DEL PROBLEMA DE TODAS LAS CUENTAS")
    print("=" * 60)
    
    # Importar datetime
    from datetime import datetime
    
    # Ejecutar diagnóstico
    resultado = diagnosticar_problema_cuentas()
    
    if not resultado:
        print("\n" + "=" * 60)
        print("INTENTANDO CREAR DATOS DE PRUEBA")
        print("=" * 60)
        
        crear_datos_prueba()
        
        # Volver a diagnosticar
        print("\n" + "=" * 60)
        print("DIAGNÓSTICO DESPUÉS DE CREAR DATOS")
        print("=" * 60)
        
        resultado = diagnosticar_problema_cuentas()
    
    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    
    if resultado:
        print("✅ EL PROBLEMA ESTÁ RESUELTO")
        print("📋 La página de Todas las Cuentas debería funcionar ahora")
    else:
        print("❌ EL PROBLEMA PERSISTE")
        print("📋 Revisar los errores mostrados arriba")
    
    print("=" * 60)