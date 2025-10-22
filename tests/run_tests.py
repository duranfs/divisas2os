#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para ejecutar pruebas unitarias del Sistema de Divisas Bancario
"""

import os
import sys
import unittest
from datetime import datetime

# Configurar path para importar módulos de web2py
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.insert(0, project_dir)

def setup_web2py_environment():
    """Configurar entorno simulado de web2py para pruebas"""
    # Crear objetos globales simulados
    class MockRequest:
        def __init__(self):
            self.now = datetime.now()
            self.vars = {}
            self.args = []
    
    class MockResponse:
        def __init__(self):
            self.flash = None
    
    class MockSession:
        def __init__(self):
            self.flash = None
    
    # Simular objetos globales de web2py
    import gluon.globals
    gluon.globals.current.request = MockRequest()
    gluon.globals.current.response = MockResponse()
    gluon.globals.current.session = MockSession()

def run_client_tests():
    """Ejecutar pruebas del módulo de clientes"""
    print("="*60)
    print("EJECUTANDO PRUEBAS UNITARIAS - MÓDULO DE CLIENTES")
    print("="*60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Configurar entorno
    setup_web2py_environment()
    
    # Importar y ejecutar pruebas
    try:
        from test_clientes import TestClientesModule
        
        # Crear suite de pruebas
        suite = unittest.TestLoader().loadTestsFromTestCase(TestClientesModule)
        
        # Ejecutar pruebas con output detallado
        runner = unittest.TextTestRunner(
            verbosity=2,
            stream=sys.stdout,
            descriptions=True,
            failfast=False
        )
        
        result = runner.run(suite)
        
        # Mostrar resumen final
        print("\n" + "="*60)
        print("RESUMEN DE PRUEBAS")
        print("="*60)
        print(f"Total de pruebas ejecutadas: {result.testsRun}")
        print(f"Pruebas exitosas: {result.testsRun - len(result.errors) - len(result.failures)}")
        print(f"Errores: {len(result.errors)}")
        print(f"Fallos: {len(result.failures)}")
        
        if result.errors:
            print(f"\nDETALLE DE ERRORES ({len(result.errors)}):")
            for i, (test, error) in enumerate(result.errors, 1):
                print(f"\n{i}. {test}")
                print("-" * 40)
                print(error)
        
        if result.failures:
            print(f"\nDETALLE DE FALLOS ({len(result.failures)}):")
            for i, (test, failure) in enumerate(result.failures, 1):
                print(f"\n{i}. {test}")
                print("-" * 40)
                print(failure)
        
        # Determinar resultado final
        if result.errors or result.failures:
            print(f"\n❌ PRUEBAS FALLIDAS - {len(result.errors + result.failures)} problemas encontrados")
            return False
        else:
            print(f"\n✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
            return True
            
    except ImportError as e:
        print(f"❌ Error al importar módulos de prueba: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado durante las pruebas: {e}")
        return False

if __name__ == '__main__':
    success = run_client_tests()
    sys.exit(0 if success else 1)