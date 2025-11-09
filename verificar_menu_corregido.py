#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificar que el menú fue corregido correctamente
"""

import os

def verificar_menu():
    """Verificar que los enlaces del menú apuntan a las URLs correctas"""
    
    print("=" * 70)
    print("🔧 VERIFICACIÓN: Corrección del Menú")
    print("=" * 70)
    
    print("PROBLEMA IDENTIFICADO:")
    print("❌ El enlace 'Información Bancaria' apuntaba a clientes/perfil")
    print("❌ Los enlaces de 'Mis Cuentas' apuntaban a funciones inexistentes")
    print("❌ Los clientes eran redirigidos a la vista incorrecta")
    
    print("\nCORRECCIONES APLICADAS:")
    
    if os.path.exists("models/menu.py"):
        with open("models/menu.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            # Verificar correcciones
            if "URL('cuentas', 'index')" in contenido:
                print("✅ 'Información Bancaria' ahora apunta a cuentas/index")
            else:
                print("❌ 'Información Bancaria' NO corregido")
            
            if "Ver Mis Cuentas" in contenido:
                print("✅ Menú 'Mis Cuentas' actualizado")
            else:
                print("❌ Menú 'Mis Cuentas' NO actualizado")
            
            if "URL('divisas', 'historial_transacciones')" in contenido:
                print("✅ Enlace a historial de transacciones corregido")
            else:
                print("❌ Enlace a historial NO corregido")
            
            if "URL('divisas', 'comprar')" in contenido:
                print("✅ Enlaces a operaciones de divisas agregados")
            else:
                print("❌ Enlaces a divisas NO agregados")
    
    print("\n" + "=" * 70)
    print("NUEVOS ENLACES DEL MENÚ PARA CLIENTES:")
    
    print("\n📋 MIS CUENTAS:")
    print("   - Ver Mis Cuentas → /cuentas/index")
    print("   - Historial de Transacciones → /divisas/historial_transacciones")
    print("   - Comprar Divisas → /divisas/comprar")
    print("   - Vender Divisas → /divisas/vender")
    
    print("\n👤 MI PERFIL:")
    print("   - Datos Personales → /default/user/profile")
    print("   - Información Bancaria → /cuentas/index")
    print("   - Cambiar Contraseña → /default/user/change_password")
    
    print("\n" + "=" * 70)
    print("🧪 PARA PROBAR:")
    print("1. Haz login como cliente")
    print("2. Ve al menú 'Mi Perfil' → 'Información Bancaria'")
    print("3. Ahora debería llevarte a /cuentas/index")
    print("4. Deberías ver tus datos bancarios")
    print("5. También prueba 'Mis Cuentas' → 'Ver Mis Cuentas'")
    
    print("\n✅ RESULTADO ESPERADO:")
    print("Los clientes ahora deberían poder acceder a sus")
    print("datos bancarios desde cualquier enlace del menú.")

if __name__ == "__main__":
    verificar_menu()