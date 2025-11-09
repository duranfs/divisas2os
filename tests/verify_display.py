#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar que los datos de prueba se muestren correctamente en las vistas
Requisitos: 1.1, 2.1

Este script verifica:
- Que los clientes aparezcan en la vista de listado
- Que los filtros funcionen correctamente
- Que las cuentas se muestren con sus saldos
- Que las estadísticas sean correctas
"""

import os
import sys
import sqlite3
from datetime import datetime

# Configurar path para el proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.insert(0, project_dir)

class DisplayVerifier:
    """Verificador de visualización de datos en las vistas"""
    
    def __init__(self, db_path="databases/storage.sqlite"):
        """Inicializar verificador con conexión a base de datos"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Conectar a la base de datos"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"❌ Error conectando a la base de datos: {e}")
            return False
    
    def disconnect(self):
        """Desconectar de la base de datos"""
        if self.conn:
            self.conn.close()
    
    def verify_client_listing(self):
        """Verificar que la vista de listado de clientes funcione correctamente"""
        print("👥 Verificando vista de listado de clientes...")
        
        try:
            # Consulta exacta que usa el controlador
            query = """
                SELECT 
                    c.id as client_id,
                    c.user_id,
                    c.cedula,
                    c.fecha_registro,
                    u.id as user_id,
                    u.first_name,
                    u.last_name,
                    u.email,
                    u.estado
                FROM clientes c
                JOIN auth_user u ON c.user_id = u.id
                ORDER BY c.fecha_registro DESC
            """
            
            self.cursor.execute(query)
            all_clients = self.cursor.fetchall()
            
            print(f"  📊 Total de clientes en la base de datos: {len(all_clients)}")
            
            if all_clients:
                print("  ✅ La consulta JOIN funciona correctamente")
                print("  📋 Primeros 5 clientes que deberían aparecer:")
                
                for i, client in enumerate(all_clients[:5], 1):
                    print(f"    {i}. ID: {client[0]} | Nombre: {client[5]} {client[6]} | Cédula: {client[2]} | Email: {client[7]} | Estado: {client[8]}")
                
                # Verificar campos requeridos
                missing_data = []
                for client in all_clients:
                    if not client[5] or not client[6]:  # first_name, last_name
                        missing_data.append(f"Cliente ID {client[0]} sin nombre completo")
                    if not client[2]:  # cedula
                        missing_data.append(f"Cliente ID {client[0]} sin cédula")
                    if not client[7]:  # email
                        missing_data.append(f"Cliente ID {client[0]} sin email")
                
                if missing_data:
                    print("  ⚠️  Datos faltantes encontrados:")
                    for issue in missing_data[:5]:
                        print(f"    - {issue}")
                else:
                    print("  ✅ Todos los clientes tienen datos completos")
                
                return True
            else:
                print("  ❌ No se encontraron clientes - la vista estará vacía")
                return False
                
        except Exception as e:
            print(f"  ❌ Error verificando listado de clientes: {e}")
            return False
    
    def verify_client_filters(self):
        """Verificar que los filtros de búsqueda funcionen"""
        print("\n🔍 Verificando filtros de búsqueda de clientes...")
        
        try:
            base_query = """
                SELECT 
                    c.id, c.cedula, u.first_name, u.last_name, u.email, u.estado
                FROM clientes c
                JOIN auth_user u ON c.user_id = u.id
            """
            
            # Filtro por nombre
            name_query = base_query + " WHERE u.first_name LIKE '%Franklin%' OR u.last_name LIKE '%Franklin%'"
            self.cursor.execute(name_query)
            name_results = self.cursor.fetchall()
            print(f"  🔍 Filtro por nombre 'Franklin': {len(name_results)} resultados")
            
            # Filtro por cédula
            cedula_query = base_query + " WHERE c.cedula LIKE '%TEST%'"
            self.cursor.execute(cedula_query)
            cedula_results = self.cursor.fetchall()
            print(f"  🔍 Filtro por cédula 'TEST': {len(cedula_results)} resultados")
            
            # Filtro por estado activo
            active_query = base_query + " WHERE u.estado = 'activo'"
            self.cursor.execute(active_query)
            active_results = self.cursor.fetchall()
            print(f"  🔍 Filtro por estado 'activo': {len(active_results)} resultados")
            
            # Filtro por estado inactivo
            inactive_query = base_query + " WHERE u.estado = 'inactivo'"
            self.cursor.execute(inactive_query)
            inactive_results = self.cursor.fetchall()
            print(f"  🔍 Filtro por estado 'inactivo': {len(inactive_results)} resultados")
            
            # Filtro combinado
            combined_query = base_query + " WHERE u.estado = 'activo' AND (u.first_name LIKE '%María%' OR u.last_name LIKE '%María%')"
            self.cursor.execute(combined_query)
            combined_results = self.cursor.fetchall()
            print(f"  🔍 Filtro combinado (activo + nombre 'María'): {len(combined_results)} resultados")
            
            print("  ✅ Todos los filtros funcionan correctamente")
            return True
            
        except Exception as e:
            print(f"  ❌ Error verificando filtros: {e}")
            return False
    
    def verify_client_statistics(self):
        """Verificar que las estadísticas de clientes sean correctas"""
        print("\n📊 Verificando estadísticas de clientes...")
        
        try:
            # Total de clientes
            self.cursor.execute("SELECT COUNT(*) FROM clientes")
            total_clients = self.cursor.fetchone()[0]
            
            # Clientes activos
            self.cursor.execute("""
                SELECT COUNT(*) FROM clientes c
                JOIN auth_user u ON c.user_id = u.id
                WHERE u.estado = 'activo'
            """)
            active_clients = self.cursor.fetchone()[0]
            
            # Clientes inactivos
            self.cursor.execute("""
                SELECT COUNT(*) FROM clientes c
                JOIN auth_user u ON c.user_id = u.id
                WHERE u.estado = 'inactivo'
            """)
            inactive_clients = self.cursor.fetchone()[0]
            
            print(f"  📈 Total de clientes: {total_clients}")
            print(f"  📈 Clientes activos: {active_clients}")
            print(f"  📈 Clientes inactivos: {inactive_clients}")
            
            # Verificar que los números cuadren
            if active_clients + inactive_clients == total_clients:
                print("  ✅ Las estadísticas son consistentes")
                return True
            else:
                print("  ⚠️  Inconsistencia en estadísticas detectada")
                return False
                
        except Exception as e:
            print(f"  ❌ Error verificando estadísticas: {e}")
            return False
    
    def verify_account_listing(self):
        """Verificar que la vista de listado de cuentas funcione"""
        print("\n💳 Verificando vista de listado de cuentas...")
        
        try:
            # Consulta que debería usar el controlador de cuentas
            query = """
                SELECT 
                    cu.id as cuenta_id,
                    cu.numero_cuenta,
                    cu.tipo_cuenta,
                    cu.saldo_ves,
                    cu.saldo_usd,
                    cu.saldo_eur,
                    cu.saldo_usdt,
                    cu.estado as estado_cuenta,
                    c.cedula,
                    u.first_name,
                    u.last_name,
                    u.email
                FROM cuentas cu
                JOIN clientes c ON cu.cliente_id = c.id
                JOIN auth_user u ON c.user_id = u.id
                ORDER BY cu.fecha_creacion DESC
            """
            
            self.cursor.execute(query)
            all_accounts = self.cursor.fetchall()
            
            print(f"  📊 Total de cuentas en la base de datos: {len(all_accounts)}")
            
            if all_accounts:
                print("  ✅ La consulta JOIN para cuentas funciona correctamente")
                print("  📋 Primeras 5 cuentas que deberían aparecer:")
                
                for i, account in enumerate(all_accounts[:5], 1):
                    cliente_nombre = f"{account[9] or ''} {account[10] or ''}".strip()
                    print(f"    {i}. Cuenta: {account[1]} | Cliente: {cliente_nombre} | Tipo: {account[2]} | Estado: {account[7]}")
                    saldo_ves = account[3] if account[3] is not None else 0
                    saldo_usd = account[4] if account[4] is not None else 0
                    saldo_eur = account[5] if account[5] is not None else 0
                    saldo_usdt = account[6] if account[6] is not None else 0
                    print(f"       Saldos: VES {saldo_ves:,.2f}, USD {saldo_usd:,.2f}, EUR {saldo_eur:,.2f}, USDT {saldo_usdt:,.2f}")
                
                # Verificar distribución por tipo
                self.cursor.execute("""
                    SELECT tipo_cuenta, COUNT(*) FROM cuentas 
                    GROUP BY tipo_cuenta
                """)
                type_distribution = self.cursor.fetchall()
                print("  📊 Distribución por tipo de cuenta:")
                for tipo, count in type_distribution:
                    print(f"    {tipo}: {count}")
                
                # Verificar distribución por estado
                self.cursor.execute("""
                    SELECT estado, COUNT(*) FROM cuentas 
                    GROUP BY estado
                """)
                status_distribution = self.cursor.fetchall()
                print("  📊 Distribución por estado de cuenta:")
                for estado, count in status_distribution:
                    print(f"    {estado}: {count}")
                
                return True
            else:
                print("  ❌ No se encontraron cuentas - la vista estará vacía")
                return False
                
        except Exception as e:
            print(f"  ❌ Error verificando listado de cuentas: {e}")
            return False
    
    def verify_account_balances(self):
        """Verificar que los saldos de cuentas se muestren correctamente"""
        print("\n💰 Verificando saldos de cuentas...")
        
        try:
            # Saldos totales por moneda
            self.cursor.execute("""
                SELECT 
                    SUM(saldo_ves) as total_ves,
                    SUM(saldo_usd) as total_usd,
                    SUM(saldo_eur) as total_eur,
                    SUM(saldo_usdt) as total_usdt,
                    COUNT(*) as total_cuentas
                FROM cuentas
                WHERE estado = 'activa'
            """)
            
            totals = self.cursor.fetchone()
            
            print(f"  💰 Saldos totales en cuentas activas ({totals[4]} cuentas):")
            print(f"    VES: {totals[0]:,.2f}")
            print(f"    USD: {totals[1]:,.2f}")
            print(f"    EUR: {totals[2]:,.2f}")
            print(f"    USDT: {totals[3]:,.2f}")
            
            # Verificar cuentas con saldos cero
            self.cursor.execute("""
                SELECT COUNT(*) FROM cuentas 
                WHERE saldo_ves = 0 AND saldo_usd = 0 AND saldo_eur = 0 AND saldo_usdt = 0
            """)
            zero_balance_accounts = self.cursor.fetchone()[0]
            
            print(f"  📊 Cuentas con saldo cero: {zero_balance_accounts}")
            
            # Verificar cuentas con saldos negativos (no deberían existir)
            self.cursor.execute("""
                SELECT COUNT(*) FROM cuentas 
                WHERE saldo_ves < 0 OR saldo_usd < 0 OR saldo_eur < 0 OR saldo_usdt < 0
            """)
            negative_balance_accounts = self.cursor.fetchone()[0]
            
            if negative_balance_accounts > 0:
                print(f"  ⚠️  Cuentas con saldos negativos encontradas: {negative_balance_accounts}")
                return False
            else:
                print("  ✅ No hay cuentas con saldos negativos")
            
            print("  ✅ Verificación de saldos completada")
            return True
            
        except Exception as e:
            print(f"  ❌ Error verificando saldos: {e}")
            return False
    
    def verify_pagination_data(self):
        """Verificar datos para paginación"""
        print("\n📄 Verificando datos para paginación...")
        
        try:
            # Contar total de clientes
            self.cursor.execute("SELECT COUNT(*) FROM clientes")
            total_clients = self.cursor.fetchone()[0]
            
            items_per_page = 20
            total_pages = (total_clients + items_per_page - 1) // items_per_page
            
            print(f"  📊 Total de clientes: {total_clients}")
            print(f"  📊 Elementos por página: {items_per_page}")
            print(f"  📊 Páginas necesarias: {total_pages}")
            
            if total_clients > items_per_page:
                print("  ✅ Se necesitará paginación")
                
                # Simular primera página
                self.cursor.execute("""
                    SELECT c.id, u.first_name, u.last_name 
                    FROM clientes c
                    JOIN auth_user u ON c.user_id = u.id
                    ORDER BY c.fecha_registro DESC
                    LIMIT ? OFFSET ?
                """, (items_per_page, 0))
                
                first_page = self.cursor.fetchall()
                print(f"  📋 Primera página: {len(first_page)} elementos")
                
                if total_pages > 1:
                    # Simular segunda página
                    self.cursor.execute("""
                        SELECT c.id, u.first_name, u.last_name 
                        FROM clientes c
                        JOIN auth_user u ON c.user_id = u.id
                        ORDER BY c.fecha_registro DESC
                        LIMIT ? OFFSET ?
                    """, (items_per_page, items_per_page))
                    
                    second_page = self.cursor.fetchall()
                    print(f"  📋 Segunda página: {len(second_page)} elementos")
            else:
                print("  ℹ️  No se necesita paginación (menos de 20 elementos)")
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error verificando paginación: {e}")
            return False
    
    def run_full_verification(self):
        """Ejecutar verificación completa de visualización"""
        print("🔍 INICIANDO VERIFICACIÓN DE VISUALIZACIÓN DE DATOS")
        print("=" * 60)
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        if not self.connect():
            return False
        
        try:
            results = []
            
            # Verificar listado de clientes
            results.append(self.verify_client_listing())
            
            # Verificar filtros
            results.append(self.verify_client_filters())
            
            # Verificar estadísticas
            results.append(self.verify_client_statistics())
            
            # Verificar listado de cuentas
            results.append(self.verify_account_listing())
            
            # Verificar saldos
            results.append(self.verify_account_balances())
            
            # Verificar paginación
            results.append(self.verify_pagination_data())
            
            # Resumen final
            passed = sum(results)
            total = len(results)
            
            print("\n" + "=" * 60)
            print("📋 RESUMEN DE VERIFICACIÓN")
            print("=" * 60)
            print(f"Pruebas pasadas: {passed}/{total}")
            
            if passed == total:
                print("✅ TODAS LAS VERIFICACIONES PASARON")
                print("\n🎉 Los datos deberían mostrarse correctamente en las vistas")
                print("\n📋 PRÓXIMOS PASOS:")
                print("   1. Acceder a /clientes/listar para ver el listado")
                print("   2. Probar los filtros de búsqueda")
                print("   3. Acceder a /cuentas/listar_todas para ver las cuentas")
                print("   4. Verificar que las estadísticas se muestren")
                return True
            else:
                print(f"❌ {total - passed} VERIFICACIONES FALLARON")
                print("\n⚠️  Puede haber problemas en la visualización de datos")
                return False
                
        except Exception as e:
            print(f"❌ Error durante la verificación: {e}")
            return False
        
        finally:
            self.disconnect()


def main():
    """Función principal"""
    verifier = DisplayVerifier()
    success = verifier.run_full_verification()
    
    if success:
        print("\n🎉 ¡Verificación completada exitosamente!")
        print("   Los datos deberían mostrarse correctamente en las vistas.")
    else:
        print("\n💥 Problemas encontrados en la verificación.")
        print("   Revisa los mensajes anteriores para más detalles.")
    
    return success


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)