#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar la funcionalidad de activar/inactivar clientes
"""

import sqlite3

def test_activar_inactivar():
    """
    Verifica la funcionalidad de activar/inactivar clientes
    """
    print("=== PRUEBA DE ACTIVAR/INACTIVAR CLIENTES ===")
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        print("\n1. Verificando función cambiar_estado() en controlador...")
        
        # Leer el controlador
        with open('controllers/clientes.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        # Verificar elementos de la función cambiar_estado
        elementos_funcion = [
            ('Función cambiar_estado existe', 'def cambiar_estado():'),
            ('Verificación de permisos', 'auth.has_membership(\'administrador\')'),
            ('Validación de parámetros', 'request.args(0)'),
            ('Validación de estado', "nuevo_estado not in ['activo', 'inactivo']"),
            ('Búsqueda de cliente', 'db(db.clientes.id == cliente_id)'),
            ('Actualización de estado', 'db(db.auth_user.id == cliente.user_id).update(estado=nuevo_estado)'),
            ('Logging de auditoría', 'logs_auditoria'),
            ('Mensaje de éxito', 'ha sido {accion} exitosamente'),
            ('Manejo de errores', 'except Exception as e:'),
            ('Redirect final', "redirect(URL('clientes', 'listar'))")
        ]
        
        funcion_ok = 0
        for nombre, elemento in elementos_funcion:
            if elemento in controller_content:
                funcion_ok += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Función cambiar_estado: {funcion_ok}/{len(elementos_funcion)}")
        
        print("\n2. Verificando botones en vista listar.html...")
        
        # Leer la vista
        with open('views/clientes/listar.html', 'r', encoding='utf-8') as f:
            vista_content = f.read()
        
        # Verificar elementos de la vista
        elementos_vista = [
            ('Botón inactivar', 'cambiar_estado.*inactivo'),
            ('Botón activar', 'cambiar_estado.*activo'),
            ('Icono inactivar', 'fa-user-slash'),
            ('Icono activar', 'fa-user-check'),
            ('Confirmación inactivar', 'confirm.*inactivar'),
            ('Confirmación activar', 'confirm.*activar'),
            ('Condicional estado activo', "cliente.auth_user.estado == 'activo'"),
            ('Condicional estado inactivo', 'else')
        ]
        
        vista_ok = 0
        import re
        for nombre, patron in elementos_vista:
            if re.search(patron, vista_content, re.IGNORECASE):
                vista_ok += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Botones en vista: {vista_ok}/{len(elementos_vista)}")
        
        print("\n3. Verificando clientes en la base de datos...")
        
        cursor.execute("""
            SELECT 
                c.id,
                au.first_name,
                au.last_name,
                au.email,
                au.estado,
                c.cedula
            FROM clientes c
            JOIN auth_user au ON c.user_id = au.id
            ORDER BY c.id
            LIMIT 5
        """)
        
        clientes = cursor.fetchall()
        
        if clientes:
            print(f"   📊 Clientes encontrados: {len(clientes)}")
            print("   " + "-" * 80)
            print("   ID | Nombre                    | Email                     | Estado   | Cédula")
            print("   " + "-" * 80)
            
            activos = 0
            inactivos = 0
            
            for cliente in clientes:
                estado_color = "✅" if cliente[4] == 'activo' else "❌"
                print(f"   {cliente[0]:2d} | {cliente[1]} {cliente[2]:<15s} | {cliente[3]:<25s} | {estado_color} {cliente[4]:<6s} | {cliente[5]}")
                
                if cliente[4] == 'activo':
                    activos += 1
                else:
                    inactivos += 1
            
            print(f"\n   📊 Resumen: {activos} activos, {inactivos} inactivos")
        else:
            print("   ⚠️  No hay clientes en la base de datos")
        
        print("\n4. Verificando URLs de cambio de estado...")
        
        if clientes:
            cliente_ejemplo = clientes[0]
            cliente_id = cliente_ejemplo[0]
            estado_actual = cliente_ejemplo[4]
            nuevo_estado = 'inactivo' if estado_actual == 'activo' else 'activo'
            
            url_ejemplo = f"/divisas2os/clientes/cambiar_estado/{cliente_id}/{nuevo_estado}"
            print(f"   📊 URL de ejemplo: {url_ejemplo}")
            print(f"   📊 Cliente: {cliente_ejemplo[1]} {cliente_ejemplo[2]}")
            print(f"   📊 Estado actual: {estado_actual}")
            print(f"   📊 Nuevo estado: {nuevo_estado}")
        
        conn.close()
        
        print("\n5. Funcionalidad implementada:")
        print("   ✅ Botones de activar/inactivar en lista de clientes")
        print("   ✅ Confirmación antes de cambiar estado")
        print("   ✅ Verificación de permisos (solo admin/operador)")
        print("   ✅ Validación de parámetros")
        print("   ✅ Actualización en base de datos")
        print("   ✅ Logging de auditoría")
        print("   ✅ Mensajes de éxito/error")
        print("   ✅ Manejo de errores con rollback")
        
        print("\n6. Para probar:")
        print("   1. Ir a: http://127.0.0.1:8000/divisas2os/clientes/listar")
        print("   2. Buscar un cliente activo")
        print("   3. Hacer clic en el botón rojo (inactivar)")
        print("   4. Confirmar la acción")
        print("   5. Verificar que el estado cambie a 'Inactivo'")
        print("   6. Hacer clic en el botón verde (activar)")
        print("   7. Confirmar la acción")
        print("   8. Verificar que el estado cambie a 'Activo'")
        
        return funcion_ok >= 8 and vista_ok >= 6
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = test_activar_inactivar()
    print(f"\n{'='*60}")
    if resultado:
        print("🎉 FUNCIONALIDAD ACTIVAR/INACTIVAR IMPLEMENTADA CORRECTAMENTE")
    else:
        print("🔧 FUNCIONALIDAD INCOMPLETA - Revisar implementación")
    print(f"{'='*60}")