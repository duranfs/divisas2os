#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para leer el último ticket de error de web2py
"""

import os
import pickle
import glob
from datetime import datetime

errors_dir = r'C:\web2py\applications\divisas2os_multiple\errors'

def leer_ticket(ticket_path):
    """Lee y muestra el contenido de un ticket de error"""
    ticket_name = os.path.basename(ticket_path)
    print("=" * 80)
    print(f"TICKET: {ticket_name}")
    print("=" * 80)
    
    try:
        with open(ticket_path, 'rb') as f:
            ticket_data = pickle.load(f)
        
        # Mostrar información del error
        print(f"\n📅 Fecha: {ticket_data.get('date', 'N/A')}")
        print(f"🐍 Python: {ticket_data.get('pyver', 'N/A')}")
        print(f"\n❌ Error: {ticket_data.get('etype', 'N/A')}")
        print(f"💬 Mensaje: {ticket_data.get('evalue', 'N/A')}")
        
        # Mostrar traceback
        if 'traceback' in ticket_data:
            print(f"\n📋 Traceback:")
            print(ticket_data['traceback'])
        
        # Mostrar código si está disponible
        if 'code' in ticket_data and ticket_data['code']:
            print(f"\n💻 Código:")
            print(ticket_data['code'][:500])  # Primeros 500 caracteres
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"❌ Error leyendo ticket: {str(e)}")
        # Intentar leer como texto
        try:
            with open(ticket_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                print(f"\nContenido (primeros 1000 caracteres):")
                print(content[:1000])
        except:
            pass

# Obtener todos los tickets
tickets = glob.glob(os.path.join(errors_dir, '127.0.0.1*'))

if not tickets:
    print("No se encontraron tickets de error")
else:
    # Ordenar por fecha de modificación (más reciente primero)
    tickets.sort(key=os.path.getmtime, reverse=True)
    
    print(f"\nTotal de tickets encontrados: {len(tickets)}")
    print(f"\nÚltimos 5 tickets:")
    for i, ticket in enumerate(tickets[:5]):
        mtime = datetime.fromtimestamp(os.path.getmtime(ticket))
        print(f"  {i+1}. {os.path.basename(ticket)} - {mtime}")
    
    print(f"\n{'='*80}")
    print("LEYENDO EL TICKET MÁS RECIENTE:")
    print(f"{'='*80}\n")
    
    leer_ticket(tickets[0])
