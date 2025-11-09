#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Prueba para diagnosticar problemas en la vista de todas las cuentas
Debe ejecutarse desde web2py: python web2py.py -S divisas2os -M -R test_cuentas_listar_todas.py
"""

def test_cuentas_listar_todas():
    """Prueba la funcionalidad de listar todas las cuentas"""
    
    print("=== DIAGNÓSTICO DE TODAS LAS CUENTAS ===")
    
    try:
        # Verificar que hay cuentas en la base de datos
        total_cuentas = db(db.cuentas.id > 0).count()
        print(f"✓ Total de cuentas en BD: {total_cuentas}")
        
        if total_cuentas == 0:
            print("⚠️  No hay cuentas en la base de datos")
            return False
        
        # Verificar que hay clientes asociados
        total_clientes = db(db.clientes.id > 0).count()
        print(f"✓ Total de clientes en BD: {total_clientes}")
        
        # Verificar usuarios asociados
        total_usuarios = db(db.auth_user.id > 0).count()
        print(f"✓ Total de usuarios en BD: {total_usuarios}")
        
        # Probar la consulta JOIN que usa el controlador
        query = (db.cuentas.cliente_id == db.clientes.id) & \
                (db.clientes.user_id == db.auth_user.id)
        
        cuentas_join = db(query).select(
            db.cuentas.ALL,
            db.clientes.cedula,
            db.auth_user.first_name,
            db.auth_user.last_name,
            db.auth_user.email,
            limitby=(0, 5)
        )
        
        print(f"✓ Cuentas con JOIN: {len(cuentas_join)}")
        
        if len(cuentas_join) > 0:
            cuenta_ejemplo = cuentas_join[0]
            print(f"✓ Ejemplo de cuenta:")
            print(f"  - ID: {cuenta_ejemplo.cuentas.id}")
            print(f"  - Número: {cuenta_ejemplo.cuentas.numero_cuenta}")
            print(f"  - Cliente: {cuenta_ejemplo.auth_user.first_name} {cuenta_ejemplo.auth_user.last_name}")
            print(f"  - Cédula: {cuenta_ejemplo.clientes.cedula}")
            print(f"  - Estado: {cuenta_ejemplo.cuentas.estado}")
        
        # Verificar estadísticas
        stats = {
            'total': db(db.cuentas.id > 0).count(),
            'activas': db(db.cuentas.estado == 'activa').count(),
            'inactivas': db(db.cuentas.estado == 'inactiva').count(),
            'corrientes': db(db.cuentas.tipo_cuenta == 'corriente').count(),
            'ahorros': db(db.cuentas.tipo_cuenta == 'ahorro').count()
        }
        
        print(f"✓ Estadísticas:")
        for key, value in stats.items():
            print(f"  - {key}: {value}")
        
        # Verificar permisos de usuario administrador
        admin_user = db(db.auth_user.email == 'admin@sistema.com').select().first()
        if admin_user:
            print(f"✓ Usuario admin encontrado: {admin_user.email}")
            
            # Verificar membresías
            memberships = db(db.auth_membership.user_id == admin_user.id).select()
            roles = []
            for m in memberships:
                role = db(db.auth_group.id == m.group_id).select().first()
                if role:
                    roles.append(role.role)
            
            print(f"✓ Roles del admin: {roles}")
            
            if 'administrador' in roles:
                print("✅ Usuario tiene permisos de administrador")
            else:
                print("⚠️  Usuario no tiene rol de administrador")
        else:
            print("⚠️  Usuario admin no encontrado")
        
        print("\n✅ DIAGNÓSTICO COMPLETADO - Los datos están disponibles")
        return True
        
    except Exception as e:
        print(f"❌ Error durante el diagnóstico: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_vista_listar_todas():
    """Verifica que la vista esté correctamente implementada"""
    
    print("\n=== VERIFICACIÓN DE VISTA ===")
    
    try:
        import os
        vista_path = "views/cuentas/listar_todas.html"
        
        if not os.path.exists(vista_path):
            print(f"❌ Vista no encontrada: {vista_path}")
            return False
        
        with open(vista_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        print(f"✓ Vista encontrada: {vista_path}")
        print(f"✓ Tamaño: {len(contenido)} caracteres")
        
        # Verificar elementos clave
        elementos = [
            ("{{extend 'layout.html'}}", "Layout"),
            ("Todas las Cuentas", "Título"),
            ("{{for cuenta in cuentas:}}", "Loop de cuentas"),
            ("{{=cuenta.cuentas.numero_cuenta}}", "Número de cuenta"),
            ("{{=cuenta.auth_user.first_name}}", "Nombre del cliente"),
            ("{{=cuenta.clientes.cedula}}", "Cédula"),
            ("{{if cuentas:}}", "Condicional de cuentas"),
            ("{{else:}}", "Manejo de estado vacío")
        ]
        
        encontrados = 0
        for elemento, descripcion in elementos:
            if elemento in contenido:
                print(f"✓ {descripcion}: OK")
                encontrados += 1
            else:
                print(f"❌ {descripcion}: FALTANTE")
        
        puntuacion = (encontrados / len(elementos)) * 100
        print(f"\nPuntuación de vista: {puntuacion:.1f}%")
        
        return puntuacion >= 80
        
    except Exception as e:
        print(f"❌ Error al verificar vista: {str(e)}")
        return False

if __name__ == "__main__":
    print("DIAGNÓSTICO DE FUNCIONALIDAD DE TODAS LAS CUENTAS")
    print("=" * 60)
    
    test1 = test_cuentas_listar_todas()
    test2 = test_vista_listar_todas()
    
    print(f"\n{'=' * 60}")
    print("RESUMEN DEL DIAGNÓSTICO")
    print(f"{'=' * 60}")
    
    print(f"Datos y consultas: {'✅ OK' if test1 else '❌ ERROR'}")
    print(f"Vista: {'✅ OK' if test2 else '❌ ERROR'}")
    
    if test1 and test2:
        print("\n🎉 ¡La funcionalidad debería estar funcionando correctamente!")
        print("📋 Si aún hay problemas, puede ser:")
        print("   1. Problema de permisos de usuario")
        print("   2. Error en el servidor web")
        print("   3. Cache del navegador")
    else:
        print("\n⚠️  Se encontraron problemas que necesitan corrección")
    
    print(f"{'=' * 60}")