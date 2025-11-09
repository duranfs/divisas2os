
import sys
import os
sys.path.insert(0, 'C:\web2py')

from gluon import *
from gluon.storage import Storage

# Simular request con datos de prueba
request = Storage()
request.vars = Storage()
request.vars.first_name = "María Elena"
request.vars.last_name = "González Rodríguez"
request.vars.cedula = "V-87654321"
request.vars.email = "maria.gonzalez.test@email.com"
request.vars.telefono = "04241234567"
request.vars.direccion = "Calle 123, Maracaibo, Zulia"
request.vars.fecha_nacimiento = "1985-03-20"
request.vars.password = "password123"
request.vars.password_confirm = "password123"

print("Datos de request.vars configurados")
print("Email:", request.vars.email)
print("Cédula:", request.vars.cedula)

# Simular response y session
response = Storage()
response.flash = ""
session = Storage()

print("\nSimulando registro de cliente...")
print("Nota: Este script requiere ejecutarse desde web2py para funcionar completamente")
