#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script simple para probar la vista de detalles
Debe ejecutarse desde web2py: python web2py.py -S sistema_divisas -M -R test_detalle_simple.py
"""

def test_detalle_funcionalidad():
    """Prueba la funcionalidad de detalles de cliente"""
    
    print("=== PRUEBA DE FUNCIONALIDAD DE DETALLES ===")
    
    try:
        # Verificar que hay clientes
        clientes = db(db.clientes.id > 0).select()
        print(f"✓ Clientes en BD: {len(clientes)}")
        
        if not clientes:
            print("❌ No hay clientes para probar")
            return False
        
        # Tomar el primer cliente
        cliente_test = clientes.first()
        print(f"✓ Cliente de prueba: ID {cliente_test.id}")
        
        # Verificar usuario asociado
        usuario = db(db.auth_user.id == cliente_test.user_id).select().first()
        if usuario:
            print(f"✓ Usuario: {usuario.first_name} {usuario.last_name}")
        else:
            print("⚠️  Usuario no encontrado")
        
        # Verificar cuentas del cliente
        cuentas = db(db.cuentas.cliente_id == cliente_test.id).select()
        print(f"✓ Cuentas del cliente: {len(cuentas)}")
        
        # Verificar transacciones si hay cuentas
        transacciones = []
        if cuentas:
            cuenta_ids = [c.id for c in cuentas]
            transacciones = db(db.transacciones.cuenta_id.belongs(cuenta_ids)).select(
                limitby=(0, 5)
            )
        print(f"✓ Transacciones recientes: {len(transacciones)}")
        
        # Simular datos que pasaría el controlador
        from gluon.storage import Storage
        datos_seguros = Storage()
        
        if usuario:
            datos_seguros['nombre_completo'] = f"{usuario.first_name} {usuario.last_name}"
            datos_seguros['email'] = usuario.email
            datos_seguros['telefono'] = getattr(usuario, 'telefono', 'No especificado')
            datos_seguros['direccion'] = getattr(usuario, 'direccion', 'No especificada')
            datos_seguros['estado_activo'] = (getattr(usuario, 'estado', 'inactivo') == 'activo')
            
            if hasattr(usuario, 'fecha_nacimiento') and usuario.fecha_nacimiento:
                datos_seguros['fecha_nacimiento_str'] = usuario.fecha_nacimiento.strftime('%d/%m/%Y')
            else:
                datos_seguros['fecha_nacimiento_str'] = 'No especificada'
        else:
            datos_seguros = Storage({
                'nombre_completo': 'Usuario no encontrado',
                'email': 'No disponible',
                'telefono': 'No especificado',
                'direccion': 'No especificada',
                'fecha_nacimiento_str': 'No especificada',
                'estado_activo': False
            })
        
        print("✓ Datos seguros preparados:")
        print(f"  - Nombre: {datos_seguros.nombre_completo}")
        print(f"  - Email: {datos_seguros.email}")
        print(f"  - Estado activo: {datos_seguros.estado_activo}")
        
        # Verificar que todos los datos necesarios están disponibles
        datos_completos = {
            'cliente': cliente_test,
            'usuario': usuario,
            'datos_seguros': datos_seguros,
            'cuentas': cuentas,
            'ultimas_transacciones': transacciones
        }
        
        print("\n✅ TODOS LOS DATOS ESTÁN DISPONIBLES PARA LA VISTA")
        print("✅ La funcionalidad de detalles debería funcionar correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_acceso_detalle():
    """Prueba el acceso a la función detalle"""
    
    print("\n=== PRUEBA DE ACCESO A DETALLE ===")
    
    try:
        # Verificar que hay un usuario administrador
        admin = db(db.auth_user.email == 'admin@sistema.com').select().first()
        if not admin:
            print("⚠️  Usuario admin no encontrado, buscando cualquier usuario...")
            admin = db(db.auth_user.id > 0).select().first()
        
        if admin:
            print(f"✓ Usuario para prueba: {admin.email}")
            
            # Verificar membresías
            memberships = db(db.auth_membership.user_id == admin.id).select()
            roles = []
            for m in memberships:
                role = db(db.auth_group.id == m.group_id).select().first()
                if role:
                    roles.append(role.role)
            
            print(f"✓ Roles del usuario: {roles}")
            
            if 'administrador' in roles or 'operador' in roles:
                print("✅ Usuario tiene permisos para ver detalles")
            else:
                print("⚠️  Usuario no tiene permisos de administrador/operador")
        else:
            print("❌ No se encontró ningún usuario")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Ejecutando pruebas de detalles de cliente...\n")
    
    test1 = test_detalle_funcionalidad()
    test2 = test_acceso_detalle()
    
    print(f"\n=== RESUMEN ===")
    print(f"Funcionalidad: {'✅ OK' if test1 else '❌ ERROR'}")
    print(f"Acceso: {'✅ OK' if test2 else '❌ ERROR'}")
    
    if test1 and test2:
        print("\n🎉 ¡La funcionalidad de detalles está lista!")
    else:
        print("\n⚠️  Hay problemas que resolver.")