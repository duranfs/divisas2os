#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Diagnóstico completo del problema de login
"""

import os

def diagnosticar_login():
    """Diagnosticar todos los aspectos del problema de login"""
    
    print("=" * 70)
    print("DIAGNÓSTICO COMPLETO: Problema de Login")
    print("=" * 70)
    
    # 1. Verificar función de registro
    print("1. VERIFICANDO FUNCIÓN DE REGISTRO:")
    if os.path.exists("controllers/clientes.py"):
        with open("controllers/clientes.py", 'r', encoding='utf-8') as f:
            contenido = f.read()
            
            if "CRYPT()" in contenido:
                print("   ✓ Usa CRYPT() para hashear contraseña")
            else:
                print("   ❌ NO usa CRYPT()")
            
            if "hashed_password = str(crypt_validator" in contenido:
                print("   ✓ Convierte hash a string")
            else:
                print("   ❌ NO convierte hash a string")
    
    # 2. Verificar configuración de auth en models
    print("\n2. VERIFICANDO CONFIGURACIÓN DE AUTH:")
    if os.path.exists("models/db.py"):
        with open("models/db.py", 'r', encoding='utf-8') as f:
            contenido_db = f.read()
            
            if "auth.define_tables()" in contenido_db:
                print("   ✓ auth.define_tables() está presente")
            else:
                print("   ❌ auth.define_tables() NO encontrado")
            
            if "CRYPT(" in contenido_db:
                print("   ✓ CRYPT configurado en models")
            else:
                print("   ❌ CRYPT NO configurado en models")
    
    # 3. Verificar estructura de tabla auth_user
    print("\n3. POSIBLES PROBLEMAS:")
    print("   - ¿El campo 'estado' existe en auth_user?")
    print("   - ¿La configuración de CRYPT es compatible?")
    print("   - ¿Hay validaciones adicionales en auth?")
    
    print("\n4. SOLUCIONES ALTERNATIVAS:")
    print("   A) Usar auth.get_or_create_user() en lugar de insert directo")
    print("   B) Verificar configuración de auth en models/db.py")
    print("   C) Usar el mismo algoritmo de hash que auth por defecto")
    
    print("\n" + "=" * 70)
    print("RECOMENDACIÓN:")
    print("Si el problema persiste, puede ser necesario:")
    print("1. Verificar la configuración de auth en models/db.py")
    print("2. Usar auth.get_or_create_user() en lugar de insert directo")
    print("3. Verificar que no hay validaciones adicionales bloqueando el login")

if __name__ == "__main__":
    diagnosticar_login()