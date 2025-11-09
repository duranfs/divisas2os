#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar el rol del usuario y qué dashboard debería ver
"""

import sqlite3

def verificar_rol_usuario():
    """Verificar roles de usuarios y qué dashboard deberían ver"""
    print("🔍 VERIFICANDO ROLES DE USUARIO")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect("databases/storage.sqlite")
        cursor = conn.cursor()
        
        # 1. Mostrar todos los usuarios y sus roles
        print("👥 1. USUARIOS Y SUS ROLES")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                u.id,
                u.email,
                u.first_name,
                u.last_name,
                u.estado,
                g.role as rol
            FROM auth_user u
            LEFT JOIN auth_membership m ON u.id = m.user_id
            LEFT JOIN auth_group g ON m.group_id = g.id
            ORDER BY u.id
        """)
        
        usuarios = cursor.fetchall()
        
        for usuario in usuarios:
            user_id, email, first_name, last_name, estado, rol = usuario
            nombre_completo = f"{first_name} {last_name}"
            rol_display = rol if rol else "Sin rol"
            
            print(f"   👤 ID: {user_id}")
            print(f"      Email: {email}")
            print(f"      Nombre: {nombre_completo}")
            print(f"      Estado: {estado}")
            print(f"      Rol: {rol_display}")
            
            # Determinar qué dashboard debería ver
            if rol == 'administrador':
                dashboard_tipo = "🔧 Dashboard Administrativo (con tasas)"
            elif rol == 'operador':
                dashboard_tipo = "🔧 Dashboard Administrativo (con tasas)"
            elif rol == 'cliente':
                dashboard_tipo = "👤 Dashboard Cliente (con tasas y saldos)"
            else:
                dashboard_tipo = "📝 Dashboard Básico (completar registro)"
            
            print(f"      Dashboard: {dashboard_tipo}")
            print()
        
        # 2. Verificar si hay clientes registrados
        print("👤 2. VERIFICANDO CLIENTES REGISTRADOS")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                c.id,
                u.email,
                u.first_name,
                u.last_name,
                c.cedula
            FROM clientes c
            JOIN auth_user u ON c.user_id = u.id
        """)
        
        clientes = cursor.fetchall()
        
        if clientes:
            print(f"   📊 Total de clientes: {len(clientes)}")
            for cliente in clientes:
                cliente_id, email, first_name, last_name, cedula = cliente
                print(f"      • {first_name} {last_name} ({email}) - Cédula: {cedula}")
        else:
            print("   ⚠️ No hay clientes registrados")
        
        # 3. Simular lógica del dashboard
        print(f"\n🎯 3. SIMULANDO LÓGICA DEL DASHBOARD")
        print("-" * 40)
        
        for usuario in usuarios:
            user_id, email, first_name, last_name, estado, rol = usuario
            
            print(f"\n   👤 Usuario: {first_name} {last_name} ({email})")
            
            # Simular la lógica de dashboard()
            # 1. Verificar si es cliente
            cursor.execute("SELECT id FROM clientes WHERE user_id = ?", (user_id,))
            es_cliente = cursor.fetchone()
            
            if es_cliente:
                print(f"      ✅ Es cliente → Dashboard Cliente")
                print(f"         • Mostrará saldos VES, USD, EUR, USDT")
                print(f"         • Mostrará widget de tasas actuales")
            else:
                # 2. Verificar si es admin/operador
                if rol in ['administrador', 'operador']:
                    print(f"      ✅ Es {rol} → Dashboard Administrativo")
                    print(f"         • Mostrará estadísticas del sistema")
                    print(f"         • Mostrará widget de tasas BCV")
                else:
                    print(f"      ⚠️ Sin rol específico → Dashboard Básico")
                    print(f"         • Mostrará mensaje de completar registro")
        
        # 4. Verificar tasas disponibles
        print(f"\n📊 4. VERIFICANDO TASAS DISPONIBLES")
        print("-" * 40)
        
        cursor.execute("""
            SELECT id, fecha, hora, usd_ves, eur_ves, usdt_ves, activa
            FROM tasas_cambio 
            WHERE activa = 1
            LIMIT 1
        """)
        
        tasa_activa = cursor.fetchone()
        
        if tasa_activa:
            print("   ✅ Hay tasas activas disponibles:")
            print(f"      USD/VES: {tasa_activa[3]}")
            print(f"      EUR/VES: {tasa_activa[4]}")
            print(f"      USDT/VES: {tasa_activa[5]}")
            print("   → Los dashboards deberían mostrar las tasas")
        else:
            print("   ❌ No hay tasas activas")
            print("   → Los dashboards mostrarán 'No hay tasas disponibles'")
        
        conn.close()
        
        # 5. Recomendaciones
        print(f"\n" + "=" * 60)
        print("📋 RECOMENDACIONES")
        print("=" * 60)
        
        print("\n🔧 Para ver el widget de tasas:")
        print("   1. Si eres administrador: Deberías ver 'Tasas BCV' en la esquina superior derecha")
        print("   2. Si eres cliente: Deberías ver 'Tasas Actuales' en la columna izquierda")
        print("   3. Si no ves tasas: Verificar que tengas el rol correcto asignado")
        
        print("\n👤 Para asignar rol de administrador:")
        print("   • Ejecutar: python tests/assign_admin_role.py")
        print("   • O usar el script de diagnóstico de web2py")
        
        print("\n🌐 Para acceder al dashboard:")
        print("   • URL: http://127.0.0.1:8000/divisas2os")
        print("   • Login con tu email y contraseña")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        return False

if __name__ == '__main__':
    verificar_rol_usuario()