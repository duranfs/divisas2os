#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Diagnosticar problema con vista de cuentas para clientes
"""

import os

def diagnosticar_cuentas_cliente():
    """Diagnosticar por qué no aparecen datos bancarios para clientes"""
    
    print("=" * 70)
    print("DIAGNÓSTICO: Vista de Cuentas para Clientes")
    print("=" * 70)
    
    # 1. Verificar controlador
    print("1. VERIFICANDO CONTROLADOR cuentas.py:")
    if os.path.exists("controllers/cuentas.py"):
        with open("controllers/cuentas.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            # Buscar función index
            if "def index():" in contenido:
                print("   ✓ Función index() existe")
                
                # Verificar validación de cliente
                if "'cliente' in user_roles:" in contenido:
                    print("   ✓ Valida rol de cliente")
                else:
                    print("   ❌ NO valida rol de cliente")
                
                # Verificar obtención de cliente
                if "cliente = db(db.clientes.user_id == auth.user.id)" in contenido:
                    print("   ✓ Obtiene cliente por user_id")
                else:
                    print("   ❌ NO obtiene cliente correctamente")
                
                # Verificar obtención de cuentas
                if "cuentas = db(db.cuentas.cliente_id == cliente.id)" in contenido:
                    print("   ✓ Obtiene cuentas del cliente")
                else:
                    print("   ❌ NO obtiene cuentas del cliente")
                
                # Verificar return
                if "return dict(" in contenido and "cuentas=cuentas" in contenido:
                    print("   ✓ Retorna datos de cuentas")
                else:
                    print("   ❌ NO retorna datos correctamente")
            else:
                print("   ❌ Función index() NO encontrada")
    
    # 2. Verificar vista
    print("\n2. VERIFICANDO VISTA index.html:")
    if os.path.exists("views/cuentas/index.html"):
        with open("views/cuentas/index.html", 'r', encoding='utf-8') as f:
            contenido_vista = f.read()
            
            print("   ✓ Vista index.html existe")
            
            # Verificar elementos clave
            if "{{if cuentas:}}" in contenido_vista:
                print("   ✓ Verifica si hay cuentas")
            else:
                print("   ❌ NO verifica si hay cuentas")
            
            if "{{for cuenta in cuentas:}}" in contenido_vista:
                print("   ✓ Itera sobre cuentas")
            else:
                print("   ❌ NO itera sobre cuentas")
            
            if "{{else:}}" in contenido_vista:
                print("   ✓ Tiene caso para sin cuentas")
            else:
                print("   ❌ NO maneja caso sin cuentas")
    
    # 3. Verificar posibles problemas
    print("\n3. POSIBLES PROBLEMAS:")
    print("   A) El cliente no tiene registro en tabla 'clientes'")
    print("   B) El cliente no tiene cuentas asociadas")
    print("   C) Hay error en la consulta de base de datos")
    print("   D) La vista no está mostrando datos correctamente")
    
    print("\n4. VERIFICACIONES RECOMENDADAS:")
    print("   - Verificar que el cliente esté en tabla 'clientes'")
    print("   - Verificar que tenga cuentas en tabla 'cuentas'")
    print("   - Revisar logs de errores en web2py")
    print("   - Verificar que la función get_user_roles() funciona")
    
    print("\n" + "=" * 70)
    print("SIGUIENTE PASO:")
    print("Vamos a verificar si el problema está en los datos")
    print("o en la lógica del controlador/vista.")

if __name__ == "__main__":
    diagnosticar_cuentas_cliente()