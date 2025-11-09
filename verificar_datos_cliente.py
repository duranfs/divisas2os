#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificar que el cliente tiene los datos necesarios en la BD
"""

def verificar_datos_cliente():
    """Crear script para verificar datos del cliente en BD"""
    
    print("=" * 70)
    print("VERIFICACIÓN: Datos de Cliente en Base de Datos")
    print("=" * 70)
    
    print("POSIBLES PROBLEMAS IDENTIFICADOS:")
    print()
    
    print("1. PROBLEMA CON REGISTRO DE CLIENTE:")
    print("   - El cliente se registra correctamente")
    print("   - Se crea usuario en auth_user")
    print("   - Se crea registro en tabla clientes")
    print("   - Se asigna rol de cliente")
    print("   - Se crea cuenta bancaria inicial")
    print()
    
    print("2. PROBLEMA CON ACCESO A CUENTAS:")
    print("   - El controlador busca: db.clientes.user_id == auth.user.id")
    print("   - Si no encuentra cliente, redirige a registrar")
    print("   - Si encuentra cliente, busca sus cuentas")
    print("   - Si no hay cuentas, debería mostrar mensaje")
    print()
    
    print("3. POSIBLE CAUSA DEL PROBLEMA:")
    print("   A) El cliente no tiene rol 'cliente' asignado")
    print("   B) El registro en tabla 'clientes' no se creó")
    print("   C) La cuenta bancaria no se creó")
    print("   D) Hay error en get_user_roles()")
    print()
    
    print("4. SOLUCIÓN RECOMENDADA:")
    print("   Vamos a agregar debug/logging al controlador")
    print("   para ver exactamente qué está pasando")
    print()
    
    print("=" * 70)
    print("CREANDO VERSIÓN DE DEBUG DEL CONTROLADOR...")
    
    # Crear versión con debug
    debug_code = '''
# Agregar al inicio de la función index() en controllers/cuentas.py:

# DEBUG: Información del usuario actual
import logging
logger = logging.getLogger("web2py.app.debug")
logger.info(f"DEBUG - Usuario actual: {auth.user.id if auth.user else 'None'}")
logger.info(f"DEBUG - Email usuario: {auth.user.email if auth.user else 'None'}")

# DEBUG: Verificar roles
user_roles = get_user_roles()
logger.info(f"DEBUG - Roles del usuario: {user_roles}")

# DEBUG: Verificar si es cliente
if 'cliente' in user_roles:
    logger.info("DEBUG - Usuario tiene rol de cliente")
    cliente = db(db.clientes.user_id == auth.user.id).select().first()
    logger.info(f"DEBUG - Cliente encontrado: {cliente.id if cliente else 'None'}")
    
    if cliente:
        cuentas = db(db.cuentas.cliente_id == cliente.id).select()
        logger.info(f"DEBUG - Cuentas encontradas: {len(cuentas)}")
        for cuenta in cuentas:
            logger.info(f"DEBUG - Cuenta: {cuenta.numero_cuenta}, Estado: {cuenta.estado}")
else:
    logger.info("DEBUG - Usuario NO tiene rol de cliente")
'''
    
    print("CÓDIGO DE DEBUG PARA AGREGAR:")
    print("-" * 50)
    print(debug_code)
    print("-" * 50)
    
    print("\nINSTRUCCIONES:")
    print("1. Agrega el código de debug al inicio de la función index()")
    print("2. Haz login como cliente")
    print("3. Ve a 'Mis Cuentas'")
    print("4. Revisa los logs de web2py para ver qué está pasando")

if __name__ == "__main__":
    verificar_datos_cliente()