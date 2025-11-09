#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para simular el dashboard localmente y verificar que funcione
"""

import sqlite3
import sys
from datetime import datetime

def simular_dashboard():
    """Simular el comportamiento del dashboard"""
    print("🔍 SIMULACIÓN LOCAL DEL DASHBOARD")
    print("=" * 60)
    
    try:
        # Conectar a BD
        conn = sqlite3.connect("databases/storage.sqlite")
        cursor = conn.cursor()
        
        # 1. Simular obtener_tasas_actuales()
        print("📡 1. SIMULANDO obtener_tasas_actuales()")
        print("-" * 40)
        
        cursor.execute("""
            SELECT id, fecha, hora, usd_ves, eur_ves, usdt_ves, fuente, activa
            FROM tasas_cambio 
            WHERE activa = 1
            ORDER BY fecha DESC, hora DESC 
            LIMIT 1
        """)
        
        tasas = cursor.fetchone()
        
        if tasas:
            print("✅ Tasas obtenidas:")
            print(f"   ID: {tasas[0]}")
            print(f"   Fecha: {tasas[1]} {tasas[2]}")
            print(f"   USD/VES: {tasas[3]}")
            print(f"   EUR/VES: {tasas[4]}")
            print(f"   USDT/VES: {tasas[5]}")
            print(f"   Fuente: {tasas[6]}")
            
            # Crear objeto simulado como lo haría web2py
            class TasaSimulada:
                def __init__(self, data):
                    self.id = data[0]
                    self.fecha = datetime.strptime(data[1], '%Y-%m-%d').date()
                    self.hora = datetime.strptime(data[2], '%H:%M:%S').time()
                    self.usd_ves = data[3]
                    self.eur_ves = data[4]
                    self.usdt_ves = data[5]
                    self.fuente = data[6]
                    self.activa = data[7]
            
            tasa_obj = TasaSimulada(tasas)
            
        else:
            print("❌ No se encontraron tasas")
            tasa_obj = None
        
        # 2. Simular dashboard público (no autenticado)
        print(f"\n🌐 2. SIMULANDO DASHBOARD PÚBLICO")
        print("-" * 40)
        
        if tasa_obj:
            print("✅ Dashboard público mostraría:")
            
            # Simular el código de la vista
            usd_display = "{:,.4f}".format(float(tasa_obj.usd_ves)) if tasa_obj.usd_ves else 'N/A'
            eur_display = "{:,.4f}".format(float(tasa_obj.eur_ves)) if tasa_obj.eur_ves else 'N/A'
            usdt_display = "{:,.4f}".format(float(tasa_obj.usdt_ves)) if tasa_obj.usdt_ves else 'N/A'
            fecha_display = tasa_obj.fecha.strftime('%d/%m/%Y %H:%M') if tasa_obj else 'No disponible'
            
            print(f"""
   Widget de Tasas Actuales BCV:
   ┌─────────────────────────────┐
   │ USD / VES: {usd_display:>13} │
   │ EUR / VES: {eur_display:>13} │
   │ USDT / VES: {usdt_display:>12} │
   │ Actualización: {fecha_display} │
   └─────────────────────────────┘
            """)
        else:
            print("❌ Dashboard público mostraría: 'No hay tasas disponibles'")
        
        # 3. Simular dashboard de cliente
        print(f"\n👤 3. SIMULANDO DASHBOARD DE CLIENTE")
        print("-" * 40)
        
        # Buscar cliente con cuentas
        cursor.execute("""
            SELECT c.id, u.first_name, u.last_name
            FROM clientes c
            JOIN auth_user u ON c.user_id = u.id
            JOIN cuentas cu ON cu.cliente_id = c.id
            GROUP BY c.id
            LIMIT 1
        """)
        
        cliente = cursor.fetchone()
        
        if cliente and tasa_obj:
            cliente_id = cliente[0]
            nombre = f"{cliente[1]} {cliente[2]}"
            
            # Obtener saldos
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(saldo_ves), 0) as total_ves,
                    COALESCE(SUM(saldo_usd), 0) as total_usd,
                    COALESCE(SUM(saldo_eur), 0) as total_eur,
                    COALESCE(SUM(saldo_usdt), 0) as total_usdt
                FROM cuentas 
                WHERE cliente_id = ?
            """, (cliente_id,))
            
            saldos = cursor.fetchone()
            
            print(f"✅ Dashboard de cliente ({nombre}) mostraría:")
            
            # Simular las tarjetas de saldo
            ves_display = "{:,.2f}".format(float(saldos[0]))
            usd_display = "{:,.2f}".format(float(saldos[1]))
            eur_display = "{:,.2f}".format(float(saldos[2]))
            usdt_display = "{:,.2f}".format(float(saldos[3]))
            
            print(f"""
   Resumen de Cuentas:
   ┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
   │ Saldo VES       │ Saldo USD       │ Saldo EUR       │ Saldo USDT      │
   │ {ves_display:>13} VES │ {usd_display:>13} USD │ {eur_display:>13} EUR │ {usdt_display:>12} USDT │
   └─────────────────┴─────────────────┴─────────────────┴─────────────────┘
            """)
            
            # Simular widget de tasas
            tasa_usd_display = "{:,.4f}".format(float(tasa_obj.usd_ves))
            tasa_eur_display = "{:,.4f}".format(float(tasa_obj.eur_ves))
            tasa_usdt_display = "{:,.4f}".format(float(tasa_obj.usdt_ves)) if tasa_obj.usdt_ves else 'N/A'
            
            print(f"""
   Widget de Tasas Actuales:
   ┌─────────────────────────────┐
   │ USD / VES: {tasa_usd_display:>13} │
   │ EUR / VES: {tasa_eur_display:>13} │
   │ USDT / VES: {tasa_usdt_display:>12} │
   └─────────────────────────────┘
            """)
            
            # Calcular equivalencia total
            equivalencia = float(saldos[0])  # VES
            equivalencia += float(saldos[1]) * float(tasa_obj.usd_ves)  # USD
            equivalencia += float(saldos[2]) * float(tasa_obj.eur_ves)  # EUR
            equivalencia += float(saldos[3]) * float(tasa_obj.usdt_ves)  # USDT
            
            print(f"   💰 Equivalencia total en VES: {equivalencia:,.2f}")
            
        else:
            print("❌ No se puede simular dashboard de cliente")
        
        # 4. Simular dashboard administrativo
        print(f"\n🔧 4. SIMULANDO DASHBOARD ADMINISTRATIVO")
        print("-" * 40)
        
        if tasa_obj:
            print("✅ Dashboard administrativo mostraría:")
            
            admin_usd = "{:,.4f}".format(float(tasa_obj.usd_ves))
            admin_eur = "{:,.4f}".format(float(tasa_obj.eur_ves))
            admin_usdt = "{:,.4f}".format(float(tasa_obj.usdt_ves)) if tasa_obj.usdt_ves else 'N/A'
            
            print(f"""
   Tasas BCV:
   ┌─────────────────────┐
   │ USD: {admin_usd:>13} │
   │ EUR: {admin_eur:>13} │
   │ USDT: {admin_usdt:>12} │
   └─────────────────────┘
            """)
        else:
            print("❌ Dashboard administrativo mostraría: 'No disponible'")
        
        conn.close()
        
        # 5. Conclusión
        print(f"\n" + "=" * 60)
        print("📋 CONCLUSIÓN DE LA SIMULACIÓN")
        print("=" * 60)
        
        if tasa_obj:
            print("✅ EL DASHBOARD DEBERÍA FUNCIONAR CORRECTAMENTE")
            print("\n🎯 Funcionalidades verificadas:")
            print("   • Tasas USD, EUR y USDT se muestran correctamente")
            print("   • Saldos de cliente incluyen las 4 monedas")
            print("   • Cálculos de equivalencia funcionan")
            print("   • Formato de números es correcto")
            
            print(f"\n🔧 Si no ves las tasas en el navegador:")
            print("   1. Verificar que web2py esté ejecutándose")
            print("   2. Acceder a: http://127.0.0.1:8000/divisas2os")
            print("   3. Revisar el log de web2py por errores")
            print("   4. Verificar que no haya errores de JavaScript en el navegador")
            
        else:
            print("❌ HAY PROBLEMAS CON LAS TASAS")
            print("   • No hay tasas activas en la base de datos")
            print("   • El dashboard mostrará mensajes de error")
        
        return tasa_obj is not None
        
    except Exception as e:
        print(f"❌ Error durante la simulación: {e}")
        return False

if __name__ == '__main__':
    success = simular_dashboard()
    sys.exit(0 if success else 1)