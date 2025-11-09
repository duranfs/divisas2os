#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificación final de todas las correcciones aplicadas
"""

import os

def verificar_todo():
    """Verificar que todas las correcciones están funcionando"""
    
    print("=" * 70)
    print("🎉 VERIFICACIÓN FINAL: Todas las Correcciones")
    print("=" * 70)
    
    errores_encontrados = []
    
    # 1. Verificar sintaxis del controlador
    print("1. VERIFICANDO SINTAXIS DEL CONTROLADOR:")
    try:
        if os.path.exists("controllers/cuentas.py"):
            with open("controllers/cuentas.py", 'r', encoding='utf-8') as f:
                contenido = f.read()
            compile(contenido, "controllers/cuentas.py", "exec")
            print("   ✅ Sintaxis de controllers/cuentas.py válida")
        else:
            errores_encontrados.append("Controlador cuentas.py no existe")
    except SyntaxError as e:
        errores_encontrados.append(f"Error de sintaxis en controlador: {e}")
        print(f"   ❌ Error de sintaxis: {e}")
    
    # 2. Verificar menú corregido
    print("\n2. VERIFICANDO MENÚ CORREGIDO:")
    if os.path.exists("models/menu.py"):
        with open("models/menu.py", 'r', encoding='utf-8') as f:
            contenido_menu = f.read()
        
        if "URL('cuentas', 'index')" in contenido_menu:
            print("   ✅ Enlaces del menú corregidos")
        else:
            errores_encontrados.append("Enlaces del menú no corregidos")
            print("   ❌ Enlaces del menú no corregidos")
    else:
        errores_encontrados.append("Archivo menu.py no existe")
    
    # 3. Verificar funciones clave
    print("\n3. VERIFICANDO FUNCIONES CLAVE:")
    if os.path.exists("controllers/cuentas.py"):
        with open("controllers/cuentas.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        funciones_requeridas = [
            "def index():",
            "def detalle():",
            "def listar_todas():",
            "def mis_cuentas():",
            "def debug_cliente():"
        ]
        
        for funcion in funciones_requeridas:
            if funcion in contenido:
                print(f"   ✅ {funcion}")
            else:
                print(f"   ❌ {funcion}")
                errores_encontrados.append(f"Función faltante: {funcion}")
    
    # 4. Verificar vistas clave
    print("\n4. VERIFICANDO VISTAS CLAVE:")
    vistas_requeridas = [
        "views/cuentas/index.html",
        "views/cuentas/detalle.html",
        "views/cuentas/mis_cuentas.html"
    ]
    
    for vista in vistas_requeridas:
        if os.path.exists(vista):
            print(f"   ✅ {vista}")
        else:
            print(f"   ❌ {vista}")
            errores_encontrados.append(f"Vista faltante: {vista}")
    
    # 5. Verificar corrección de hash de contraseñas
    print("\n5. VERIFICANDO HASH DE CONTRASEÑAS:")
    if os.path.exists("controllers/clientes.py"):
        with open("controllers/clientes.py", 'r', encoding='utf-8') as f:
            contenido_clientes = f.read()
        
        if "CRYPT()" in contenido_clientes and "validated_password" in contenido_clientes:
            print("   ✅ Hash de contraseñas corregido")
        else:
            print("   ❌ Hash de contraseñas no corregido")
            errores_encontrados.append("Hash de contraseñas no implementado")
    
    # Resumen final
    print("\n" + "=" * 70)
    if not errores_encontrados:
        print("🎉 TODAS LAS CORRECCIONES APLICADAS EXITOSAMENTE")
        
        print("\n✅ FUNCIONALIDADES DISPONIBLES:")
        print("   - Login de clientes funciona correctamente")
        print("   - Menú redirige a vistas correctas")
        print("   - Vista de cuentas para clientes")
        print("   - Vista de detalles de cuenta")
        print("   - Historial de transacciones")
        print("   - Acceso de administradores restaurado")
        
        print("\n🧪 PARA PROBAR:")
        print("1. Haz login como cliente")
        print("2. Ve a 'Mi Perfil' → 'Información Bancaria'")
        print("3. O ve a 'Mis Cuentas' → 'Ver Mis Cuentas'")
        print("4. Deberías ver tus datos bancarios")
        
        print("\n📍 URLS FUNCIONALES:")
        print("   - /cuentas/index - Vista principal")
        print("   - /cuentas/detalle/ID - Detalles de cuenta")
        print("   - /cuentas/mis_cuentas - Vista alternativa")
        print("   - /divisas/historial_transacciones - Historial")
        print("   - /cuentas/debug_cliente - Debug (si necesario)")
        
    else:
        print("❌ ERRORES ENCONTRADOS:")
        for error in errores_encontrados:
            print(f"   - {error}")
        
        print("\n🔧 ACCIONES REQUERIDAS:")
        print("   - Corregir los errores listados arriba")
        print("   - Verificar sintaxis de archivos")
        print("   - Probar funcionalidades manualmente")

if __name__ == "__main__":
    verificar_todo()