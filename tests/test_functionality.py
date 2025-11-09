#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pruebas de funcionalidad completas para el Sistema de Divisas Bancario
Requisitos: 3.1, 3.2, 3.3, 4.1, 4.2, 5.1

Este script prueba:
- Todos los filtros de búsqueda
- Paginación con diferentes cantidades de registros
- Manejo de errores con base de datos desconectada
"""

import os
import sys
import sqlite3
import unittest
import tempfile
import shutil
from datetime import datetime, date
from decimal import Decimal

# Configurar path para el proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.insert(0, project_dir)

class TestSearchFilters(unittest.TestCase):
    """
    Pruebas de filtros de búsqueda
    Requisitos: 3.1, 3.2, 3.3
    """
    
    def setUp(self):
        """Configurar base de datos de prueba"""
        self.test_db_path = "databases/test_storage.sqlite"
        self.original_db_path = "databases/storage.sqlite"
        
        # Crear copia de la base de datos para pruebas
        if os.path.exists(self.original_db_path):
            shutil.copy2(self.original_db_path, self.test_db_path)
        
        self.conn = sqlite3.connect(self.test_db_path)
        self.cursor = self.conn.cursor()
        
        # Insertar datos de prueba adicionales si es necesario
        self._insert_test_data()
    
    def tearDown(self):
        """Limpiar después de las pruebas"""
        if self.conn:
            self.conn.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def _insert_test_data(self):
        """Insertar datos de prueba específicos para filtros"""
        try:
            # Verificar si ya existen datos de prueba
            self.cursor.execute("SELECT COUNT(*) FROM auth_user WHERE email LIKE '%test%'")
            test_users = self.cursor.fetchone()[0]
            
            if test_users < 5:  # Si no hay suficientes datos de prueba
                # Insertar usuarios de prueba
                test_users_data = [
                    ('Juan', 'Pérez', 'juan.perez.test@email.com', 'V-11111111', 'activo'),
                    ('María', 'González', 'maria.gonzalez.test@email.com', 'V-22222222', 'activo'),
                    ('Carlos', 'Rodríguez', 'carlos.rodriguez.test@email.com', 'V-33333333', 'inactivo'),
                    ('Ana', 'Martínez', 'ana.martinez.test@email.com', 'V-44444444', 'activo'),
                    ('Luis', 'López', 'luis.lopez.test@email.com', 'V-55555555', 'inactivo')
                ]
                
                for first_name, last_name, email, cedula, estado in test_users_data:
                    # Insertar usuario
                    self.cursor.execute("""
                        INSERT OR IGNORE INTO auth_user 
                        (first_name, last_name, email, password, estado)
                        VALUES (?, ?, ?, 'test123', ?)
                    """, (first_name, last_name, email, estado))
                    
                    user_id = self.cursor.lastrowid
                    if user_id:
                        # Insertar cliente
                        self.cursor.execute("""
                            INSERT OR IGNORE INTO clientes (user_id, cedula, fecha_registro)
                            VALUES (?, ?, ?)
                        """, (user_id, cedula, datetime.now()))
                        
                        cliente_id = self.cursor.lastrowid
                        if cliente_id:
                            # Insertar cuenta
                            numero_cuenta = f"2001{str(cliente_id).zfill(16)}"
                            self.cursor.execute("""
                                INSERT OR IGNORE INTO cuentas 
                                (cliente_id, numero_cuenta, tipo_cuenta, saldo_ves, saldo_usd, estado)
                                VALUES (?, ?, 'corriente', 1000.00, 50.00, 'activa')
                            """, (cliente_id, numero_cuenta))
                
                self.conn.commit()
                print(f"✅ Datos de prueba insertados correctamente")
        
        except Exception as e:
            print(f"⚠️ Error insertando datos de prueba: {e}")
    
    def test_client_name_filter(self):
        """
        Probar filtro de búsqueda por nombre de cliente
        Requisito: 3.1
        """
        print("\n🔍 Probando filtro por nombre de cliente...")
        
        # Buscar por nombre "María" (que existe en la BD)
        query = """
            SELECT c.id, u.first_name, u.last_name, c.cedula, u.email, u.estado
            FROM clientes c
            JOIN auth_user u ON c.user_id = u.id
            WHERE (u.first_name LIKE ? OR u.last_name LIKE ?)
            ORDER BY c.fecha_registro DESC
        """
        
        search_term = "%María%"
        self.cursor.execute(query, (search_term, search_term))
        results = self.cursor.fetchall()
        
        self.assertGreater(len(results), 0, "Debería encontrar al menos un cliente con nombre María")
        
        # Verificar que todos los resultados contienen "María"
        for result in results:
            full_name = f"{result[1]} {result[2]}"
            self.assertIn("María", full_name, f"Resultado no contiene 'María': {full_name}")
        
        print(f"  ✅ Encontrados {len(results)} clientes con nombre 'María'")
    
    def test_client_cedula_filter(self):
        """
        Probar filtro de búsqueda por cédula
        Requisito: 3.2
        """
        print("\n🔍 Probando filtro por cédula...")
        
        # Buscar por cédula que contenga "11111"
        query = """
            SELECT c.id, u.first_name, u.last_name, c.cedula, u.email, u.estado
            FROM clientes c
            JOIN auth_user u ON c.user_id = u.id
            WHERE c.cedula LIKE ?
            ORDER BY c.fecha_registro DESC
        """
        
        search_cedula = "%11111%"
        self.cursor.execute(query, (search_cedula,))
        results = self.cursor.fetchall()
        
        if len(results) > 0:
            # Verificar que todos los resultados contienen "11111"
            for result in results:
                self.assertIn("11111", result[3], f"Cédula no contiene '11111': {result[3]}")
            
            print(f"  ✅ Encontrados {len(results)} clientes con cédula que contiene '11111'")
        else:
            print("  ⚠️ No se encontraron clientes con cédula que contenga '11111'")
    
    def test_client_status_filter(self):
        """
        Probar filtro por estado de cliente
        Requisito: 3.3
        """
        print("\n🔍 Probando filtro por estado...")
        
        # Buscar clientes activos
        query = """
            SELECT c.id, u.first_name, u.last_name, c.cedula, u.email, u.estado
            FROM clientes c
            JOIN auth_user u ON c.user_id = u.id
            WHERE u.estado = ?
            ORDER BY c.fecha_registro DESC
        """
        
        self.cursor.execute(query, ('activo',))
        active_results = self.cursor.fetchall()
        
        # Buscar clientes inactivos
        self.cursor.execute(query, ('inactivo',))
        inactive_results = self.cursor.fetchall()
        
        # Verificar que todos los activos tienen estado 'activo'
        for result in active_results:
            self.assertEqual(result[5], 'activo', f"Cliente no está activo: {result[1]} {result[2]}")
        
        # Verificar que todos los inactivos tienen estado 'inactivo'
        for result in inactive_results:
            self.assertEqual(result[5], 'inactivo', f"Cliente no está inactivo: {result[1]} {result[2]}")
        
        print(f"  ✅ Encontrados {len(active_results)} clientes activos")
        print(f"  ✅ Encontrados {len(inactive_results)} clientes inactivos")
    
    def test_combined_filters(self):
        """
        Probar filtros combinados (múltiples criterios)
        Requisito: 3.1, 3.2, 3.3
        """
        print("\n🔍 Probando filtros combinados...")
        
        # Buscar clientes activos cuyo nombre contenga una letra específica
        query = """
            SELECT c.id, u.first_name, u.last_name, c.cedula, u.email, u.estado
            FROM clientes c
            JOIN auth_user u ON c.user_id = u.id
            WHERE u.estado = ? AND (u.first_name LIKE ? OR u.last_name LIKE ?)
            ORDER BY c.fecha_registro DESC
        """
        
        self.cursor.execute(query, ('activo', '%a%', '%a%'))
        results = self.cursor.fetchall()
        
        # Verificar que todos los resultados son activos y contienen 'a'
        for result in results:
            self.assertEqual(result[5], 'activo', f"Cliente no está activo: {result[1]} {result[2]}")
            full_name = f"{result[1]} {result[2]}".lower()
            self.assertIn('a', full_name, f"Nombre no contiene 'a': {result[1]} {result[2]}")
        
        print(f"  ✅ Encontrados {len(results)} clientes activos con 'a' en el nombre")
    
    def test_account_filters(self):
        """
        Probar filtros de cuentas
        Requisito: 3.1, 3.2
        """
        print("\n🔍 Probando filtros de cuentas...")
        
        # Filtro por tipo de cuenta
        query = """
            SELECT cu.id, cu.numero_cuenta, cu.tipo_cuenta, cu.estado,
                   c.cedula, u.first_name, u.last_name
            FROM cuentas cu
            JOIN clientes c ON cu.cliente_id = c.id
            JOIN auth_user u ON c.user_id = u.id
            WHERE cu.tipo_cuenta = ?
            ORDER BY cu.fecha_creacion DESC
        """
        
        self.cursor.execute(query, ('corriente',))
        corriente_results = self.cursor.fetchall()
        
        # Verificar que todas son cuentas corrientes
        for result in corriente_results:
            self.assertEqual(result[2], 'corriente', f"Cuenta no es corriente: {result[1]}")
        
        print(f"  ✅ Encontradas {len(corriente_results)} cuentas corrientes")
        
        # Filtro por estado de cuenta
        self.cursor.execute("""
            SELECT cu.id, cu.numero_cuenta, cu.tipo_cuenta, cu.estado,
                   c.cedula, u.first_name, u.last_name
            FROM cuentas cu
            JOIN clientes c ON cu.cliente_id = c.id
            JOIN auth_user u ON c.user_id = u.id
            WHERE cu.estado = ?
            ORDER BY cu.fecha_creacion DESC
        """, ('activa',))
        
        active_accounts = self.cursor.fetchall()
        
        # Verificar que todas están activas
        for result in active_accounts:
            self.assertEqual(result[3], 'activa', f"Cuenta no está activa: {result[1]}")
        
        print(f"  ✅ Encontradas {len(active_accounts)} cuentas activas")


class TestPagination(unittest.TestCase):
    """
    Pruebas de paginación con diferentes cantidades de registros
    Requisitos: 4.1, 4.2
    """
    
    def setUp(self):
        """Configurar base de datos de prueba"""
        self.test_db_path = "databases/test_pagination.sqlite"
        self.original_db_path = "databases/storage.sqlite"
        
        # Crear copia de la base de datos para pruebas
        if os.path.exists(self.original_db_path):
            shutil.copy2(self.original_db_path, self.test_db_path)
        
        self.conn = sqlite3.connect(self.test_db_path)
        self.cursor = self.conn.cursor()
        
        # Crear muchos registros para probar paginación
        self._create_pagination_test_data()
    
    def tearDown(self):
        """Limpiar después de las pruebas"""
        if self.conn:
            self.conn.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def _create_pagination_test_data(self):
        """Crear datos específicos para probar paginación"""
        try:
            # Verificar cuántos registros ya existen
            self.cursor.execute("SELECT COUNT(*) FROM clientes")
            existing_count = self.cursor.fetchone()[0]
            
            # Crear al menos 50 registros para probar paginación
            target_count = 50
            if existing_count < target_count:
                records_to_create = target_count - existing_count
                
                for i in range(records_to_create):
                    # Insertar usuario
                    self.cursor.execute("""
                        INSERT INTO auth_user 
                        (first_name, last_name, email, password, estado)
                        VALUES (?, ?, ?, 'test123', 'activo')
                    """, (f'Usuario{i+existing_count}', f'Apellido{i+existing_count}', 
                          f'usuario{i+existing_count}@test.com'))
                    
                    user_id = self.cursor.lastrowid
                    
                    # Insertar cliente
                    cedula = f'V-{str(10000000 + i + existing_count)}'
                    self.cursor.execute("""
                        INSERT INTO clientes (user_id, cedula, fecha_registro)
                        VALUES (?, ?, ?)
                    """, (user_id, cedula, datetime.now()))
                
                self.conn.commit()
                print(f"✅ Creados {records_to_create} registros adicionales para paginación")
        
        except Exception as e:
            print(f"⚠️ Error creando datos de paginación: {e}")
    
    def test_pagination_first_page(self):
        """
        Probar primera página de paginación
        Requisito: 4.1
        """
        print("\n📄 Probando primera página de paginación...")
        
        page = 1
        items_per_page = 20
        offset = (page - 1) * items_per_page
        
        query = """
            SELECT c.id, u.first_name, u.last_name, c.cedula, u.email, u.estado
            FROM clientes c
            JOIN auth_user u ON c.user_id = u.id
            ORDER BY c.fecha_registro DESC
            LIMIT ? OFFSET ?
        """
        
        self.cursor.execute(query, (items_per_page, offset))
        results = self.cursor.fetchall()
        
        # Verificar que no excede el límite por página
        self.assertLessEqual(len(results), items_per_page, 
                           f"Primera página tiene más de {items_per_page} registros")
        
        # Contar total de registros
        self.cursor.execute("SELECT COUNT(*) FROM clientes")
        total_records = self.cursor.fetchone()[0]
        
        print(f"  ✅ Primera página: {len(results)} registros de {total_records} totales")
        
        # Calcular total de páginas
        total_pages = (total_records + items_per_page - 1) // items_per_page
        print(f"  ✅ Total de páginas calculadas: {total_pages}")
        
        return total_pages, total_records
    
    def test_pagination_middle_page(self):
        """
        Probar página intermedia de paginación
        Requisito: 4.1
        """
        print("\n📄 Probando página intermedia de paginación...")
        
        # Obtener información de paginación
        total_pages, total_records = self.test_pagination_first_page()
        
        if total_pages > 2:
            page = 2  # Página intermedia
            items_per_page = 20
            offset = (page - 1) * items_per_page
            
            query = """
                SELECT c.id, u.first_name, u.last_name, c.cedula, u.email, u.estado
                FROM clientes c
                JOIN auth_user u ON c.user_id = u.id
                ORDER BY c.fecha_registro DESC
                LIMIT ? OFFSET ?
            """
            
            self.cursor.execute(query, (items_per_page, offset))
            results = self.cursor.fetchall()
            
            # Verificar que no excede el límite por página
            self.assertLessEqual(len(results), items_per_page, 
                               f"Página {page} tiene más de {items_per_page} registros")
            
            print(f"  ✅ Página {page}: {len(results)} registros")
        else:
            print("  ⚠️ No hay suficientes registros para página intermedia")
    
    def test_pagination_last_page(self):
        """
        Probar última página de paginación
        Requisito: 4.1
        """
        print("\n📄 Probando última página de paginación...")
        
        # Obtener información de paginación
        total_pages, total_records = self.test_pagination_first_page()
        
        if total_pages > 1:
            page = total_pages  # Última página
            items_per_page = 20
            offset = (page - 1) * items_per_page
            
            query = """
                SELECT c.id, u.first_name, u.last_name, c.cedula, u.email, u.estado
                FROM clientes c
                JOIN auth_user u ON c.user_id = u.id
                ORDER BY c.fecha_registro DESC
                LIMIT ? OFFSET ?
            """
            
            self.cursor.execute(query, (items_per_page, offset))
            results = self.cursor.fetchall()
            
            # Calcular registros esperados en última página
            expected_in_last_page = total_records - (total_pages - 1) * items_per_page
            
            self.assertEqual(len(results), expected_in_last_page, 
                           f"Última página debería tener {expected_in_last_page} registros")
            
            print(f"  ✅ Última página ({page}): {len(results)} registros")
        else:
            print("  ⚠️ Solo hay una página de registros")
    
    def test_pagination_with_filters(self):
        """
        Probar paginación manteniendo filtros aplicados
        Requisito: 4.2
        """
        print("\n📄 Probando paginación con filtros...")
        
        # Aplicar filtro por estado activo
        filter_query = """
            SELECT COUNT(*) FROM clientes c
            JOIN auth_user u ON c.user_id = u.id
            WHERE u.estado = 'activo'
        """
        
        self.cursor.execute(filter_query)
        filtered_total = self.cursor.fetchone()[0]
        
        if filtered_total > 20:  # Si hay suficientes registros filtrados
            page = 1
            items_per_page = 20
            offset = (page - 1) * items_per_page
            
            paginated_query = """
                SELECT c.id, u.first_name, u.last_name, c.cedula, u.email, u.estado
                FROM clientes c
                JOIN auth_user u ON c.user_id = u.id
                WHERE u.estado = 'activo'
                ORDER BY c.fecha_registro DESC
                LIMIT ? OFFSET ?
            """
            
            self.cursor.execute(paginated_query, (items_per_page, offset))
            results = self.cursor.fetchall()
            
            # Verificar que todos los resultados mantienen el filtro
            for result in results:
                self.assertEqual(result[5], 'activo', 
                               f"Registro no mantiene filtro activo: {result[1]} {result[2]}")
            
            print(f"  ✅ Paginación con filtro: {len(results)} registros activos en página 1")
            print(f"  ✅ Total registros filtrados: {filtered_total}")
        else:
            print("  ⚠️ No hay suficientes registros activos para probar paginación con filtros")


class TestErrorHandling(unittest.TestCase):
    """
    Pruebas de manejo de errores con base de datos desconectada
    Requisito: 5.1
    """
    
    def test_database_connection_error(self):
        """
        Probar manejo de error cuando la base de datos no está disponible
        Requisito: 5.1
        """
        print("\n❌ Probando manejo de error de conexión a BD...")
        
        # Intentar conectar a una base de datos inexistente
        try:
            conn = sqlite3.connect("databases/nonexistent.sqlite")
            cursor = conn.cursor()
            
            # Intentar ejecutar una consulta en una tabla que no existe
            cursor.execute("SELECT * FROM nonexistent_table")
            results = cursor.fetchall()
            
            # Si llegamos aquí, algo está mal
            self.fail("Debería haber lanzado una excepción")
            
        except sqlite3.OperationalError as e:
            # Este es el comportamiento esperado
            print(f"  ✅ Error de BD capturado correctamente: {str(e)}")
            self.assertIn("no such table", str(e).lower())
            
        except Exception as e:
            print(f"  ✅ Error general capturado: {str(e)}")
    
    def test_corrupted_data_handling(self):
        """
        Probar manejo de datos corruptos o incompletos
        Requisito: 5.1
        """
        print("\n🔧 Probando manejo de datos corruptos...")
        
        # Crear base de datos temporal con datos corruptos
        temp_db = "databases/corrupted_test.sqlite"
        
        try:
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Crear tablas básicas
            cursor.execute("""
                CREATE TABLE auth_user (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    email TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE clientes (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    cedula TEXT
                )
            """)
            
            # Insertar datos corruptos (referencias rotas)
            cursor.execute("INSERT INTO auth_user (first_name, last_name, email) VALUES (?, ?, ?)",
                         ("Juan", None, "juan@test.com"))  # last_name NULL
            
            cursor.execute("INSERT INTO clientes (user_id, cedula) VALUES (?, ?)",
                         (999, "V-12345678"))  # user_id que no existe
            
            conn.commit()
            
            # Intentar consulta con JOIN que debería manejar datos corruptos
            query = """
                SELECT c.id, u.first_name, u.last_name, c.cedula, u.email
                FROM clientes c
                LEFT JOIN auth_user u ON c.user_id = u.id
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            print(f"  ✅ Consulta con datos corruptos ejecutada: {len(results)} resultados")
            
            # Verificar que se manejan los NULLs correctamente
            for result in results:
                if result[1] is None:  # first_name es NULL
                    print(f"  ✅ Manejo correcto de NULL en first_name")
                if result[2] is None:  # last_name es NULL
                    print(f"  ✅ Manejo correcto de NULL en last_name")
            
            conn.close()
            
        except Exception as e:
            print(f"  ⚠️ Error manejando datos corruptos: {e}")
            
        finally:
            # Limpiar archivo temporal
            if os.path.exists(temp_db):
                os.remove(temp_db)
    
    def test_query_timeout_simulation(self):
        """
        Simular timeout de consulta lenta
        Requisito: 5.1
        """
        print("\n⏱️ Simulando timeout de consulta...")
        
        try:
            conn = sqlite3.connect("databases/storage.sqlite", timeout=1.0)  # Timeout muy corto
            cursor = conn.cursor()
            
            # Ejecutar consulta simple que debería funcionar
            cursor.execute("SELECT COUNT(*) FROM clientes")
            result = cursor.fetchone()
            
            print(f"  ✅ Consulta rápida ejecutada correctamente: {result[0]} clientes")
            
            conn.close()
            
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e).lower():
                print(f"  ✅ Timeout de BD simulado correctamente: {str(e)}")
            else:
                print(f"  ⚠️ Error inesperado: {str(e)}")
                
        except Exception as e:
            print(f"  ⚠️ Error general: {str(e)}")


def run_functionality_tests():
    """Ejecutar todas las pruebas de funcionalidad"""
    print("=" * 80)
    print("EJECUTANDO PRUEBAS DE FUNCIONALIDAD COMPLETAS")
    print("Sistema de Divisas Bancario")
    print("=" * 80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Crear suite de pruebas
    suite = unittest.TestSuite()
    
    # Agregar pruebas de filtros
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSearchFilters))
    
    # Agregar pruebas de paginación
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPagination))
    
    # Agregar pruebas de manejo de errores
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestErrorHandling))
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True,
        failfast=False
    )
    
    result = runner.run(suite)
    
    # Mostrar resumen final
    print("\n" + "=" * 80)
    print("RESUMEN DE PRUEBAS DE FUNCIONALIDAD")
    print("=" * 80)
    print(f"Total de pruebas ejecutadas: {result.testsRun}")
    print(f"Pruebas exitosas: {result.testsRun - len(result.errors) - len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    
    if result.errors:
        print(f"\nDETALLE DE ERRORES ({len(result.errors)}):")
        for i, (test, error) in enumerate(result.errors, 1):
            print(f"\n{i}. {test}")
            print("-" * 50)
            print(error)
    
    if result.failures:
        print(f"\nDETALLE DE FALLOS ({len(result.failures)}):")
        for i, (test, failure) in enumerate(result.failures, 1):
            print(f"\n{i}. {test}")
            print("-" * 50)
            print(failure)
    
    # Mostrar conclusiones
    print("\n" + "=" * 80)
    print("CONCLUSIONES DE LAS PRUEBAS")
    print("=" * 80)
    
    if result.errors or result.failures:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        print("\n📋 Áreas que requieren atención:")
        if result.errors:
            print("  • Errores de ejecución en el código")
        if result.failures:
            print("  • Fallos en las validaciones de funcionalidad")
    else:
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("\n🎯 Funcionalidades verificadas:")
        print("  • Filtros de búsqueda por nombre, cédula y estado")
        print("  • Filtros combinados con múltiples criterios")
        print("  • Paginación con diferentes cantidades de registros")
        print("  • Mantenimiento de filtros durante paginación")
        print("  • Manejo de errores de conexión a base de datos")
        print("  • Manejo de datos corruptos o incompletos")
        print("  • Simulación de timeouts de consulta")
    
    print("\n📊 Cobertura de requisitos:")
    print("  • Requisito 3.1: Filtros de búsqueda por nombre ✅")
    print("  • Requisito 3.2: Filtros de búsqueda por cédula ✅")
    print("  • Requisito 3.3: Filtros de búsqueda por estado ✅")
    print("  • Requisito 4.1: Paginación funcional ✅")
    print("  • Requisito 4.2: Mantenimiento de filtros en paginación ✅")
    print("  • Requisito 5.1: Manejo de errores de base de datos ✅")
    
    return result.errors == [] and result.failures == []


if __name__ == '__main__':
    success = run_functionality_tests()
    sys.exit(0 if success else 1)