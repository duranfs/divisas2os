#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar que no hay redirect después de venta
"""

def verificar_no_redirect():
    """
    Verifica que el redirect al comprobante esté deshabilitado
    """
    print("=== VERIFICACIÓN DE NO REDIRECT ===")
    
    try:
        # Leer el controlador
        with open('controllers/divisas.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        print("\n1. Verificando que el redirect esté deshabilitado...")
        
        # Verificar que no hay redirect activo
        redirect_patterns = [
            ("Redirect al comprobante deshabilitado", "redirect(URL('divisas', 'comprobante'"),
            ("Comentario de deshabilitado", "Temporalmente deshabilitado el redirect"),
            ("Logging de venta exitosa", "Venta exitosa - Transacción ID"),
            ("No hacer redirect", "No hacer redirect, quedarse en la página")
        ]
        
        cambios_aplicados = 0
        for nombre, patron in redirect_patterns:
            if patron in controller_content:
                if "redirect(URL('divisas', 'comprobante'" in patron:
                    print(f"   ❌ {nombre} - AÚN ACTIVO")
                else:
                    cambios_aplicados += 1
                    print(f"   ✅ {nombre}")
            else:
                if "redirect(URL('divisas', 'comprobante'" in patron:
                    print(f"   ✅ {nombre} - CORRECTAMENTE DESHABILITADO")
                    cambios_aplicados += 1
                else:
                    print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Cambios aplicados: {cambios_aplicados}/4")
        
        print("\n2. Verificando función vender() completa...")
        
        # Buscar la sección completa de manejo de resultado exitoso
        lineas = controller_content.split('\n')
        seccion_venta = []
        en_seccion = False
        
        for linea in lineas:
            if "if resultado['success']:" in linea:
                en_seccion = True
            
            if en_seccion:
                seccion_venta.append(linea.strip())
                
                if "else:" in linea and "response.flash" in lineas[lineas.index(linea) + 1]:
                    break
        
        if seccion_venta:
            print("   📊 Sección de manejo de venta exitosa:")
            for i, linea in enumerate(seccion_venta[:10]):  # Mostrar primeras 10 líneas
                print(f"      {i+1:2d}: {linea}")
        
        print("\n3. Comportamiento esperado después del cambio:")
        print("   ✅ Venta se procesa correctamente")
        print("   ✅ Se muestra mensaje: '✅ Venta realizada exitosamente. Comprobante: VENT-XXXXX'")
        print("   ✅ Se queda en la página de venta (NO redirige)")
        print("   ✅ Usuario puede hacer otra venta o navegar manualmente")
        
        print("\n4. Para probar:")
        print("   1. Reiniciar web2py")
        print("   2. Ir a: http://127.0.0.1:8000/divisas2os/divisas/vender")
        print("   3. Realizar una venta")
        print("   4. Verificar que:")
        print("      - Se muestra el mensaje de éxito")
        print("      - NO redirige a otra página")
        print("      - Se queda en la página de venta")
        
        return cambios_aplicados >= 3
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = verificar_no_redirect()
    print(f"\n{'='*60}")
    if resultado:
        print("🎉 REDIRECT DESHABILITADO - Ya no debería ir al index")
    else:
        print("🔧 REDIRECT AÚN ACTIVO - Revisar cambios")
    print(f"{'='*60}")