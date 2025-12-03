# -*- coding: utf-8 -*-
"""
Script para leer tickets de error de web2py de forma legible
"""

import os
import pickle
import datetime

print("=" * 80)
print("LECTOR DE TICKETS DE ERROR - web2py")
print("=" * 80)

# Directorio de errores
errors_dir = "errors"

if not os.path.exists(errors_dir):
    print(f"\n❌ No se encontró el directorio de errores: {errors_dir}")
    exit(1)

# Listar todos los archivos de ticket
tickets = []
for filename in os.listdir(errors_dir):
    # Los tickets de web2py no tienen extensión, solo el formato IP.fecha.uuid
    if filename.startswith('127.0.0.1'):
        filepath = os.path.join(errors_dir, filename)
        # Obtener fecha de modificación
        mtime = os.path.getmtime(filepath)
        tickets.append((filename, filepath, mtime))

if not tickets:
    print("\n✓ No hay tickets de error registrados")
    exit(0)

# Ordenar por fecha (más recientes primero)
tickets.sort(key=lambda x: x[2], reverse=True)

print(f"\n✓ Se encontraron {len(tickets)} ticket(s) de error")
print("\nMostrando los 5 más recientes:\n")

for i, (filename, filepath, mtime) in enumerate(tickets[:5], 1):
    fecha = datetime.datetime.fromtimestamp(mtime)
    print(f"\n{'=' * 80}")
    print(f"TICKET #{i}: {filename}")
    print(f"Fecha: {fecha.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 80}")
    
    try:
        # Intentar leer como pickle
        with open(filepath, 'rb') as f:
            try:
                ticket_data = pickle.load(f)
                
                # Mostrar información del ticket
                if isinstance(ticket_data, dict):
                    print("\n📋 INFORMACIÓN DEL ERROR:")
                    
                    if 'traceback' in ticket_data:
                        print("\n🔴 TRACEBACK:")
                        print(ticket_data['traceback'])
                    
                    if 'snapshot' in ticket_data:
                        snapshot = ticket_data['snapshot']
                        if 'request' in snapshot:
                            req = snapshot['request']
                            print(f"\n📍 REQUEST:")
                            print(f"  URL: {req.get('url', 'N/A')}")
                            print(f"  Método: {req.get('method', 'N/A')}")
                            print(f"  Cliente: {req.get('client', 'N/A')}")
                        
                        if 'variables' in snapshot:
                            print(f"\n📦 VARIABLES:")
                            for key, value in snapshot['variables'].items():
                                print(f"  {key}: {value}")
                else:
                    print(f"\nContenido: {ticket_data}")
                    
            except pickle.UnpicklingError:
                # Si no es pickle, intentar leer como texto
                f.seek(0)
                content = f.read()
                try:
                    print(content.decode('utf-8'))
                except:
                    print(content.decode('latin-1', errors='ignore'))
                    
    except Exception as e:
        print(f"\n❌ Error leyendo ticket: {str(e)}")
        # Intentar leer como texto plano
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                print(f.read())
        except:
            print("No se pudo leer el archivo")

print(f"\n{'=' * 80}")
print(f"Total de tickets: {len(tickets)}")
print(f"{'=' * 80}")
