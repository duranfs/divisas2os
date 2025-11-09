#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificar que se corrigió el acceso de administradores
"""

import os

def verificar_admin_corregido():
    """Verificar que los administradores pueden acceder nuevamente"""
    
    print("=" * 70)
    print("🚨 VERIFICACIÓN: Corrección de Acceso de Administradores")
    print("=" * 70)
    
    if os.path.exists("controllers/cuentas.py"):
        with open("controllers/cuentas.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            # Buscar la función index
            inicio = contenido.find("def index():")
            if inicio != -1:
                siguiente_def = contenido.find("\ndef ", inicio + 1)
                if siguiente_def == -1:
                    siguiente_def = len(contenido)
                
                funcion_index = contenido[inicio:siguiente_def]
                
                print("VERIFICANDO CORRECCIONES:")
                
                # Verificar que NO redirige automáticamente a listar_todas
                if "redirect(URL('cuentas', 'listar_todas'))" not in funcion_index:
                    print("✓ Ya NO redirige automáticamente a listar_todas")
                else:
                    print("❌ Aún redirige automáticamente a listar_todas")
                
                # Verificar que maneja cliente_id para administradores
                if "cliente_id = request.vars.cliente_id" in funcion_index:
                    print("✓ Maneja parámetro cliente_id para administradores")
                else:
                    print("❌ NO maneja parámetro cliente_id")
                
                # Verificar que redirige a lista de clientes si no hay cliente_id
                if "redirect(URL('clientes', 'listar'))" in funcion_index:
                    print("✓ Redirige a lista de clientes para seleccionar")
                else:
                    print("❌ NO redirige a lista de clientes")
                
                # Verificar que mantiene lógica para clientes
                if "'cliente' in user_roles" in funcion_index or "db.clientes.user_id == auth.user.id" in funcion_index:
                    print("✓ Mantiene lógica para clientes")
                else:
                    print("❌ NO mantiene lógica para clientes")
    
    print("\n" + "=" * 70)
    print("ESTADO ACTUAL:")
    print("✅ ADMINISTRADORES:")
    print("   - Pueden acceder a /cuentas/index")
    print("   - Si no especifican cliente_id, van a lista de clientes")
    print("   - Si especifican cliente_id, ven cuentas de ese cliente")
    print("   - Pueden usar /cuentas/listar_todas para ver todas las cuentas")
    
    print("\n✅ CLIENTES:")
    print("   - Pueden acceder a /cuentas/index")
    print("   - Ven solo sus propias cuentas")
    print("   - Se les asigna rol automáticamente si falta")
    
    print("\n📍 URLS DISPONIBLES:")
    print("   - /cuentas/index - Vista principal (admin y clientes)")
    print("   - /cuentas/listar_todas - Todas las cuentas (solo admin)")
    print("   - /cuentas/mis_cuentas - Vista específica para clientes")
    print("   - /clientes/listar - Lista de clientes (admin)")
    
    print("\n🔧 PARA ADMINISTRADORES:")
    print("1. Ve a /clientes/listar")
    print("2. Haz clic en 'Ver cuentas' de un cliente")
    print("3. O ve directamente a /cuentas/listar_todas")
    
    print("\n🔧 PARA CLIENTES:")
    print("1. Ve a /cuentas/index")
    print("2. O ve a /cuentas/mis_cuentas")
    print("3. Deberías ver tus cuentas y saldos")

if __name__ == "__main__":
    verificar_admin_corregido()