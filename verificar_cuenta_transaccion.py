#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gluon import DAL, Field

db = DAL('sqlite://storage.sqlite', folder='databases')

db.define_table('auth_user',
    Field('first_name'),
    Field('last_name'),
    Field('email')
)

db.define_table('clientes',
    Field('user_id', 'reference auth_user'),
    Field('cedula')
)

db.define_table('cuentas',
    Field('cliente_id', 'reference clientes'),
    Field('numero_cuenta')
)

# Buscar la cuenta
numero_cuenta = '20013632622832935010'
cuenta = db(db.cuentas.numero_cuenta == numero_cuenta).select().first()

if cuenta:
    print(f"Cuenta encontrada: {cuenta.numero_cuenta}")
    print(f"Cliente ID: {cuenta.cliente_id}")
    
    # Buscar el cliente
    cliente = db(db.clientes.id == cuenta.cliente_id).select().first()
    if cliente:
        print(f"Cliente cédula: {cliente.cedula}")
        print(f"Cliente user_id: {cliente.user_id}")
        
        # Buscar el usuario
        usuario = db(db.auth_user.id == cliente.user_id).select().first()
        if usuario:
            print(f"\nDatos del usuario:")
            print(f"Nombre: {usuario.first_name} {usuario.last_name}")
            print(f"Email: {usuario.email}")
else:
    print("Cuenta no encontrada")
