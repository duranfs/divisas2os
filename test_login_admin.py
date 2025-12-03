# -*- coding: utf-8 -*-
"""
Verificar que el usuario admin puede acceder
"""

print("=" * 80)
print("VERIFICACIÓN DE ACCESO ADMINISTRATIVO")
print("=" * 80)

# Buscar usuario administrador
admin_user = db(db.auth_user.email == 'duranfs.2012@gmail.com').select().first()

if admin_user:
    print(f"\n✓ Usuario encontrado: {admin_user.email}")
    print(f"  ID: {admin_user.id}")
    print(f"  Nombre: {admin_user.first_name} {admin_user.last_name}")
    
    # Verificar roles
    memberships = db(db.auth_membership.user_id == admin_user.id).select()
    
    if memberships:
        print(f"\n✓ Roles asignados:")
        for membership in memberships:
            grupo = db(db.auth_group.id == membership.group_id).select().first()
            if grupo:
                print(f"  - {grupo.role}")
    else:
        print("\n⚠️  No tiene roles asignados")
        
        # Asignar rol de administrador
        grupo_admin = db(db.auth_group.role == 'administrador').select().first()
        if not grupo_admin:
            print("  Creando grupo administrador...")
            grupo_id = db.auth_group.insert(
                role='administrador',
                description='Administrador del sistema'
            )
            grupo_admin = db.auth_group[grupo_id]
        
        print(f"  Asignando rol de administrador...")
        db.auth_membership.insert(
            user_id=admin_user.id,
            group_id=grupo_admin.id
        )
        db.commit()
        print("  ✓ Rol asignado")
    
    # Verificar cliente asociado
    cliente = db(db.clientes.user_id == admin_user.id).select().first()
    if cliente:
        print(f"\n✓ Perfil de cliente: {cliente.cedula}")
        
        # Verificar cuentas
        cuentas = db(
            (db.cuentas.cliente_id == cliente.id) &
            (db.cuentas.estado == 'activa')
        ).select()
        
        print(f"✓ Cuentas activas: {len(cuentas)}")
        for cuenta in cuentas:
            print(f"  - {cuenta.numero_cuenta}: {cuenta.moneda} - Saldo: {cuenta.saldo}")
    else:
        print("\n⚠️  No tiene perfil de cliente")

else:
    print("\n❌ Usuario no encontrado")

print("\n" + "=" * 80)
print("INSTRUCCIONES PARA PROBAR:")
print("=" * 80)
print("\n1. Abrir navegador en: http://127.0.0.1:8000/divisas2os_multiple")
print(f"2. Login con: {admin_user.email if admin_user else 'N/A'}")
print("3. Password: prueba123")
print("4. Ir a: /divisas/vender")
print("5. Seleccionar cuenta USD y vender 50 USD")
print("6. Verificar que el comprobante se muestra correctamente")
print("\n" + "=" * 80)
