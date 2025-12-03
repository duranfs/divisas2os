# -*- coding: utf-8 -*-
"""
Ver solo el último ticket de error
"""

import os
import pickle
import datetime

errors_dir = "errors"

if not os.path.exists(errors_dir):
    print("No hay directorio de errores")
    exit(1)

# Listar tickets
tickets = []
for filename in os.listdir(errors_dir):
    if filename.endswith('.log'):
        filepath = os.path.join(errors_dir, filename)
        mtime = os.path.getmtime(filepath)
        tickets.append((filename, filepath, mtime))

if not tickets:
    print("✓ No hay tickets de error")
    exit(0)

# Ordenar por fecha (más reciente primero)
tickets.sort(key=lambda x: x[2], reverse=True)

# Mostrar solo el más reciente
filename, filepath, mtime = tickets[0]
fecha = datetime.datetime.fromtimestamp(mtime)

print("=" * 80)
print(f"ÚLTIMO ERROR: {filename}")
print(f"Fecha: {fecha.strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

try:
    with open(filepath, 'rb') as f:
        ticket_data = pickle.load(f)
        
        if isinstance(ticket_data, dict):
            if 'traceback' in ticket_data:
                print("\nTRACEBACK:")
                print(ticket_data['traceback'])
except Exception as e:
    print(f"Error leyendo ticket: {str(e)}")
