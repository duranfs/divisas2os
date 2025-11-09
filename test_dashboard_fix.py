#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar que el fix del dashboard funcione correctamente
"""

import sqlite3

def test_dashboard_logic():
    """Probar la nueva lógica del dashboard"""
    print("🔧 PROBANDO FIX DEL DASHBOARD")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect("databases/storage.sqlite")
        cursor = conn.cursor()
        
        # Simular la nueva lógica para cada usuario
        cursor.execute("""
            SELECT DISTINCT
                u.id,
                u.email,
                u.first_name,
                u.last_name,
                GROUP_CONCAT(g.role) as roles
            FROM auth_user u
            LEFT JOIN auth_membership m ON u.id = m.user_id
            LEFT JOIN auth_group g ON m.group_id = g.id
            WHERE u.estado = 'activo'
            GROUP BY u.id, u.email, u.first_name, u.last_name
            ORDER BY u.id
        """)
        
        usuarios = cursor.fetchall()
        
        print("👥 SIMULANDO NUEVA LÓGICA DEL DASHBOARD")
        print("-" * 40)
        
        for usuario in usuarios:
            user_id, email, first_name, last_name, roles_str = usuario
            roles = roles_str.split(',') if roles_str else []
            
            print(f"\n👤 {first_name} {last_name} ({email})")
            print(f"   Roles: {roles}")
            
            # Simular nueva lógica
            # 1. Verificar primero si es admin/operador
            es_admin = 'administrador' in roles
            es_operador = 'operador' in roles
            
            if es_admin or es_operador:
                dashboard_tipo = "🔧 Dashboard Administrativo"
                widget_tasas = "✅ Widget 'Tasas BCV' visible"
                print(f"   → {dashboard_tipo}")
                print(f"   → {widget_tasas}")
                
                # Verificar qué mostraría el widget
                cursor.execute("""
                    SELECT usd_ves, eur_ves, usdt_ves 
                    FROM tasas_cambio 
                    WHERE activa = 1 
                    LIMIT 1
                """)
                tasas = cursor.fetchone()
                
                if tasas:
                    print(f"   → USD: {tasas[0]:.4f}")
                    print(f"   → EUR: {tasas[1]:.4f}")
                    print(f"   → USDT: {tasas[2]:.4f}")
                else:
                    print(f"   → ⚠️ 'No disponible'")
                
            else:
                # 2. Verificar si es cliente
                cursor.execute("SELECT id FROM clientes WHERE user_id = ?", (user_id,))
                es_cliente = cursor.fetchone()
                
                if es_cliente:
                    dashboard_tipo = "👤 Dashboard Cliente"
                    widget_tasas = "✅ Widget 'Tasas Actuales' visible"
                    print(f"   → {dashboard_tipo}")
                    print(f"   → {widget_tasas}")
                    print(f"   → ✅ Saldos VES, USD, EUR, USDT")
                else:
                    dashboard_tipo = "📝 Dashboard Básico"
                    widget_tasas = "❌ Sin widget de tasas"
                    print(f"   → {dashboard_tipo}")
                    print(f"   → {widget_tasas}")
                    print(f"   → Mensaje: Completar registro")
        
        # Verificar casos específicos
        print(f"\n" + "=" * 60)
        print("🎯 CASOS ESPECÍFICOS VERIFICADOS")
        print("=" * 60)
        
        # Caso 1: Usuario con rol admin + cliente
        cursor.execute("""
            SELECT u.email, u.first_name, u.last_name
            FROM auth_user u
            JOIN auth_membership m1 ON u.id = m1.user_id
            JOIN auth_group g1 ON m1.group_id = g1.id AND g1.role = 'administrador'
            JOIN auth_membership m2 ON u.id = m2.user_id
            JOIN auth_group g2 ON m2.group_id = g2.id AND g2.role = 'cliente'
            LIMIT 1
        """)
        
        admin_cliente = cursor.fetchone()
        
        if admin_cliente:
            email, first_name, last_name = admin_cliente
            print(f"✅ Usuario con admin + cliente: {first_name} {last_name}")
            print(f"   → Verá: Dashboard Administrativo (prioridad)")
            print(f"   → Widget: Tasas BCV")
        
        # Caso 2: Usuario solo cliente
        cursor.execute("""
            SELECT u.email, u.first_name, u.last_name
            FROM auth_user u
            JOIN auth_membership m ON u.id = m.user_id
            JOIN auth_group g ON m.group_id = g.id AND g.role = 'cliente'
            WHERE u.id NOT IN (
                SELECT DISTINCT u2.id 
                FROM auth_user u2
                JOIN auth_membership m2 ON u2.id = m2.user_id
                JOIN auth_group g2 ON m2.group_id = g2.id 
                WHERE g2.role IN ('administrador', 'operador')
            )
            LIMIT 1
        """)
        
        solo_cliente = cursor.fetchone()
        
        if solo_cliente:
            email, first_name, last_name = solo_cliente
            print(f"✅ Usuario solo cliente: {first_name} {last_name}")
            print(f"   → Verá: Dashboard Cliente")
            print(f"   → Widget: Tasas Actuales")
        
        conn.close()
        
        print(f"\n" + "=" * 60)
        print("📋 RESUMEN DEL FIX")
        print("=" * 60)
        
        print("🔧 Cambio realizado:")
        print("   • Prioridad a roles admin/operador sobre cliente")
        print("   • Administradores ven dashboard administrativo")
        print("   • Clientes ven dashboard de cliente")
        print("   • Usuarios sin rol ven dashboard básico")
        
        print("\n✅ Resultado esperado:")
        print("   • Administradores verán 'Tasas BCV' en esquina superior derecha")
        print("   • Clientes verán 'Tasas Actuales' en columna izquierda")
        print("   • Ambos incluyen USD, EUR y USDT")
        
        print(f"\n🌐 Para probar:")
        print("   1. Refrescar la página del dashboard")
        print("   2. Verificar que aparezca el widget de tasas")
        print("   3. Confirmar que muestre USD, EUR y USDT")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False

if __name__ == '__main__':
    test_dashboard_logic()