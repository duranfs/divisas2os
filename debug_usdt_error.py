#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de debug para rastrear el error de USDT
"""

import sqlite3

def debug_usdt_error():
    """
    Debug específico para el error de USDT
    """
    print("=== DEBUG DEL ERROR USDT ===")
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        print("\n1. Verificando tasas en la base de datos...")
        
        cursor.execute("""
            SELECT id, fecha, hora, usd_ves, eur_ves, usdt_ves, fuente, activa
            FROM tasas_cambio 
            WHERE activa = 1
            ORDER BY fecha DESC, hora DESC
            LIMIT 3
        """)
        
        tasas_activas = cursor.fetchall()
        
        if tasas_activas:
            print(f"   📊 Tasas activas encontradas: {len(tasas_activas)}")
            for tasa in tasas_activas:
                print(f"   ID: {tasa[0]} | Fecha: {tasa[1]} | Hora: {tasa[2]}")
                print(f"      USD/VES: {tasa[3]} | EUR/VES: {tasa[4]} | USDT/VES: {tasa[5]}")
                print(f"      Fuente: {tasa[6]} | Activa: {tasa[7]}")
                print(f"      USDT es None: {tasa[5] is None}")
                print(f"      USDT es 0: {tasa[5] == 0}")
                print("   " + "-" * 60)
        else:
            print("   ❌ No hay tasas activas")
        
        print("\n2. Simulando obtener_tasas_actuales()...")
        
        # Simular la función obtener_tasas_actuales
        cursor.execute("SELECT * FROM tasas_cambio WHERE activa = 1 LIMIT 1")
        tasa_activa = cursor.fetchone()
        
        if tasa_activa:
            print("   ✅ Tasa activa encontrada")
            print(f"   Campos: {[desc[0] for desc in cursor.description]}")
            print(f"   Valores: {tasa_activa}")
            
            # Simular la lógica de la función
            try:
                usd_ves = float(tasa_activa[3])  # Asumiendo que usd_ves está en posición 3
                eur_ves = float(tasa_activa[4])  # Asumiendo que eur_ves está en posición 4
                usdt_ves_raw = tasa_activa[5]    # Asumiendo que usdt_ves está en posición 5
                
                print(f"   USD/VES raw: {tasa_activa[3]} -> float: {usd_ves}")
                print(f"   EUR/VES raw: {tasa_activa[4]} -> float: {eur_ves}")
                print(f"   USDT/VES raw: {usdt_ves_raw}")
                
                if usdt_ves_raw:
                    usdt_ves = float(usdt_ves_raw)
                    print(f"   USDT/VES convertido: {usdt_ves}")
                else:
                    usdt_ves = usd_ves  # Fallback a USD
                    print(f"   USDT/VES fallback a USD: {usdt_ves}")
                
                tasas_simuladas = {
                    'usd_ves': usd_ves,
                    'eur_ves': eur_ves,
                    'usdt_ves': usdt_ves,
                    'fecha': tasa_activa[1],
                    'hora': tasa_activa[2],
                    'fuente': tasa_activa[6]
                }
                
                print(f"   📊 Diccionario de tasas simulado:")
                for key, value in tasas_simuladas.items():
                    print(f"      {key}: {value}")
                
                # Verificar acceso a USDT
                if 'usdt_ves' in tasas_simuladas:
                    print(f"   ✅ Clave 'usdt_ves' existe: {tasas_simuladas['usdt_ves']}")
                else:
                    print("   ❌ Clave 'usdt_ves' NO existe")
                
            except Exception as e:
                print(f"   ❌ Error simulando obtener_tasas_actuales: {str(e)}")
        
        print("\n3. Verificando función obtener_tasas_para_transacciones()...")
        
        # Leer el controlador para ver si existe esta función
        with open('controllers/divisas.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        if 'def obtener_tasas_para_transacciones():' in controller_content:
            print("   ✅ Función obtener_tasas_para_transacciones() existe")
            
            # Buscar si se usa en procesar_compra_divisa
            if 'obtener_tasas_para_transacciones()' in controller_content:
                print("   ⚠️  Se usa obtener_tasas_para_transacciones() en lugar de obtener_tasas_actuales()")
                print("   🔧 Esto podría ser la causa del problema")
            else:
                print("   ✅ No se usa obtener_tasas_para_transacciones() incorrectamente")
        else:
            print("   ✅ Función obtener_tasas_para_transacciones() no existe")
        
        print("\n4. Verificando llamadas a obtener tasas en procesar_compra_divisa...")
        
        # Buscar las líneas específicas
        lineas_tasas = [
            'tasas = obtener_tasas_actuales()',
            'tasas = obtener_tasas_para_transacciones()',
            'if not tasas:',
            "return {'success': False, 'error': 'No se pudieron obtener las tasas de cambio'}"
        ]
        
        for linea in lineas_tasas:
            if linea in controller_content:
                print(f"   ✅ Encontrado: {linea}")
            else:
                print(f"   ❌ No encontrado: {linea}")
        
        print("\n5. Verificando validación de moneda USDT...")
        
        validaciones_usdt = [
            "if moneda_destino not in ['USD', 'EUR', 'USDT']:",
            "elif moneda_destino == 'USDT':",
            "tasa_aplicada = tasas['usdt_ves']"
        ]
        
        for validacion in validaciones_usdt:
            if validacion in controller_content:
                print(f"   ✅ Encontrado: {validacion}")
            else:
                print(f"   ❌ No encontrado: {validacion}")
        
        conn.close()
        
        print("\n6. Posibles causas del error:")
        print("   1. La función obtener_tasas_para_transacciones() no incluye USDT")
        print("   2. El campo usdt_ves es NULL en la base de datos")
        print("   3. Error en la conversión de tipos de datos")
        print("   4. La validación de moneda falla antes de llegar a las tasas")
        
        print("\n7. Soluciones recomendadas:")
        print("   1. Verificar que se use obtener_tasas_actuales() y no obtener_tasas_para_transacciones()")
        print("   2. Actualizar la tasa USDT en la base de datos si es NULL")
        print("   3. Agregar logging detallado en procesar_compra_divisa()")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el debug: {str(e)}")
        return False

if __name__ == "__main__":
    debug_usdt_error()
    print(f"\n{'='*60}")
    print("🔍 DEBUG COMPLETADO - Revisar posibles causas arriba")
    print(f"{'='*60}")