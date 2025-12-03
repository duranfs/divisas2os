# -*- coding: utf-8 -*-
"""
Script para leer y mostrar el contenido del último ticket de error
"""

import os
import pickle

# Buscar el último ticket de error
errors_dir = 'errors'
tickets = [f for f in os.listdir(errors_dir) if f.startswith('127.0.0.1')]

if not tickets:
    print("No hay tickets de error")
else:
    # Ordenar por fecha (más reciente primero)
    tickets.sort(reverse=True)
    ultimo_ticket = tickets[0]
    
    print("=" * 80)
    print(f"Último ticket de error: {ultimo_ticket}")
    print("=" * 80)
    
    ticket_path = os.path.join(errors_dir, ultimo_ticket)
    
    try:
        # Los tickets de web2py están en formato pickle
        with open(ticket_path, 'rb') as f:
            ticket_data = pickle.load(f)
        
        print("\nInformación del error:")
        print("-" * 80)
        
        if isinstance(ticket_data, dict):
            for key, value in ticket_data.items():
                if key == 'traceback':
                    print(f"\n{key}:")
                    print(value)
                elif key not in ['snapshot', 'code']:
                    print(f"{key}: {value}")
        else:
            print(ticket_data)
            
    except Exception as e:
        print(f"Error leyendo ticket: {str(e)}")
        print("\nIntentando leer como texto plano...")
        try:
            with open(ticket_path, 'r', encoding='utf-8', errors='ignore') as f:
                print(f.read())
        except:
            print("No se pudo leer el archivo")
