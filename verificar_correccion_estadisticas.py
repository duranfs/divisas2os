#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificar que las correcciones de estadísticas están aplicadas
"""

import os

def verificar_correcciones():
    """Verificar que la vista usa correctamente el diccionario estadisticas_mes"""
    
    print("=" * 70)
    print("VERIFICACIÓN: Corrección de acceso a estadísticas_mes")
    print("=" * 70)
    
    if os.path.exists("views/cuentas/detalle.html"):
        with open("views/cuentas/detalle.html", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            print("VERIFICANDO CORRECCIONES EN LA VISTA:")
            
            # Verificar correcciones aplicadas
            correcciones = [
                ("estadisticas_mes['total_transacciones']", "Total transacciones"),
                ("estadisticas_mes['compras']", "Compras"),
                ("estadisticas_mes['ventas']", "Ventas"),
                ("estadisticas_mes['monto_total_ves']", "Monto total VES")
            ]
            
            todas_correctas = True
            
            for correccion, descripcion in correcciones:
                if correccion in contenido:
                    print(f"✓ {descripcion}: Usa acceso por clave de diccionario")
                else:
                    print(f"❌ {descripcion}: NO corregido")
                    todas_correctas = False
            
            # Verificar que no quedan accesos por atributo
            accesos_incorrectos = [
                "estadisticas_mes.total_transacciones",
                "estadisticas_mes.compras", 
                "estadisticas_mes.ventas",
                "estadisticas_mes.monto_total_ves"
            ]
            
            print("\nVERIFICANDO QUE NO QUEDAN ACCESOS INCORRECTOS:")
            
            for acceso in accesos_incorrectos:
                if acceso in contenido:
                    print(f"❌ ENCONTRADO: {acceso} (debe ser corregido)")
                    todas_correctas = False
                else:
                    print(f"✓ NO encontrado: {acceso}")
            
            print("\n" + "=" * 70)
            
            if todas_correctas:
                print("🎉 TODAS LAS CORRECCIONES APLICADAS CORRECTAMENTE")
                print("\nLa vista ahora debería funcionar sin errores.")
                print("Puedes probar haciendo clic en 'Ver detalles' de una cuenta.")
            else:
                print("❌ ALGUNAS CORRECCIONES FALTAN")
                print("Revisa los elementos marcados con ❌")
                
    else:
        print("❌ No se encontró el archivo views/cuentas/detalle.html")

if __name__ == "__main__":
    verificar_correcciones()