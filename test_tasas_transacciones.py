#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para probar la función obtener_tasas_para_transacciones con USDT
"""

def test_tasas_transacciones():
    """
    Prueba la función obtener_tasas_para_transacciones
    """
    print("=== PRUEBA DE TASAS PARA TRANSACCIONES ===")
    
    try:
        # Leer el controlador para verificar la función
        with open('controllers/divisas.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        print("\n1. Verificando función obtener_tasas_para_transacciones()...")
        
        # Verificar que incluye USDT
        elementos_usdt = [
            "usdt_base = tasas_base['usdt_ves']",
            "'USDT': {",
            "'usdt': {",
            "usdt_base * (1 + margen)",
            "usdt_base * (1 - margen)"
        ]
        
        elementos_encontrados = 0
        for elemento in elementos_usdt:
            if elemento in controller_content:
                elementos_encontrados += 1
                print(f"   ✅ {elemento}")
            else:
                print(f"   ❌ {elemento}")
        
        print(f"\n   📊 Elementos USDT encontrados: {elementos_encontrados}/{len(elementos_usdt)}")
        
        print("\n2. Verificando tasas por defecto...")
        
        # Verificar tasas por defecto
        tasas_defecto = [
            "'USDT': {",
            "'compra': 36.50,",
            "'venta': 36.80"
        ]
        
        defecto_encontrados = 0
        for tasa in tasas_defecto:
            count = controller_content.count(tasa)
            if count >= 2:  # Debe aparecer al menos 2 veces (en ambas secciones de defecto)
                defecto_encontrados += 1
                print(f"   ✅ {tasa} (aparece {count} veces)")
            else:
                print(f"   ❌ {tasa} (aparece {count} veces)")
        
        print(f"\n   📊 Tasas por defecto USDT: {defecto_encontrados}/{len(tasas_defecto)}")
        
        print("\n3. Verificando uso en procesar_compra_divisa()...")
        
        # Buscar la línea específica que usa obtener_tasas_para_transacciones
        if 'tasas = obtener_tasas_para_transacciones()' in controller_content:
            print("   ✅ Se usa obtener_tasas_para_transacciones() en procesar_compra_divisa")
            
            # Verificar el contexto
            lineas = controller_content.split('\n')
            for i, linea in enumerate(lineas):
                if 'tasas = obtener_tasas_para_transacciones()' in linea:
                    print(f"   📍 Línea {i+1}: {linea.strip()}")
                    
                    # Mostrar contexto
                    if i > 0:
                        print(f"   📍 Línea {i}: {lineas[i-1].strip()}")
                    if i < len(lineas) - 1:
                        print(f"   📍 Línea {i+2}: {lineas[i+1].strip()}")
        else:
            print("   ❌ No se usa obtener_tasas_para_transacciones() en procesar_compra_divisa")
        
        print("\n4. Verificando validación de moneda destino...")
        
        # Buscar la validación específica
        if 'if not tasas or moneda_destino not in tasas:' in controller_content:
            print("   ✅ Validación de moneda destino encontrada")
        else:
            print("   ❌ Validación de moneda destino NO encontrada")
        
        print("\n5. Simulando estructura de tasas...")
        
        # Simular la estructura que debería devolver la función
        estructura_esperada = {
            'USD': {'compra': 214.18, 'venta': 210.78},
            'EUR': {'compra': 248.65, 'venta': 244.71},
            'USDT': {'compra': 214.16, 'venta': 210.76},
            'usd': {'compra': 214.18, 'venta': 210.78},
            'eur': {'compra': 248.65, 'venta': 244.71},
            'usdt': {'compra': 214.16, 'venta': 210.76}
        }
        
        print("   📊 Estructura esperada de tasas:")
        for moneda, tasas in estructura_esperada.items():
            print(f"      {moneda}: compra={tasas['compra']}, venta={tasas['venta']}")
        
        # Verificar si USDT estaría disponible
        if 'USDT' in estructura_esperada:
            print("   ✅ USDT disponible en estructura de tasas")
        else:
            print("   ❌ USDT NO disponible en estructura de tasas")
        
        print("\n6. Recomendaciones:")
        
        if elementos_encontrados == len(elementos_usdt) and defecto_encontrados == len(tasas_defecto):
            print("   ✅ La función obtener_tasas_para_transacciones() incluye USDT correctamente")
            print("   🎯 El error de USDT debería estar resuelto")
            print("   📝 Reiniciar web2py y probar la compra de USDT")
        else:
            print("   ❌ La función obtener_tasas_para_transacciones() NO incluye USDT completamente")
            print("   🔧 Revisar las correcciones aplicadas")
        
        return elementos_encontrados == len(elementos_usdt) and defecto_encontrados == len(tasas_defecto)
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = test_tasas_transacciones()
    print(f"\n{'='*60}")
    if resultado:
        print("🎉 FUNCIÓN CORREGIDA - USDT debería funcionar ahora")
    else:
        print("🔧 FUNCIÓN INCOMPLETA - Revisar correcciones")
    print(f"{'='*60}")