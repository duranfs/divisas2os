#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para debuggear completamente el problema del dashboard
"""

import sqlite3
import sys

def debug_dashboard_completo():
    """Debug completo del dashboard"""
    print("🔍 DEBUG COMPLETO DEL DASHBOARD")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect("databases/storage.sqlite")
        cursor = conn.cursor()
        
        # 1. Verificar usuarios y roles
        print("👥 1. VERIFICANDO USUARIOS Y ROLES")
        print("-" * 40)
        
        cursor.execute("""
            SELECT 
                u.id,
                u.email,
                u.first_name,
                u.last_name,
                GROUP_CONCAT(g.role) as roles,
                CASE WHEN c.id IS NOT NULL THEN 'Sí' ELSE 'No' END as es_cliente
            FROM auth_user u
            LEFT JOIN auth_membership m ON u.id = m.user_id
            LEFT JOIN auth_group g ON m.group_id = g.id
            LEFT JOIN clientes c ON u.id = c.user_id
            WHERE u.estado = 'activo'
            GROUP BY u.id, u.email, u.first_name, u.last_name, c.id
            ORDER BY u.id
        """)
        
        usuarios = cursor.fetchall()
        
        for usuario in usuarios:
            user_id, email, first_name, last_name, roles_str, es_cliente = usuario
            roles = roles_str.split(',') if roles_str else []
            
            print(f"\n   👤 {first_name} {last_name} ({email})")
            print(f"      Roles: {roles}")
            print(f"      Es cliente: {es_cliente}")
            
            # Determinar dashboard según nueva lógica
            es_admin = 'administrador' in roles
            es_operador = 'operador' in roles
            
            if es_cliente == 'Sí':
                dashboard_esperado = "👤 Dashboard Cliente"
                tasas_widget = "✅ Widget 'Tasas Actuales' (columna izquierda)"
            elif es_admin or es_operador:
                dashboard_esperado = "🔧 Dashboard Administrativo"
                tasas_widget = "✅ Widget 'Tasas BCV' (esquina superior derecha)"
            else:
                dashboard_esperado = "📝 Dashboard Básico"
                tasas_widget = "❌ Sin widget de tasas"
            
            print(f"      Dashboard: {dashboard_esperado}")
            print(f"      Tasas: {tasas_widget}")
        
        # 2. Verificar función obtener_tasas_actuales()
        print(f"\n📡 2. VERIFICANDO obtener_tasas_actuales()")
        print("-" * 40)
        
        # Simular la consulta exacta de la función
        cursor.execute("""
            SELECT id, fecha, hora, usd_ves, eur_ves, usdt_ves, fuente, activa
            FROM tasas_cambio 
            WHERE activa = 1
            ORDER BY fecha DESC, hora DESC 
            LIMIT 1
        """)
        
        tasa_resultado = cursor.fetchone()
        
        if tasa_resultado:
            print("   ✅ obtener_tasas_actuales() retornaría objeto con:")
            print(f"      .id = {tasa_resultado[0]}")
            print(f"      .fecha = {tasa_resultado[1]}")
            print(f"      .hora = {tasa_resultado[2]}")
            print(f"      .usd_ves = {tasa_resultado[3]}")
            print(f"      .eur_ves = {tasa_resultado[4]}")
            print(f"      .usdt_ves = {tasa_resultado[5]}")
            print(f"      .fuente = {tasa_resultado[6]}")
            print(f"      .activa = {tasa_resultado[7]}")
        else:
            print("   ❌ obtener_tasas_actuales() retornaría None")
            print("   🔧 Esto causaría que {{if tasas_actuales:}} sea False")
        
        # 3. Simular dashboard_cliente()
        print(f"\n👤 3. SIMULANDO dashboard_cliente()")
        print("-" * 40)
        
        if tasa_resultado:
            print("   ✅ dashboard_cliente() pasaría a la vista:")
            print("   {")
            print("       'tipo_dashboard': 'cliente',")
            print("       'cliente': <objeto_cliente>,")
            print("       'cuentas': <lista_cuentas>,")
            print("       'total_ves': <numero>,")
            print("       'total_usd': <numero>,")
            print("       'total_eur': <numero>,")
            print("       'total_usdt': <numero>,")
            print(f"       'tasas_actuales': <objeto_con_usdt={tasa_resultado[5]}>,")
            print("       'ultimas_transacciones': <lista>,")
            print("       'accesos_rapidos': <lista>")
            print("   }")
        
        # 4. Simular dashboard_administrativo()
        print(f"\n🔧 4. SIMULANDO dashboard_administrativo()")
        print("-" * 40)
        
        if tasa_resultado:
            print("   ✅ dashboard_administrativo() pasaría a la vista:")
            print("   {")
            print("       'tipo_dashboard': 'administrativo',")
            print("       'transacciones_hoy': <numero>,")
            print("       'clientes_activos': <numero>,")
            print("       'cuentas_activas': <numero>,")
            print(f"       'tasas_actuales': <objeto_con_usdt={tasa_resultado[5]}>,")
            print("       'ultimas_transacciones': <lista>,")
            print("       'accesos_rapidos': <lista>")
            print("   }")
        
        # 5. Verificar vista HTML
        print(f"\n🎨 5. VERIFICANDO VISTA HTML")
        print("-" * 40)
        
        print("   📄 Para dashboard cliente:")
        print("   {{if tipo_dashboard == 'cliente':}}")
        print("     {{if tasas_actuales:}}  ← Debería ser True")
        print("       <div class=\"widget-tasas\">")
        print("         <h5>Tasas Actuales</h5>")
        print(f"         USD: {tasa_resultado[3] if tasa_resultado else 'N/A'}")
        print(f"         EUR: {tasa_resultado[4] if tasa_resultado else 'N/A'}")
        print(f"         USDT: {tasa_resultado[5] if tasa_resultado else 'N/A'}")
        print("       </div>")
        
        print(f"\n   📄 Para dashboard administrativo:")
        print("   {{elif tipo_dashboard == 'administrativo':}}")
        print("     {{if tasas_actuales:}}  ← Debería ser True")
        print("       <div class=\"widget-tasas\">")
        print("         <h6>Tasas BCV</h6>")
        print(f"         USD: {tasa_resultado[3] if tasa_resultado else 'N/A'}")
        print(f"         EUR: {tasa_resultado[4] if tasa_resultado else 'N/A'}")
        print(f"         USDT: {tasa_resultado[5] if tasa_resultado else 'N/A'}")
        print("       </div>")
        
        # 6. Crear URL de prueba
        print(f"\n🌐 6. URLs DE PRUEBA")
        print("-" * 40)
        
        print("   📋 Para probar dashboards específicos:")
        print("   • Dashboard automático: /divisas2os/default/index")
        print("   • Dashboard cliente: /divisas2os/default/dashboard")
        print("   • Dashboard admin: /divisas2os/default/admin")
        print("   • Dashboard con parámetro: /divisas2os/default/dashboard?type=admin")
        
        conn.close()
        
        # 7. Diagnóstico final
        print(f"\n" + "=" * 60)
        print("📋 DIAGNÓSTICO FINAL")
        print("=" * 60)
        
        if tasa_resultado:
            print("✅ DATOS CORRECTOS:")
            print("   • Hay tasas activas en la base de datos")
            print("   • obtener_tasas_actuales() debería funcionar")
            print("   • Los dashboards deberían mostrar las tasas")
            
            print(f"\n🔧 SI NO VES LAS TASAS:")
            print("   1. Verificar que estés en el dashboard correcto")
            print("   2. Buscar errores en la consola del navegador (F12)")
            print("   3. Agregar debug temporal en la vista:")
            print("      {{=tasas_actuales}} para ver el objeto")
            print("   4. Verificar logs de web2py por errores")
            
        else:
            print("❌ PROBLEMA IDENTIFICADO:")
            print("   • No hay tasas activas")
            print("   • obtener_tasas_actuales() retorna None")
            print("   • Los widgets mostrarán 'No disponible'")
        
        return tasa_resultado is not None
        
    except Exception as e:
        print(f"❌ Error durante el debug: {e}")
        return False

if __name__ == '__main__':
    debug_dashboard_completo()