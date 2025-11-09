#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificar columnas de la tabla clientes
"""

import sqlite3

def verificar():
    """Verificar estructura de clientes"""
    
    print("🔍 VERIFICANDO ESTRUCTURA DE TABLA CLIENTES")
    print("="*70)
    
    try:
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        # Ver estructura de clientes
        cursor.execute("PRAGMA table_info(clientes)")
        columnas = cursor.fetchall()
        
        print("\n📋 COLUMNAS DE LA TABLA clientes:")
        for col in columnas:
            cid, nombre, tipo, notnull, default, pk = col
            print(f"   {nombre} ({tipo})")
        
        # Ver un registro de ejemplo
        print("\n📊 REGISTRO DE EJEMPLO:")
        cursor.execute("SELECT * FROM clientes LIMIT 1")
        registro = cursor.fetchone()
        
        if registro:
            for i, col in enumerate(columnas):
                nombre = col[1]
                valor = registro[i]
                print(f"   {nombre}: {valor}")
        
        conn.close()
        
        print("\n" + "="*70)
        print("🔧 SOLUCIÓN:")
        print("="*70)
        print()
        print("La tabla clientes NO tiene 'first_name' y 'last_name'.")
        print("Probablemente tiene 'nombre' y 'apellido' o similar.")
        print()
        print("Necesito corregir la consulta en controllers/divisas.py")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    verificar()
