#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Diagnóstico profundo del problema de clientes
"""

import os

def diagnostico_profundo():
    """Diagnóstico completo del problema"""
    
    print("=" * 70)
    print("🔍 DIAGNÓSTICO PROFUNDO: Problema de Clientes")
    print("=" * 70)
    
    print("VAMOS A VERIFICAR PASO A PASO:")
    
    print("\n1. ¿EL CLIENTE SE REGISTRA CORRECTAMENTE?")
    print("   - ¿Se crea el usuario en auth_user?")
    print("   - ¿Se crea el registro en tabla clientes?")
    print("   - ¿Se crea la cuenta bancaria?")
    print("   - ¿Se asigna el rol de cliente?")
    
    print("\n2. ¿EL LOGIN FUNCIONA?")
    print("   - ¿Puede hacer login con email/contraseña?")
    print("   - ¿Se autentica correctamente?")
    print("   - ¿auth.user.id tiene valor?")
    
    print("\n3. ¿LOS DATOS ESTÁN EN LA BASE DE DATOS?")
    print("   - ¿Existe en tabla auth_user?")
    print("   - ¿Existe en tabla clientes?")
    print("   - ¿Existe en tabla cuentas?")
    print("   - ¿Tiene rol asignado en auth_membership?")
    
    print("\n4. ¿QUÉ PASA CUANDO ACCEDE A CUENTAS?")
    print("   - ¿A qué URL está accediendo?")
    print("   - ¿Qué función del controlador se ejecuta?")
    print("   - ¿Encuentra el registro de cliente?")
    print("   - ¿Encuentra las cuentas?")
    
    print("\n" + "=" * 70)
    print("CREANDO FUNCIÓN DE DEBUG TEMPORAL")
    print("=" * 70)
    
    debug_function = '''
# FUNCIÓN DE DEBUG TEMPORAL - Agregar a controllers/cuentas.py

@auth.requires_login()
def debug_cliente():
    """Función temporal para debuggear problema de clientes"""
    
    debug_info = []
    
    # 1. Información del usuario autenticado
    debug_info.append(f"Usuario autenticado: {auth.user.id if auth.user else 'None'}")
    debug_info.append(f"Email del usuario: {auth.user.email if auth.user else 'None'}")
    
    # 2. Buscar en tabla clientes
    if auth.user:
        cliente_record = db(db.clientes.user_id == auth.user.id).select().first()
        debug_info.append(f"Cliente encontrado: {cliente_record.id if cliente_record else 'None'}")
        
        if cliente_record:
            # 3. Buscar cuentas del cliente
            cuentas = db(db.cuentas.cliente_id == cliente_record.id).select()
            debug_info.append(f"Cuentas encontradas: {len(cuentas)}")
            
            for cuenta in cuentas:
                debug_info.append(f"  - Cuenta: {cuenta.numero_cuenta}, VES: {cuenta.saldo_ves}")
        
        # 4. Verificar roles
        try:
            user_roles = get_user_roles()
            debug_info.append(f"Roles del usuario: {user_roles}")
        except Exception as e:
            debug_info.append(f"Error obteniendo roles: {str(e)}")
        
        # 5. Verificar membresías directamente
        memberships = db(db.auth_membership.user_id == auth.user.id).select(
            db.auth_membership.ALL,
            db.auth_group.role,
            join=db.auth_group.on(db.auth_membership.group_id == db.auth_group.id)
        )
        debug_info.append(f"Membresías directas: {[m.auth_group.role for m in memberships]}")
    
    return dict(debug_info=debug_info)
'''
    
    print("CÓDIGO PARA AGREGAR:")
    print("-" * 50)
    print(debug_function)
    print("-" * 50)
    
    print("\nCREAR VISTA DE DEBUG:")
    
    debug_view = '''
<!-- Crear archivo: views/cuentas/debug_cliente.html -->

{{extend 'layout.html'}}

<div class="container">
    <h1>Debug de Cliente</h1>
    
    <div class="card">
        <div class="card-header">
            <h3>Información de Debug</h3>
        </div>
        <div class="card-body">
            {{if debug_info:}}
                {{for info in debug_info:}}
                    <p><code>{{=info}}</code></p>
                {{pass}}
            {{else:}}
                <p>No hay información de debug</p>
            {{pass}}
        </div>
    </div>
    
    <div class="mt-3">
        <a href="{{=URL('default', 'dashboard')}}" class="btn btn-primary">Volver</a>
    </div>
</div>
'''
    
    print("VISTA DE DEBUG:")
    print("-" * 50)
    print(debug_view)
    print("-" * 50)
    
    print("\nINSTRUCCIONES:")
    print("1. Agrega la función debug_cliente() al controlador cuentas.py")
    print("2. Crea el archivo views/cuentas/debug_cliente.html con el contenido")
    print("3. Haz login como cliente")
    print("4. Ve a: /cuentas/debug_cliente")
    print("5. Revisa qué información aparece")
    print("6. Comparte los resultados para identificar el problema exacto")

if __name__ == "__main__":
    diagnostico_profundo()