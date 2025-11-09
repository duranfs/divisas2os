#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para limpiar cache y verificar que las tasas aparezcan en el dashboard
"""

import sqlite3
import os
import glob

def limpiar_cache_tasas():
    """Limpiar cache de tasas y verificar funcionamiento"""
    print("🧹 LIMPIANDO CACHE Y VERIFICANDO TASAS")
    print("=" * 60)
    
    try:
        # 1. Limpiar archivos de cache
        print("🗑️ 1. LIMPIANDO ARCHIVOS DE CACHE")
        print("-" * 40)
        
        cache_patterns = [
            "cache/*.cache",
            "sessions/*.sess",
            "errors/*.log"
        ]
        
        files_deleted = 0
        for pattern in cache_patterns:
            files = glob.glob(pattern)
            for file in files:
                try:
                    os.remove(file)
                    files_deleted += 1
                except:
                    pass
        
        print(f"   🗑️ Eliminados {files_deleted} archivos de cache")
        
        # 2. Verificar estado actual de tasas
        print(f"\n📊 2. VERIFICANDO ESTADO ACTUAL")
        print("-" * 40)
        
        conn = sqlite3.connect("databases/storage.sqlite")
        cursor = conn.cursor()
        
        # Verificar tasa activa
        cursor.execute("""
            SELECT id, fecha, hora, usd_ves, eur_ves, usdt_ves, fuente
            FROM tasas_cambio 
            WHERE activa = 1
            LIMIT 1
        """)
        
        tasa_activa = cursor.fetchone()
        
        if tasa_activa:
            print("   ✅ Tasa activa encontrada:")
            print(f"      ID: {tasa_activa[0]}")
            print(f"      Fecha: {tasa_activa[1]} {tasa_activa[2]}")
            print(f"      USD/VES: {tasa_activa[3]}")
            print(f"      EUR/VES: {tasa_activa[4]}")
            print(f"      USDT/VES: {tasa_activa[5]}")
            print(f"      Fuente: {tasa_activa[6]}")
        else:
            print("   ❌ No hay tasa activa")
            return False
        
        # 3. Simular respuesta del dashboard
        print(f"\n🎯 3. SIMULANDO RESPUESTA DEL DASHBOARD")
        print("-" * 40)
        
        # Simular dashboard_administrativo()
        print("   📋 dashboard_administrativo() retornaría:")
        print("   {")
        print("       'tipo_dashboard': 'administrativo',")
        print("       'tasas_actuales': <objeto_tasa>,")
        print("       'transacciones_hoy': <numero>,")
        print("       'clientes_activos': <numero>,")
        print("       'cuentas_activas': <numero>,")
        print("       'accesos_rapidos': <lista>")
        print("   }")
        
        # 4. Simular vista HTML
        print(f"\n🎨 4. SIMULANDO VISTA HTML")
        print("-" * 40)
        
        print("   📄 En views/default/index.html:")
        print("   {{elif tipo_dashboard == 'administrativo':}}")
        print("   ...")
        print("   <div class=\"widget-tasas\">")
        print("     <h6>Tasas BCV</h6>")
        print("     {{if tasas_actuales:}}  ← Debería ser True")
        print(f"       USD: {tasa_activa[3]:.4f}")
        print(f"       EUR: {tasa_activa[4]:.4f}")
        print(f"       USDT: {tasa_activa[5]:.4f}")
        print("     {{else:}}")
        print("       No disponible  ← NO debería ejecutarse")
        print("     {{pass}}")
        print("   </div>")
        
        # 5. Verificar que no haya problemas de formato
        print(f"\n🔍 5. VERIFICANDO FORMATO")
        print("-" * 40)
        
        try:
            usd_formatted = "{:,.4f}".format(float(tasa_activa[3]))
            eur_formatted = "{:,.4f}".format(float(tasa_activa[4]))
            usdt_formatted = "{:,.4f}".format(float(tasa_activa[5])) if tasa_activa[5] else 'N/A'
            
            print("   ✅ Formato correcto:")
            print(f"      USD: {usd_formatted}")
            print(f"      EUR: {eur_formatted}")
            print(f"      USDT: {usdt_formatted}")
            
        except Exception as e:
            print(f"   ❌ Error de formato: {e}")
            return False
        
        conn.close()
        
        # 6. Instrucciones finales
        print(f"\n" + "=" * 60)
        print("📋 INSTRUCCIONES FINALES")
        print("=" * 60)
        
        print("🔄 PASOS PARA VER LAS TASAS:")
        print("   1. Refrescar la página del dashboard (F5)")
        print("   2. Si no aparecen, hacer Ctrl+F5 (refresh completo)")
        print("   3. Si aún no aparecen, reiniciar web2py")
        
        print(f"\n🎯 DEBERÍAS VER:")
        print("   • Widget 'Tasas BCV' en la esquina superior derecha")
        print("   • Tres líneas con USD, EUR y USDT")
        print("   • Valores numéricos (no 'No disponible')")
        
        print(f"\n🔧 SI AÚN NO APARECEN:")
        print("   1. Verificar consola del navegador (F12)")
        print("   2. Buscar errores JavaScript")
        print("   3. Verificar que estés logueado como administrador")
        print("   4. Confirmar que ves 'Panel Administrativo' en el título")
        
        print(f"\n📞 PARA DEBUGGING ADICIONAL:")
        print("   • Agregar {{=tasas_actuales}} en la vista para ver el objeto")
        print("   • Verificar logs de web2py por errores")
        print("   • Usar herramientas de desarrollador del navegador")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la limpieza: {e}")
        return False

if __name__ == '__main__':
    limpiar_cache_tasas()