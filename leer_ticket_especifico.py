# -*- coding: utf-8 -*-
"""
Leer un ticket de error específico
"""

import os
import pickle
import sys

ticket_name = "127.0.0.1.2025-11-27.18-52-28.a044fd48-f31e-41db-874b-670614fc2fba"
errors_dir = "errors"
filepath = os.path.join(errors_dir, ticket_name)

if not os.path.exists(filepath):
    print(f"❌ Ticket no encontrado: {filepath}")
    exit(1)

print("=" * 80)
print(f"TICKET: {ticket_name}")
print("=" * 80)

try:
    with open(filepath, 'rb') as f:
        ticket_data = pickle.load(f)
        
        if isinstance(ticket_data, dict):
            print("\n🔴 TRACEBACK:")
            if 'traceback' in ticket_data:
                print(ticket_data['traceback'])
            
            print("\n📍 REQUEST INFO:")
            if 'snapshot' in ticket_data and 'request' in ticket_data['snapshot']:
                req = ticket_data['snapshot']['request']
                print(f"  URL: {req.get('url', 'N/A')}")
                print(f"  Método: {req.get('method', 'N/A')}")
                print(f"  Función: {req.get('function', 'N/A')}")
                print(f"  Controlador: {req.get('controller', 'N/A')}")
        else:
            print(ticket_data)
            
except Exception as e:
    print(f"❌ Error leyendo ticket: {str(e)}")
    # Intentar leer como texto
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Buscar el traceback
            if 'Traceback' in content:
                start = content.find('Traceback')
                end = content.find('\n\n', start)
                if end == -1:
                    end = len(content)
                print(content[start:end])
            else:
                print(content[:2000])  # Primeros 2000 caracteres
    except:
        print("No se pudo leer el archivo")

print("\n" + "=" * 80)
