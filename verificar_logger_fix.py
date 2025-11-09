#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar que el logger esté correctamente configurado
"""

def verificar_logger_fix():
    """
    Verifica que el logger esté correctamente importado y configurado
    """
    print("=== VERIFICACIÓN DEL LOGGER FIX ===")
    
    try:
        # Leer el controlador
        with open('controllers/clientes.py', 'r', encoding='utf-8') as f:
            controller_content = f.read()
        
        print("\n1. Verificando importaciones...")
        
        # Verificar importaciones necesarias
        importaciones = [
            ('Import logging', 'import logging'),
            ('Configuración logger', 'logger = logging.getLogger'),
            ('Logger web2py.app.clientes', '"web2py.app.clientes"')
        ]
        
        imports_ok = 0
        for nombre, import_text in importaciones:
            if import_text in controller_content:
                imports_ok += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Importaciones: {imports_ok}/{len(importaciones)}")
        
        print("\n2. Verificando uso del logger...")
        
        # Verificar que el logger se use correctamente
        usos_logger = [
            ('Logger info en cambiar_estado', 'logger.info(f"Estado de cliente cambiado'),
            ('Logger error en cambiar_estado', 'logger.error(f"Error cambiando estado'),
            ('Logger warning en auditoría', 'logger.warning(f"No se pudo registrar')
        ]
        
        usos_ok = 0
        for nombre, uso in usos_logger:
            if uso in controller_content:
                usos_ok += 1
                print(f"   ✅ {nombre}")
            else:
                print(f"   ❌ {nombre}")
        
        print(f"\n   📊 Usos del logger: {usos_ok}/{len(usos_logger)}")
        
        print("\n3. Verificando sintaxis del archivo...")
        
        # Intentar compilar el archivo
        try:
            import py_compile
            py_compile.compile('controllers/clientes.py', doraise=True)
            print("   ✅ Archivo compila sin errores de sintaxis")
            sintaxis_ok = True
        except py_compile.PyCompileError as e:
            print(f"   ❌ Error de sintaxis: {str(e)}")
            sintaxis_ok = False
        
        print("\n4. Verificando función cambiar_estado completa...")
        
        # Buscar la función cambiar_estado
        lineas = controller_content.split('\n')
        en_funcion = False
        lineas_funcion = []
        
        for linea in lineas:
            if 'def cambiar_estado():' in linea:
                en_funcion = True
            
            if en_funcion:
                lineas_funcion.append(linea.strip())
                
                if linea.strip().startswith('redirect(URL(') and 'listar' in linea:
                    break
        
        if lineas_funcion:
            print(f"   ✅ Función cambiar_estado encontrada ({len(lineas_funcion)} líneas)")
            
            # Verificar elementos clave
            elementos_clave = [
                'auth.requires_login()',
                'auth.has_membership',
                'request.args(0)',
                'db(db.clientes.id == cliente_id)',
                'db(db.auth_user.id == cliente.user_id).update',
                'logger.info',
                'logger.error',
                'session.flash',
                'redirect(URL'
            ]
            
            elementos_encontrados = 0
            for elemento in elementos_clave:
                if any(elemento in linea for linea in lineas_funcion):
                    elementos_encontrados += 1
            
            print(f"   📊 Elementos clave: {elementos_encontrados}/{len(elementos_clave)}")
        else:
            print("   ❌ Función cambiar_estado no encontrada")
        
        print("\n5. Estado del fix:")
        
        if imports_ok == len(importaciones) and sintaxis_ok:
            print("   ✅ Logger correctamente importado y configurado")
            print("   ✅ Archivo compila sin errores")
            print("   ✅ Función cambiar_estado debería funcionar")
        else:
            print("   ❌ Hay problemas que necesitan corrección")
        
        print("\n6. Para probar:")
        print("   1. Reiniciar web2py (importante para cargar los cambios)")
        print("   2. Ir a: http://127.0.0.1:8000/divisas2os/clientes/listar")
        print("   3. Intentar cambiar el estado de un cliente")
        print("   4. Verificar que no aparezca el error de 'logger not defined'")
        
        return imports_ok == len(importaciones) and sintaxis_ok
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {str(e)}")
        return False

if __name__ == "__main__":
    resultado = verificar_logger_fix()
    print(f"\n{'='*60}")
    if resultado:
        print("🎉 LOGGER FIX APLICADO CORRECTAMENTE")
    else:
        print("🔧 LOGGER FIX INCOMPLETO - Revisar correcciones")
    print(f"{'='*60}")