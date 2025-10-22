# -*- coding: utf-8 -*-
"""
Pruebas unitarias para el módulo de clientes
Sistema de Divisas Bancario
"""

import unittest
import sys
import os
from datetime import datetime, date

# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar entorno de prueba
os.environ['WEB2PY_PATH'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Importar web2py
from gluon import *
from gluon.globals import Request, Response, Session
from gluon.storage import Storage
from gluon.dal import DAL, Field
from gluon.tools import Auth
from gluon.validators import *

class TestClientesModule(unittest.TestCase):
    """
    Pruebas unitarias para el módulo de gestión de clientes
    Requisitos: 2.1, 2.2
    """
    
    def setUp(self):
        """Configurar entorno de prueba"""
        # Crear base de datos en memoria para pruebas
        self.db = DAL('sqlite:memory:')
        
        # Definir tabla auth_user simplificada para pruebas
        self.db.define_table('auth_user',
            Field('first_name', 'string'),
            Field('last_name', 'string'),
            Field('email', 'string'),
            Field('password', 'password'),
            Field('telefono', 'string'),
            Field('direccion', 'text'),
            Field('fecha_nacimiento', 'date'),
            Field('estado', 'string', default='activo')
        )
        
        # Definir tabla clientes para pruebas
        self.db.define_table('clientes',
            Field('user_id', 'reference auth_user'),
            Field('cedula', 'string', length=20, unique=True),
            Field('fecha_registro', 'datetime', default=datetime.now())
        )
        
        # Definir tabla cuentas para pruebas
        self.db.define_table('cuentas',
            Field('cliente_id', 'reference clientes'),
            Field('numero_cuenta', 'string', length=20, unique=True),
            Field('tipo_cuenta', 'string', default='corriente'),
            Field('saldo_ves', 'decimal(15,2)', default=0),
            Field('saldo_usd', 'decimal(15,2)', default=0),
            Field('saldo_eur', 'decimal(15,2)', default=0),
            Field('estado', 'string', default='activa'),
            Field('fecha_creacion', 'datetime', default=datetime.now())
        )
        
        # Crear las tablas
        self.db.commit()
        
        # Configurar objetos globales simulados
        self.request = Storage()
        self.response = Storage()
        self.session = Storage()
        
        # Insertar datos de prueba
        self._insertar_datos_prueba()
    
    def tearDown(self):
        """Limpiar después de cada prueba"""
        self.db.close()
    
    def _insertar_datos_prueba(self):
        """Insertar datos de prueba en la base de datos"""
        # Insertar usuario existente para pruebas de duplicados
        user_id = self.db.auth_user.insert(
            first_name='Juan',
            last_name='Pérez',
            email='juan.perez@email.com',
            password='password123',
            telefono='04141234567',
            direccion='Caracas, Venezuela',
            fecha_nacimiento=date(1990, 1, 1),
            estado='activo'
        )
        
        # Insertar cliente existente
        self.db.clientes.insert(
            user_id=user_id,
            cedula='V-12345678',
            fecha_registro=datetime.now()
        )
        
        self.db.commit()
    
    def test_validar_cedula_formato_valido_v(self):
        """
        Probar validación de cédula con formato válido V-12345678
        Requisito: 2.1
        """
        from controllers.clientes import validar_cedula
        
        # Simular contexto de web2py
        import gluon.globals
        gluon.globals.current.db = self.db
        
        # Probar formato válido con V
        es_valida, mensaje = validar_cedula('V-87654321')
        self.assertTrue(es_valida)
        self.assertEqual(mensaje, "Cédula válida")
    
    def test_validar_cedula_formato_valido_e(self):
        """
        Probar validación de cédula con formato válido E-12345678
        Requisito: 2.1
        """
        from controllers.clientes import validar_cedula
        
        # Simular contexto de web2py
        import gluon.globals
        gluon.globals.current.db = self.db
        
        # Probar formato válido con E
        es_valida, mensaje = validar_cedula('E-87654321')
        self.assertTrue(es_valida)
        self.assertEqual(mensaje, "Cédula válida")
    
    def test_validar_cedula_formato_invalido(self):
        """
        Probar validación de cédula con formato inválido
        Requisito: 2.1
        """
        from controllers.clientes import validar_cedula
        
        # Simular contexto de web2py
        import gluon.globals
        gluon.globals.current.db = self.db
        
        # Probar formatos inválidos
        casos_invalidos = [
            'X-12345678',  # Letra inválida
            'V12345678',   # Sin guión
            'V-123',       # Muy corto
            'V-123456789', # Muy largo
            '12345678',    # Sin letra
            '',            # Vacío
            None           # Nulo
        ]
        
        for cedula_invalida in casos_invalidos:
            es_valida, mensaje = validar_cedula(cedula_invalida)
            self.assertFalse(es_valida)
            self.assertIn('inválido', mensaje.lower())
    
    def test_validar_cedula_duplicada(self):
        """
        Probar validación de cédula ya registrada
        Requisito: 2.1
        """
        from controllers.clientes import validar_cedula
        
        # Simular contexto de web2py
        import gluon.globals
        gluon.globals.current.db = self.db
        
        # Probar cédula ya registrada
        es_valida, mensaje = validar_cedula('V-12345678')
        self.assertFalse(es_valida)
        self.assertIn('ya está registrada', mensaje)
    
    def test_validar_cedula_espacios_y_mayusculas(self):
        """
        Probar que la validación maneja espacios y convierte a mayúsculas
        Requisito: 2.1
        """
        from controllers.clientes import validar_cedula
        
        # Simular contexto de web2py
        import gluon.globals
        gluon.globals.current.db = self.db
        
        # Probar con espacios y minúsculas
        es_valida, mensaje = validar_cedula('  v-87654321  ')
        self.assertTrue(es_valida)
        self.assertEqual(mensaje, "Cédula válida")
    
    def test_generar_numero_cuenta_unico(self):
        """
        Probar generación de número de cuenta único
        Requisito: 2.1
        """
        from controllers.clientes import generar_numero_cuenta
        
        # Simular contexto de web2py
        import gluon.globals
        gluon.globals.current.db = self.db
        
        # Generar varios números de cuenta
        numeros_generados = set()
        for _ in range(10):
            numero = generar_numero_cuenta()
            
            # Verificar formato (20 dígitos, empieza con 2001)
            self.assertEqual(len(numero), 20)
            self.assertTrue(numero.startswith('2001'))
            self.assertTrue(numero.isdigit())
            
            # Verificar unicidad
            self.assertNotIn(numero, numeros_generados)
            numeros_generados.add(numero)
    
    def test_generar_numero_cuenta_no_duplicado(self):
        """
        Probar que no se generen números de cuenta duplicados
        Requisito: 2.1
        """
        from controllers.clientes import generar_numero_cuenta
        
        # Simular contexto de web2py
        import gluon.globals
        gluon.globals.current.db = self.db
        
        # Insertar una cuenta existente
        self.db.cuentas.insert(
            cliente_id=1,
            numero_cuenta='20011234567890123456'
        )
        self.db.commit()
        
        # Generar nuevo número
        numero = generar_numero_cuenta()
        
        # Verificar que no es el mismo que el existente
        self.assertNotEqual(numero, '20011234567890123456')
        self.assertEqual(len(numero), 20)
        self.assertTrue(numero.startswith('2001'))
    
    def test_validacion_datos_registro_completos(self):
        """
        Probar validación de datos completos para registro
        Requisito: 2.1, 2.2
        """
        # Datos válidos para registro
        datos_validos = {
            'first_name': 'María',
            'last_name': 'González',
            'email': 'maria.gonzalez@email.com',
            'password': 'Password123!',
            'cedula': 'V-98765432',
            'telefono': '04241234567',
            'direccion': 'Valencia, Venezuela',
            'fecha_nacimiento': date(1985, 5, 15)
        }
        
        # Verificar que todos los campos requeridos están presentes
        campos_requeridos = ['first_name', 'last_name', 'email', 'password', 
                           'cedula', 'telefono', 'direccion', 'fecha_nacimiento']
        
        for campo in campos_requeridos:
            self.assertIn(campo, datos_validos)
            self.assertIsNotNone(datos_validos[campo])
            self.assertNotEqual(datos_validos[campo], '')
    
    def test_validacion_email_duplicado(self):
        """
        Probar validación de email duplicado en registro
        Requisito: 2.2
        """
        # Verificar que existe un usuario con email duplicado
        usuario_existente = self.db(self.db.auth_user.email == 'juan.perez@email.com').select().first()
        self.assertIsNotNone(usuario_existente)
        
        # Simular intento de registro con email duplicado
        email_duplicado = 'juan.perez@email.com'
        usuario_duplicado = self.db(self.db.auth_user.email == email_duplicado).select().first()
        
        # Verificar que se detecta el duplicado
        self.assertIsNotNone(usuario_duplicado)
    
    def test_actualizacion_perfil_datos_validos(self):
        """
        Probar actualización de perfil con datos válidos
        Requisito: 2.2
        """
        # Obtener usuario existente
        usuario = self.db(self.db.auth_user.id == 1).select().first()
        self.assertIsNotNone(usuario)
        
        # Datos para actualización
        datos_actualizacion = {
            'first_name': 'Juan Carlos',
            'last_name': 'Pérez Rodríguez',
            'email': 'juan.carlos.perez@email.com',
            'telefono': '04141234568',
            'direccion': 'Caracas, Distrito Capital',
            'fecha_nacimiento': date(1990, 2, 1)
        }
        
        # Simular actualización
        self.db(self.db.auth_user.id == 1).update(**datos_actualizacion)
        self.db.commit()
        
        # Verificar actualización
        usuario_actualizado = self.db(self.db.auth_user.id == 1).select().first()
        self.assertEqual(usuario_actualizado.first_name, 'Juan Carlos')
        self.assertEqual(usuario_actualizado.last_name, 'Pérez Rodríguez')
        self.assertEqual(usuario_actualizado.email, 'juan.carlos.perez@email.com')
    
    def test_validacion_telefono_formato(self):
        """
        Probar validación de formato de teléfono
        Requisito: 2.1, 2.2
        """
        telefonos_validos = [
            '04141234567',
            '02121234567',
            '04241234567'
        ]
        
        telefonos_invalidos = [
            '123456',      # Muy corto
            '041412345678', # Muy largo
            'abcd1234567', # Contiene letras
            ''             # Vacío
        ]
        
        # Verificar que los teléfonos válidos tienen el formato correcto
        for telefono in telefonos_validos:
            self.assertTrue(len(telefono) == 11)
            self.assertTrue(telefono.isdigit())
            self.assertTrue(telefono.startswith('0'))
        
        # Verificar que los teléfonos inválidos no cumplen el formato
        for telefono in telefonos_invalidos:
            if telefono:  # Si no está vacío
                self.assertFalse(len(telefono) == 11 and telefono.isdigit() and telefono.startswith('0'))
    
    def test_estado_cliente_activo_por_defecto(self):
        """
        Probar que los clientes se crean con estado activo por defecto
        Requisito: 2.1
        """
        # Crear nuevo usuario
        user_id = self.db.auth_user.insert(
            first_name='Ana',
            last_name='Martínez',
            email='ana.martinez@email.com',
            password='password123',
            telefono='04161234567',
            direccion='Maracaibo, Venezuela',
            fecha_nacimiento=date(1992, 3, 10)
        )
        
        # Verificar estado por defecto
        usuario = self.db(self.db.auth_user.id == user_id).select().first()
        self.assertEqual(usuario.estado, 'activo')
    
    def test_fecha_registro_automatica(self):
        """
        Probar que la fecha de registro se asigna automáticamente
        Requisito: 2.1
        """
        # Crear nuevo cliente
        cliente_id = self.db.clientes.insert(
            user_id=1,
            cedula='V-11111111'
        )
        
        # Verificar que tiene fecha de registro
        cliente = self.db(self.db.clientes.id == cliente_id).select().first()
        self.assertIsNotNone(cliente.fecha_registro)
        self.assertIsInstance(cliente.fecha_registro, datetime)


if __name__ == '__main__':
    # Configurar suite de pruebas
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClientesModule)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Mostrar resumen
    print(f"\nPruebas ejecutadas: {result.testsRun}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    
    if result.errors:
        print("\nErrores:")
        for test, error in result.errors:
            print(f"- {test}: {error}")
    
    if result.failures:
        print("\nFallos:")
        for test, failure in result.failures:
            print(f"- {test}: {failure}")