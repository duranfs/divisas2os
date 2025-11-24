#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os

# Ruta a la base de datos
db_path = r'C:\web2py\applications\sistema_divisas\databases\storage.sqlite'

if not os.path.exists(db_path):
    print("ERROR: No se encuentra la base de datos en:", db_path)
    print("Buscando en ubicaciones alternativas...")
    
    # Intentar otras ubicaciones
    alt_paths = [
        r'C:\web2py\applications\divisas2os\databases\storage.sqlite',
        r'C:\web2py\databases\storage.sqlite'
    ]
    
    for alt_path in alt_paths:
        if os.path.exists(alt_path):
            db_path = alt_path
            print("Base de datos encontrada en:", db_path)
            break
    else:
        print("No se pudo encontrar la base de datos")
        input("Presiona Enter para salir...")
        exit(1)

print("=" * 80)
print("ACTUALIZACIÓN DIRECTA DE USDT EN BASE DE DATOS")
print("=" * 80)
print("Base de datos:", db_path)

try:
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ver la tasa actual
    cursor.execute("SELECT id, usd_ves, usdt_ves, eur_ves, activa FROM tasas_cambio WHERE activa = 1")
    tasa_actual = cursor.fetchone()
    
    if tasa_actual:
        print("\nTASA ACTUAL:")
        print("ID:", tasa_actual[0])
        print("USD/VES:", tasa_actual[1])
        print("USDT/VES:", tasa_actual[2])
        print("EUR/VES:", tasa_actual[3])
        
        # Actualizar USDT a 241.76
        nuevo_usdt = 241.76
        print("\nActualizando USDT/VES a", nuevo_usdt, "...")
        
        cursor.execute("UPDATE tasas_cambio SET usdt_ves = ? WHERE id = ?", (nuevo_usdt, tasa_actual[0]))
        conn.commit()
        
        # Verificar
        cursor.execute("SELECT usd_ves, usdt_ves, eur_ves FROM tasas_cambio WHERE id = ?", (tasa_actual[0],))
        tasa_nueva = cursor.fetchone()
        
        print("\nTASA ACTUALIZADA:")
        print("USD/VES:", tasa_nueva[0])
        print("USDT/VES:", tasa_nueva[1])
        print("EUR/VES:", tasa_nueva[2])
        
        print("\n✓ ACTUALIZACIÓN EXITOSA")
    else:
        print("\nNo se encontró ninguna tasa activa")
        
        # Mostrar todas las tasas
        cursor.execute("SELECT id, usd_ves, usdt_ves, activa FROM tasas_cambio ORDER BY id DESC LIMIT 5")
        todas = cursor.fetchall()
        print("\nÚltimas 5 tasas en la base de datos:")
        for t in todas:
            print("ID:", t[0], "USD:", t[1], "USDT:", t[2], "Activa:", t[3])
    
    conn.close()
    
except Exception as e:
    print("\nERROR:", str(e))

print("\n" + "=" * 80)
print("Recarga la página del navegador para ver los cambios")
print("=" * 80)
input("\nPresiona Enter para salir...")
