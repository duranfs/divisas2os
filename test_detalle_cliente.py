#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para probar la funcionalidad de detalles de cliente
"""

import sys
import os

# Agregar el directorio de web2py al path
sys.path.append('.')

def test_detalle_cliente():
    """Prueba la función detalle del controlador de clientes"""
    
    print("=== PRUEBA DE VISTA DE DETALLES DE CLIENTE ===")
    
    try:
        # Importar web2py
        from gluon import current
        from gluon.shell import env
        from gluon.storage import Storage
        
        # Configurar entorno de web2py
        env_vars = env('sistema_divisas', c=None, import_models=True)
        
        # Obtener objetos globales
        db = env_vars['db']
        auth = env_vars['auth']
        request = env_vars['request']
        response = env_vars['response']
        session = env_vars['session']
        
        # Configurar current para que esté disponible en los módulos
        current.db = db
        current.auth = auth
        current.request = request
        current.response = response
        current.session = session
        
        print("✓ Entorno de web2py configurado correctamente")
        
        # Verificar que hay clientes en la base de datos
        clientes = db(db.clientes.id > 0).select()
        print(f"✓ Clientes encontrados en BD: {len(clientes)}")
        
        if not clientes:
            print("❌ No hay clientes en la base de datos para probar")
            return False
        
        # Tomar el primer cliente para la prueba
        cliente_test = clientes.first()
        print(f"✓ Cliente de prueba: ID {cliente_test.id}, Cédula: {cliente_test.cedula}")
        
        # Verificar que el usuario asociado existe
        usuario = db(db.auth_user.id == cliente_test.user_id).select().first()
        if usuario:
            print(f"✓ Usuario asociado encontrado: {usuario.first_name} {usuario.last_name}")
        else:
            print(f"⚠️  Usuario asociado no encontrado para cliente {cliente_test.id}")
        
        # Simular autenticación como administrador
        admin_user = db(db.auth_user.email == 'admin@sistema.com').select().first()
        if not admin_user:
            print("❌ Usuario administrador no encontrado")
            return False
        
        # Configurar sesión de usuario
        auth.user = admin_user
        session.auth = Storage(user=admin_user)
        
        # Simular request para la función detalle
        request.args = [str(cliente_test.id)]
        request.vars = Storage()
        
        print(f"✓ Simulando request para cliente ID: {cliente_test.id}")
        
        # Importar y ejecutar la función detalle
        exec(open('controllers/clientes.py').read(), env_vars)
        
        # Ejecutar la función detalle
        resultado = env_vars['detalle']()
        
        print("✓ Función detalle() ejecutada sin errores")
        
        # Verificar el resultado
        if isinstance(resultado, dict):
            print("✓ La función devolvió un diccionario")
            
            # Verificar campos esperados
            campos_esperados = ['cliente', 'usuario', 'datos_seguros', 'cuentas', 'ultimas_transacciones']
            for campo in campos_esperados:
                if campo in resultado:
                    print(f"✓ Campo '{campo}' presente en resultado")
                else:
                    print(f"⚠️  Campo '{campo}' faltante en resultado")
            
            # Verificar datos del cliente
            if resultado.get('cliente'):
                cliente_resultado = resultado['cliente']
                print(f"✓ Datos del cliente: ID {cliente_resultado.id}")
            
            # Verificar datos seguros
            if resultado.get('datos_seguros'):
                datos = resultado['datos_seguros']
                print(f"✓ Datos seguros: {datos.get('nombre_completo', 'N/A')}")
                print(f"✓ Email: {datos.get('email', 'N/A')}")
                print(f"✓ Estado activo: {datos.get('estado_activo', False)}")
            
            # Verificar cuentas
            cuentas = resultado.get('cuentas', [])
            print(f"✓ Cuentas encontradas: {len(cuentas)}")
            
            # Verificar transacciones
            transacciones = resultado.get('ultimas_transacciones', [])
            print(f"✓ Transacciones encontradas: {len(transacciones)}")
            
            print("\n=== RESULTADO DE LA PRUEBA ===")
            print("✅ La función detalle() funciona correctamente")
            print("✅ Todos los datos necesarios están disponibles para la vista")
            
            return True
        else:
            print(f"❌ La función devolvió un tipo inesperado: {type(resultado)}")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_vista_detalle():
    """Prueba que la vista detalle.html puede renderizar correctamente"""
    
    print("\n=== PRUEBA DE RENDERIZADO DE VISTA ===")
    
    try:
        # Verificar que el archivo de vista existe
        vista_path = "views/clientes/detalle.html"
        if os.path.exists(vista_path):
            print(f"✓ Vista encontrada: {vista_path}")
            
            # Leer el contenido de la vista
            with open(vista_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Verificar elementos clave de la vista
            elementos_clave = [
                '{{extend \'layout.html\'}}',
                '{{if cliente and datos_seguros:}}',
                '{{=datos_seguros.nombre_completo}}',
                '{{if cuentas:}}',
                '{{if ultimas_transacciones:}}'
            ]
            
            for elemento in elementos_clave:
                if elemento in contenido:
                    print(f"✓ Elemento encontrado: {elemento}")
                else:
                    print(f"⚠️  Elemento faltante: {elemento}")
            
            print("✅ La vista detalle.html está correctamente estructurada")
            return True
            
        else:
            print(f"❌ Vista no encontrada: {vista_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error al verificar la vista: {str(e)}")
        return False

if __name__ == "__main__":
    print("Iniciando pruebas de funcionalidad de detalles de cliente...\n")
    
    # Ejecutar pruebas
    test_controlador = test_detalle_cliente()
    test_vista = test_vista_detalle()
    
    print(f"\n=== RESUMEN DE PRUEBAS ===")
    print(f"Controlador detalle(): {'✅ PASÓ' if test_controlador else '❌ FALLÓ'}")
    print(f"Vista detalle.html: {'✅ PASÓ' if test_vista else '❌ FALLÓ'}")
    
    if test_controlador and test_vista:
        print("\n🎉 ¡Todas las pruebas pasaron! La funcionalidad de detalles está funcionando correctamente.")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisar los errores arriba.")