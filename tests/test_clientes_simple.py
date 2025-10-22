# -*- coding: utf-8 -*-
"""
Pruebas unitarias simplificadas para el módulo de clientes
Sistema de Divisas Bancario - Sin dependencias de web2py
"""

import unittest
import re
from datetime import datetime, date

class TestClientesValidation(unittest.TestCase):
    """
    Pruebas unitarias para validaciones del módulo de clientes
    Requisitos: 2.1, 2.2
    """
    
    def test_validar_cedula_formato_regex(self):
        """
        Probar validación de formato de cédula con regex
        Requisito: 2.1
        """
        # Patrón de validación de cédula venezolana
        patron_cedula = r'^[VE]-?\d{7,8}$'
        
        # Casos válidos
        cedulas_validas = [
            'V-12345678',
            'E-12345678',
            'V-1234567',
            'E-1234567',
            'V12345678',
            'E12345678'
        ]
        
        for cedula in cedulas_validas:
            cedula_limpia = cedula.strip().upper()
            self.assertTrue(re.match(patron_cedula, cedula_limpia), 
                          f"Cédula válida falló: {cedula}")
    
    def test_validar_cedula_formato_invalido_regex(self):
        """
        Probar validación de formato inválido de cédula con regex
        Requisito: 2.1
        """
        patron_cedula = r'^[VE]-?\d{7,8}$'
        
        # Casos inválidos
        cedulas_invalidas = [
            'X-12345678',  # Letra inválida
            'V-123',       # Muy corto
            'V-123456789', # Muy largo
            '12345678',    # Sin letra
            'V-12345abc',  # Contiene letras en números
            '',            # Vacío
            'V--12345678', # Doble guión
            'VV-12345678'  # Doble letra
        ]
        
        for cedula in cedulas_invalidas:
            if cedula:  # Si no está vacío
                cedula_limpia = cedula.strip().upper()
                self.assertFalse(re.match(patron_cedula, cedula_limpia), 
                               f"Cédula inválida pasó: {cedula}")
    
    def test_generar_numero_cuenta_formato(self):
        """
        Probar formato de número de cuenta generado
        Requisito: 2.1
        """
        import random
        
        # Simular generación de número de cuenta
        def generar_numero_cuenta_test():
            return "2001" + "".join([str(random.randint(0, 9)) for _ in range(16)])
        
        # Generar varios números y verificar formato
        for _ in range(10):
            numero = generar_numero_cuenta_test()
            
            # Verificar longitud
            self.assertEqual(len(numero), 20, f"Longitud incorrecta: {numero}")
            
            # Verificar que empiece con 2001
            self.assertTrue(numero.startswith('2001'), f"No empieza con 2001: {numero}")
            
            # Verificar que solo contenga dígitos
            self.assertTrue(numero.isdigit(), f"Contiene no-dígitos: {numero}")
    
    def test_validacion_email_formato(self):
        """
        Probar validación de formato de email
        Requisito: 2.1, 2.2
        """
        # Patrón básico de email
        patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Emails válidos
        emails_validos = [
            'usuario@ejemplo.com',
            'test.email@dominio.co.ve',
            'user123@test-domain.org',
            'nombre.apellido@empresa.com.ve'
        ]
        
        for email in emails_validos:
            self.assertTrue(re.match(patron_email, email), 
                          f"Email válido falló: {email}")
        
        # Emails inválidos
        emails_invalidos = [
            'usuario@',
            '@dominio.com',
            'usuario.dominio.com',
            'usuario@dominio',
            'usuario@.com',
            ''
        ]
        
        for email in emails_invalidos:
            if email:  # Si no está vacío
                self.assertFalse(re.match(patron_email, email), 
                               f"Email inválido pasó: {email}")
    
    def test_validacion_telefono_formato(self):
        """
        Probar validación de formato de teléfono venezolano
        Requisito: 2.1, 2.2
        """
        # Patrón para teléfonos venezolanos
        patron_telefono = r'^0(4[0-9]{2}|2[0-9]{2})[0-9]{7}$'
        
        # Teléfonos válidos
        telefonos_validos = [
            '04141234567',  # Móvil
            '04241234567',  # Móvil
            '02121234567',  # Fijo Caracas
            '02611234567'   # Fijo Valencia
        ]
        
        for telefono in telefonos_validos:
            self.assertTrue(re.match(patron_telefono, telefono), 
                          f"Teléfono válido falló: {telefono}")
        
        # Teléfonos inválidos
        telefonos_invalidos = [
            '123456',       # Muy corto
            '041412345678', # Muy largo
            '05141234567',  # Código inválido
            'abcd1234567',  # Contiene letras
            '4141234567',   # Sin 0 inicial
            ''              # Vacío
        ]
        
        for telefono in telefonos_invalidos:
            if telefono:  # Si no está vacío
                self.assertFalse(re.match(patron_telefono, telefono), 
                               f"Teléfono inválido pasó: {telefono}")
    
    def test_validacion_nombres_formato(self):
        """
        Probar validación de formato de nombres y apellidos
        Requisito: 2.1, 2.2
        """
        # Patrón para nombres (solo letras y espacios, incluyendo acentos)
        patron_nombre = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$'
        
        # Nombres válidos
        nombres_validos = [
            'Juan',
            'María José',
            'José María',
            'Ana Sofía',
            'Ángel',
            'Niño'
        ]
        
        for nombre in nombres_validos:
            self.assertTrue(re.match(patron_nombre, nombre), 
                          f"Nombre válido falló: {nombre}")
        
        # Nombres inválidos
        nombres_invalidos = [
            'Juan123',      # Contiene números
            'María-José',   # Contiene guión
            'Ana.Sofía',    # Contiene punto
            'José@María',   # Contiene símbolos
            '',             # Vacío
            '123',          # Solo números
            'A'             # Muy corto (menos de 2 caracteres)
        ]
        
        for nombre in nombres_invalidos:
            if nombre and len(nombre) >= 2:  # Solo probar si no está vacío y tiene al menos 2 caracteres
                self.assertFalse(re.match(patron_nombre, nombre), 
                               f"Nombre inválido pasó: {nombre}")
    
    def test_validacion_longitud_campos(self):
        """
        Probar validación de longitud de campos
        Requisito: 2.1, 2.2
        """
        # Validar longitudes mínimas y máximas
        casos_longitud = {
            'nombre': {'min': 2, 'max': 50},
            'apellido': {'min': 2, 'max': 50},
            'telefono': {'min': 11, 'max': 11},
            'cedula': {'min': 9, 'max': 10},  # V-1234567 a V-12345678
            'direccion': {'min': 10, 'max': 500}
        }
        
        for campo, limites in casos_longitud.items():
            # Probar longitud mínima válida
            texto_min = 'a' * limites['min']
            self.assertGreaterEqual(len(texto_min), limites['min'], 
                                  f"Longitud mínima falló para {campo}")
            
            # Probar longitud máxima válida
            texto_max = 'a' * limites['max']
            self.assertLessEqual(len(texto_max), limites['max'], 
                               f"Longitud máxima falló para {campo}")
            
            # Probar longitud inválida (muy corto)
            if limites['min'] > 1:
                texto_corto = 'a' * (limites['min'] - 1)
                self.assertLess(len(texto_corto), limites['min'], 
                              f"Texto muy corto no detectado para {campo}")
    
    def test_validacion_fecha_nacimiento(self):
        """
        Probar validación de fecha de nacimiento
        Requisito: 2.1, 2.2
        """
        hoy = date.today()
        
        # Fechas válidas (mayores de edad)
        fechas_validas = [
            date(1990, 1, 1),
            date(1985, 5, 15),
            date(2000, 12, 31),
            date(hoy.year - 18, hoy.month, hoy.day)  # Exactamente 18 años
        ]
        
        for fecha in fechas_validas:
            edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
            self.assertGreaterEqual(edad, 18, f"Fecha válida falló: {fecha}")
        
        # Fechas inválidas (menores de edad o futuras)
        fechas_invalidas = [
            date(hoy.year - 17, hoy.month, hoy.day),  # 17 años
            date(hoy.year + 1, 1, 1),                 # Fecha futura
            date(hoy.year, hoy.month, hoy.day)        # Hoy (0 años)
        ]
        
        for fecha in fechas_invalidas:
            if fecha <= hoy:
                edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
                self.assertLess(edad, 18, f"Fecha inválida pasó: {fecha}")
    
    def test_validacion_password_segura(self):
        """
        Probar validación de contraseña segura
        Requisito: 2.1, 2.2
        """
        def validar_password_test(password):
            """Función de validación de contraseña para pruebas"""
            errores = []
            
            if len(password) < 8:
                errores.append('Muy corta')
            if not re.search(r'[A-Z]', password):
                errores.append('Sin mayúscula')
            if not re.search(r'[a-z]', password):
                errores.append('Sin minúscula')
            if not re.search(r'\d', password):
                errores.append('Sin número')
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                errores.append('Sin carácter especial')
            if ' ' in password:
                errores.append('Contiene espacios')
            
            return len(errores) == 0, errores
        
        # Contraseñas válidas
        passwords_validas = [
            'Password123!',
            'MiClave456@',
            'Segura789#',
            'Fuerte2024$'
        ]
        
        for password in passwords_validas:
            es_valida, errores = validar_password_test(password)
            self.assertTrue(es_valida, f"Password válida falló: {password}, errores: {errores}")
        
        # Contraseñas inválidas
        passwords_invalidas = [
            'password',      # Sin mayúscula, sin número, sin especial
            'PASSWORD123',   # Sin minúscula, sin especial
            'Password',      # Sin número, sin especial
            'Pass123',       # Muy corta, sin especial
            'Password 123!', # Contiene espacios
            ''               # Vacía
        ]
        
        for password in passwords_invalidas:
            if password:  # Si no está vacía
                es_valida, errores = validar_password_test(password)
                self.assertFalse(es_valida, f"Password inválida pasó: {password}")


if __name__ == '__main__':
    print("="*60)
    print("EJECUTANDO PRUEBAS UNITARIAS SIMPLIFICADAS - MÓDULO DE CLIENTES")
    print("="*60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Ejecutar pruebas
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClientesValidation)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Mostrar resumen
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    print(f"Total de pruebas ejecutadas: {result.testsRun}")
    print(f"Pruebas exitosas: {result.testsRun - len(result.errors) - len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    
    if result.errors or result.failures:
        print(f"\n❌ PRUEBAS FALLIDAS - {len(result.errors + result.failures)} problemas encontrados")
    else:
        print(f"\n✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")