#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para crear datos de prueba para el Sistema de Divisas Bancario
Requisitos: 1.1, 2.1

Este script genera:
- Clientes de prueba con diferentes estados (activo/inactivo)
- Cuentas de prueba con diferentes tipos (corriente/ahorro) y saldos
- Verifica que los datos se muestren correctamente en las vistas
"""

import os
import sys
import sqlite3
from datetime import datetime, date, timedelta
from decimal import Decimal
import random

# Configurar path para el proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.insert(0, project_dir)

class TestDataGenerator:
    """Generador de datos de prueba para el sistema de divisas"""
    
    def __init__(self, db_path="databases/storage.sqlite"):
        """Inicializar generador con conexión a base de datos"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Conectar a la base de datos"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"✅ Conectado a la base de datos: {self.db_path}")
            return True
        except Exception as e:
            print(f"❌ Error conectando a la base de datos: {e}")
            return False
    
    def disconnect(self):
        """Desconectar de la base de datos"""
        if self.conn:
            self.conn.close()
            print("✅ Desconectado de la base de datos")
    
    def clear_test_data(self):
        """Limpiar datos de prueba existentes"""
        try:
            print("🧹 Limpiando datos de prueba existentes...")
            
            # Eliminar en orden correcto para respetar foreign keys
            tables_to_clear = [
                'movimientos_cuenta',
                'transacciones', 
                'cuentas',
                'clientes'
            ]
            
            for table in tables_to_clear:
                # Solo eliminar registros de prueba (que contengan 'TEST' en algún campo)
                if table == 'clientes':
                    self.cursor.execute("""
                        DELETE FROM clientes 
                        WHERE cedula LIKE 'V-TEST%' OR cedula LIKE 'E-TEST%'
                    """)
                elif table == 'cuentas':
                    self.cursor.execute("""
                        DELETE FROM cuentas 
                        WHERE numero_cuenta LIKE '2001TEST%'
                    """)
                else:
                    # Para otras tablas, eliminar por referencia a clientes de prueba
                    continue
            
            # Eliminar usuarios de prueba
            self.cursor.execute("""
                DELETE FROM auth_user 
                WHERE email LIKE '%@test.com' OR email LIKE '%@prueba.com'
            """)
            
            self.conn.commit()
            print("✅ Datos de prueba anteriores eliminados")
            
        except Exception as e:
            print(f"⚠️  Error limpiando datos: {e}")
            self.conn.rollback()
    
    def generate_test_users(self):
        """Generar usuarios de prueba con diferentes estados"""
        print("👥 Generando usuarios de prueba...")
        
        # Datos de usuarios de prueba
        test_users = [
            {
                'first_name': 'Franklin',
                'last_name': 'Rodríguez',
                'email': 'franklin.rodriguez@test.com',
                'password': 'pbkdf2(1000,20,sha512)$12345678$test_hash',
                'telefono': '04141234567',
                'direccion': 'Caracas, Distrito Capital, Venezuela',
                'fecha_nacimiento': date(1985, 3, 15),
                'estado': 'activo'
            },
            {
                'first_name': 'María',
                'last_name': 'González',
                'email': 'maria.gonzalez@test.com',
                'password': 'pbkdf2(1000,20,sha512)$12345678$test_hash',
                'telefono': '04241234567',
                'direccion': 'Valencia, Carabobo, Venezuela',
                'fecha_nacimiento': date(1990, 7, 22),
                'estado': 'activo'
            },
            {
                'first_name': 'Carlos',
                'last_name': 'Martínez',
                'email': 'carlos.martinez@test.com',
                'password': 'pbkdf2(1000,20,sha512)$12345678$test_hash',
                'telefono': '04161234567',
                'direccion': 'Maracaibo, Zulia, Venezuela',
                'fecha_nacimiento': date(1988, 11, 8),
                'estado': 'inactivo'
            },
            {
                'first_name': 'Ana',
                'last_name': 'López',
                'email': 'ana.lopez@test.com',
                'password': 'pbkdf2(1000,20,sha512)$12345678$test_hash',
                'telefono': '04121234567',
                'direccion': 'Barquisimeto, Lara, Venezuela',
                'fecha_nacimiento': date(1992, 5, 30),
                'estado': 'activo'
            },
            {
                'first_name': 'José',
                'last_name': 'Hernández',
                'email': 'jose.hernandez@test.com',
                'password': 'pbkdf2(1000,20,sha512)$12345678$test_hash',
                'telefono': '04261234567',
                'direccion': 'Puerto Ordaz, Bolívar, Venezuela',
                'fecha_nacimiento': date(1987, 9, 12),
                'estado': 'activo'
            },
            {
                'first_name': 'Carmen',
                'last_name': 'Pérez',
                'email': 'carmen.perez@test.com',
                'password': 'pbkdf2(1000,20,sha512)$12345678$test_hash',
                'telefono': '04141234568',
                'direccion': 'Mérida, Mérida, Venezuela',
                'fecha_nacimiento': date(1983, 12, 3),
                'estado': 'inactivo'
            },
            {
                'first_name': 'Roberto',
                'last_name': 'Silva',
                'email': 'roberto.silva@test.com',
                'password': 'pbkdf2(1000,20,sha512)$12345678$test_hash',
                'telefono': '04251234567',
                'direccion': 'San Cristóbal, Táchira, Venezuela',
                'fecha_nacimiento': date(1991, 4, 18),
                'estado': 'activo'
            },
            {
                'first_name': 'Luisa',
                'last_name': 'Morales',
                'email': 'luisa.morales@test.com',
                'password': 'pbkdf2(1000,20,sha512)$12345678$test_hash',
                'telefono': '04141234569',
                'direccion': 'Cumana, Sucre, Venezuela',
                'fecha_nacimiento': date(1989, 8, 25),
                'estado': 'activo'
            }
        ]
        
        user_ids = []
        
        try:
            for i, user_data in enumerate(test_users, 1):
                self.cursor.execute("""
                    INSERT INTO auth_user (
                        first_name, last_name, email, password, telefono, 
                        direccion, fecha_nacimiento, estado
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_data['first_name'],
                    user_data['last_name'],
                    user_data['email'],
                    user_data['password'],
                    user_data['telefono'],
                    user_data['direccion'],
                    user_data['fecha_nacimiento'],
                    user_data['estado']
                ))
                
                user_id = self.cursor.lastrowid
                user_ids.append(user_id)
                
                print(f"  ✅ Usuario creado: {user_data['first_name']} {user_data['last_name']} (ID: {user_id}, Estado: {user_data['estado']})")
            
            self.conn.commit()
            print(f"✅ {len(test_users)} usuarios de prueba creados")
            return user_ids
            
        except Exception as e:
            print(f"❌ Error creando usuarios: {e}")
            self.conn.rollback()
            return []
    
    def generate_test_clients(self, user_ids):
        """Generar clientes de prueba asociados a los usuarios"""
        print("🏦 Generando clientes de prueba...")
        
        # Cédulas de prueba
        test_cedulas = [
            'V-TEST001',
            'V-TEST002', 
            'E-TEST003',
            'V-TEST004',
            'V-TEST005',
            'E-TEST006',
            'V-TEST007',
            'V-TEST008'
        ]
        
        client_ids = []
        
        try:
            for i, user_id in enumerate(user_ids):
                if i < len(test_cedulas):
                    cedula = test_cedulas[i]
                    fecha_registro = datetime.now() - timedelta(days=random.randint(1, 365))
                    
                    self.cursor.execute("""
                        INSERT INTO clientes (user_id, cedula, fecha_registro)
                        VALUES (?, ?, ?)
                    """, (user_id, cedula, fecha_registro))
                    
                    client_id = self.cursor.lastrowid
                    client_ids.append(client_id)
                    
                    print(f"  ✅ Cliente creado: {cedula} (ID: {client_id}, User ID: {user_id})")
            
            self.conn.commit()
            print(f"✅ {len(client_ids)} clientes de prueba creados")
            return client_ids
            
        except Exception as e:
            print(f"❌ Error creando clientes: {e}")
            self.conn.rollback()
            return []
    
    def generate_test_accounts(self, client_ids):
        """Generar cuentas de prueba con diferentes tipos y saldos"""
        print("💳 Generando cuentas de prueba...")
        
        account_types = ['corriente', 'ahorro']
        account_ids = []
        
        try:
            for i, client_id in enumerate(client_ids):
                # Cada cliente puede tener 1-2 cuentas
                num_accounts = random.randint(1, 2)
                
                for j in range(num_accounts):
                    # Generar número de cuenta único
                    account_number = f"2001TEST{str(client_id).zfill(4)}{str(j+1).zfill(4)}{str(random.randint(1000, 9999))}"
                    
                    # Tipo de cuenta
                    account_type = account_types[j % len(account_types)]
                    
                    # Generar saldos aleatorios realistas
                    saldo_ves = Decimal(str(random.uniform(100000, 5000000))).quantize(Decimal('0.01'))
                    saldo_usd = Decimal(str(random.uniform(100, 10000))).quantize(Decimal('0.01'))
                    saldo_eur = Decimal(str(random.uniform(50, 5000))).quantize(Decimal('0.01'))
                    saldo_usdt = Decimal(str(random.uniform(0, 1000))).quantize(Decimal('0.01'))
                    
                    # Estado de cuenta (mayoría activas)
                    estado = 'activa' if random.random() > 0.1 else 'inactiva'
                    
                    fecha_creacion = datetime.now() - timedelta(days=random.randint(30, 300))
                    
                    self.cursor.execute("""
                        INSERT INTO cuentas (
                            cliente_id, numero_cuenta, tipo_cuenta, 
                            saldo_ves, saldo_usd, saldo_eur, saldo_usdt,
                            estado, fecha_creacion
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        client_id, account_number, account_type,
                        float(saldo_ves), float(saldo_usd), float(saldo_eur), float(saldo_usdt),
                        estado, fecha_creacion
                    ))
                    
                    account_id = self.cursor.lastrowid
                    account_ids.append(account_id)
                    
                    print(f"  ✅ Cuenta creada: {account_number} ({account_type}, {estado})")
                    print(f"     Saldos: VES {saldo_ves:,.2f}, USD {saldo_usd:,.2f}, EUR {saldo_eur:,.2f}, USDT {saldo_usdt:,.2f}")
            
            self.conn.commit()
            print(f"✅ {len(account_ids)} cuentas de prueba creadas")
            return account_ids
            
        except Exception as e:
            print(f"❌ Error creando cuentas: {e}")
            self.conn.rollback()
            return []
    
    def generate_test_exchange_rates(self):
        """Generar tasas de cambio de prueba"""
        print("💱 Generando tasas de cambio de prueba...")
        
        try:
            # Tasas actuales aproximadas (ejemplo)
            today = date.today()
            
            self.cursor.execute("""
                INSERT OR REPLACE INTO tasas_cambio (
                    fecha, hora, usd_ves, eur_ves, usdt_ves, fuente, activa
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                today,
                datetime.now().time(),
                36.50,  # USD/VES
                39.80,  # EUR/VES  
                36.45,  # USDT/VES
                'BCV',
                True
            ))
            
            self.conn.commit()
            print("✅ Tasas de cambio de prueba creadas")
            
        except Exception as e:
            print(f"❌ Error creando tasas de cambio: {e}")
            self.conn.rollback()
    
    def verify_test_data(self):
        """Verificar que los datos de prueba se crearon correctamente"""
        print("🔍 Verificando datos de prueba creados...")
        
        try:
            # Verificar usuarios
            self.cursor.execute("""
                SELECT COUNT(*) FROM auth_user 
                WHERE email LIKE '%@test.com'
            """)
            user_count = self.cursor.fetchone()[0]
            print(f"  👥 Usuarios de prueba: {user_count}")
            
            # Verificar clientes
            self.cursor.execute("""
                SELECT COUNT(*) FROM clientes 
                WHERE cedula LIKE '%TEST%'
            """)
            client_count = self.cursor.fetchone()[0]
            print(f"  🏦 Clientes de prueba: {client_count}")
            
            # Verificar cuentas
            self.cursor.execute("""
                SELECT COUNT(*) FROM cuentas 
                WHERE numero_cuenta LIKE '%TEST%'
            """)
            account_count = self.cursor.fetchone()[0]
            print(f"  💳 Cuentas de prueba: {account_count}")
            
            # Verificar distribución por estado de usuarios
            self.cursor.execute("""
                SELECT estado, COUNT(*) FROM auth_user 
                WHERE email LIKE '%@test.com'
                GROUP BY estado
            """)
            status_distribution = self.cursor.fetchall()
            print("  📊 Distribución por estado de usuarios:")
            for estado, count in status_distribution:
                print(f"     {estado}: {count}")
            
            # Verificar distribución por tipo de cuenta
            self.cursor.execute("""
                SELECT tipo_cuenta, COUNT(*) FROM cuentas 
                WHERE numero_cuenta LIKE '%TEST%'
                GROUP BY tipo_cuenta
            """)
            account_type_distribution = self.cursor.fetchall()
            print("  📊 Distribución por tipo de cuenta:")
            for tipo, count in account_type_distribution:
                print(f"     {tipo}: {count}")
            
            # Verificar saldos totales
            self.cursor.execute("""
                SELECT 
                    SUM(saldo_ves) as total_ves,
                    SUM(saldo_usd) as total_usd,
                    SUM(saldo_eur) as total_eur,
                    SUM(saldo_usdt) as total_usdt
                FROM cuentas 
                WHERE numero_cuenta LIKE '%TEST%'
            """)
            totals = self.cursor.fetchone()
            print("  💰 Saldos totales en cuentas de prueba:")
            print(f"     VES: {totals[0]:,.2f}")
            print(f"     USD: {totals[1]:,.2f}")
            print(f"     EUR: {totals[2]:,.2f}")
            print(f"     USDT: {totals[3]:,.2f}")
            
            # Probar la consulta que usa el controlador
            print("\n🔍 Probando consulta del controlador de clientes...")
            self.cursor.execute("""
                SELECT 
                    c.id as client_id,
                    c.cedula,
                    c.fecha_registro,
                    u.first_name,
                    u.last_name,
                    u.email,
                    u.estado
                FROM clientes c
                JOIN auth_user u ON c.user_id = u.id
                WHERE c.cedula LIKE '%TEST%'
                ORDER BY c.fecha_registro DESC
            """)
            
            test_clients = self.cursor.fetchall()
            print(f"  📋 Clientes que deberían aparecer en la vista: {len(test_clients)}")
            
            for client in test_clients[:3]:  # Mostrar solo los primeros 3
                print(f"     ID: {client[0]}, Nombre: {client[3]} {client[4]}, Cédula: {client[1]}, Estado: {client[6]}")
            
            if len(test_clients) > 3:
                print(f"     ... y {len(test_clients) - 3} más")
            
            print("✅ Verificación completada")
            return True
            
        except Exception as e:
            print(f"❌ Error verificando datos: {e}")
            return False
    
    def run_full_generation(self):
        """Ejecutar generación completa de datos de prueba"""
        print("🚀 INICIANDO GENERACIÓN DE DATOS DE PRUEBA")
        print("=" * 60)
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        if not self.connect():
            return False
        
        try:
            # Limpiar datos anteriores
            self.clear_test_data()
            
            # Generar usuarios
            user_ids = self.generate_test_users()
            if not user_ids:
                print("❌ No se pudieron crear usuarios")
                return False
            
            # Generar clientes
            client_ids = self.generate_test_clients(user_ids)
            if not client_ids:
                print("❌ No se pudieron crear clientes")
                return False
            
            # Generar cuentas
            account_ids = self.generate_test_accounts(client_ids)
            if not account_ids:
                print("❌ No se pudieron crear cuentas")
                return False
            
            # Generar tasas de cambio
            self.generate_test_exchange_rates()
            
            # Verificar datos
            if self.verify_test_data():
                print("\n" + "=" * 60)
                print("✅ GENERACIÓN DE DATOS DE PRUEBA COMPLETADA EXITOSAMENTE")
                print("=" * 60)
                print()
                print("📋 RESUMEN:")
                print(f"   • {len(user_ids)} usuarios creados")
                print(f"   • {len(client_ids)} clientes creados")
                print(f"   • {len(account_ids)} cuentas creadas")
                print("   • Tasas de cambio actualizadas")
                print()
                print("🔍 PRÓXIMOS PASOS:")
                print("   1. Acceder a la vista de listado de clientes")
                print("   2. Verificar que los datos se muestren correctamente")
                print("   3. Probar filtros de búsqueda")
                print("   4. Verificar paginación si hay más de 20 registros")
                print()
                return True
            else:
                print("❌ Error en la verificación de datos")
                return False
                
        except Exception as e:
            print(f"❌ Error durante la generación: {e}")
            return False
        
        finally:
            self.disconnect()


def main():
    """Función principal"""
    generator = TestDataGenerator()
    success = generator.run_full_generation()
    
    if success:
        print("🎉 ¡Datos de prueba generados exitosamente!")
        print("   Ahora puedes probar las vistas de clientes y cuentas.")
    else:
        print("💥 Error generando datos de prueba.")
        print("   Revisa los mensajes de error anteriores.")
    
    return success


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)