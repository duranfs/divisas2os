#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para instalar completamente el módulo de Remesas y Límites
"""

import os
import sqlite3
from datetime import datetime

def crear_tablas_bd():
    """Crear tablas en la base de datos"""
    
    print("\n📊 Creando tablas en la base de datos...")
    
    try:
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        # Tabla remesas_diarias
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS remesas_diarias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                moneda VARCHAR(10) NOT NULL,
                monto_recibido DECIMAL(15,2) NOT NULL DEFAULT 0,
                monto_disponible DECIMAL(15,2) NOT NULL DEFAULT 0,
                monto_vendido DECIMAL(15,2) NOT NULL DEFAULT 0,
                monto_reservado DECIMAL(15,2) NOT NULL DEFAULT 0,
                fuente_remesa VARCHAR(100),
                numero_referencia VARCHAR(50),
                observaciones TEXT,
                usuario_registro INTEGER,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                activa BOOLEAN DEFAULT 1,
                FOREIGN KEY (usuario_registro) REFERENCES auth_user(id)
            )
        """)
        print("   ✅ Tabla remesas_diarias creada")
        
        # Tabla limites_venta
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS limites_venta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                moneda VARCHAR(10) NOT NULL,
                limite_diario DECIMAL(15,2) NOT NULL DEFAULT 0,
                monto_vendido DECIMAL(15,2) NOT NULL DEFAULT 0,
                monto_disponible DECIMAL(15,2) NOT NULL DEFAULT 0,
                porcentaje_utilizado DECIMAL(5,2) DEFAULT 0,
                alerta_80_enviada BOOLEAN DEFAULT 0,
                alerta_95_enviada BOOLEAN DEFAULT 0,
                usuario_configuracion INTEGER,
                fecha_configuracion DATETIME DEFAULT CURRENT_TIMESTAMP,
                activo BOOLEAN DEFAULT 1,
                FOREIGN KEY (usuario_configuracion) REFERENCES auth_user(id)
            )
        """)
        print("   ✅ Tabla limites_venta creada")
        
        # Tabla movimientos_remesas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimientos_remesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                remesa_id INTEGER NOT NULL,
                tipo_movimiento VARCHAR(20) NOT NULL,
                monto DECIMAL(15,2) NOT NULL,
                saldo_anterior DECIMAL(15,2) NOT NULL,
                saldo_nuevo DECIMAL(15,2) NOT NULL,
                transaccion_id INTEGER,
                descripcion TEXT,
                usuario INTEGER,
                fecha_movimiento DATETIME DEFAULT CURRENT_TIMESTAMP,
                ip_address VARCHAR(50),
                FOREIGN KEY (remesa_id) REFERENCES remesas_diarias(id),
                FOREIGN KEY (transaccion_id) REFERENCES transacciones(id),
                FOREIGN KEY (usuario) REFERENCES auth_user(id)
            )
        """)
        print("   ✅ Tabla movimientos_remesas creada")
        
        # Tabla alertas_limites
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alertas_limites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_alerta VARCHAR(20) NOT NULL,
                moneda VARCHAR(10) NOT NULL,
                umbral_porcentaje DECIMAL(5,2) NOT NULL,
                mensaje_alerta TEXT,
                enviar_email BOOLEAN DEFAULT 1,
                emails_destino TEXT,
                activa BOOLEAN DEFAULT 1,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("   ✅ Tabla alertas_limites creada")
        
        # Crear índices
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_remesas_fecha_moneda ON remesas_diarias(fecha, moneda)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_limites_fecha_moneda ON limites_venta(fecha, moneda)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_movimientos_remesa ON movimientos_remesas(remesa_id)")
        print("   ✅ Índices creados")
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error creando tablas: {str(e)}")
        return False

def insertar_datos_ejemplo():
    """Insertar datos de ejemplo para pruebas"""
    
    print("\n📝 Insertando datos de ejemplo...")
    
    try:
        conn = sqlite3.connect('databases/storage.sqlite')
        cursor = conn.cursor()
        
        fecha_hoy = datetime.now().date().strftime('%Y-%m-%d')
        
        # Remesas de ejemplo
        remesas_ejemplo = [
            (fecha_hoy, 'USD', 10000.00, 10000.00, 0, 0, 'Banco Corresponsal USA', 'REF-USD-001', 'Remesa inicial USD', 1),
            (fecha_hoy, 'EUR', 8000.00, 8000.00, 0, 0, 'Banco Corresponsal EUR', 'REF-EUR-001', 'Remesa inicial EUR', 1),
            (fecha_hoy, 'USDT', 15000.00, 15000.00, 0, 0, 'Exchange Crypto', 'REF-USDT-001', 'Remesa inicial USDT', 1),
        ]
        
        for remesa in remesas_ejemplo:
            cursor.execute("""
                INSERT INTO remesas_diarias 
                (fecha, moneda, monto_recibido, monto_disponible, monto_vendido, monto_reservado, 
                 fuente_remesa, numero_referencia, observaciones, usuario_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, remesa)
        
        print("   ✅ Remesas de ejemplo insertadas")
        
        # Límites de ejemplo
        limites_ejemplo = [
            (fecha_hoy, 'USD', 9000.00, 0, 9000.00, 0, 0, 0, 1),
            (fecha_hoy, 'EUR', 7000.00, 0, 7000.00, 0, 0, 0, 1),
            (fecha_hoy, 'USDT', 13000.00, 0, 13000.00, 0, 0, 0, 1),
        ]
        
        for limite in limites_ejemplo:
            cursor.execute("""
                INSERT INTO limites_venta 
                (fecha, moneda, limite_diario, monto_vendido, monto_disponible, 
                 porcentaje_utilizado, alerta_80_enviada, alerta_95_enviada, usuario_configuracion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, limite)
        
        print("   ✅ Límites de ejemplo insertados")
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error insertando datos: {str(e)}")
        return False

def verificar_archivos():
    """Verificar que todos los archivos necesarios existen"""
    
    print("\n📁 Verificando archivos del módulo...")
    
    archivos_requeridos = [
        "controllers/remesas.py",
        "views/remesas/index.html",
        "views/remesas/registrar_remesa.html",
        "views/remesas/configurar_limites.html",
        "views/remesas/historial_movimientos.html",
        "views/remesas/ajustar_remesa.html"
    ]
    
    todos_existen = True
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} - NO ENCONTRADO")
            todos_existen = False
    
    return todos_existen

def mostrar_resumen_instalacion():
    """Mostrar resumen de la instalación"""
    
    print("\n" + "="*60)
    print("🏦 MÓDULO DE REMESAS Y LÍMITES INSTALADO")
    print("="*60)
    print()
    print("✅ COMPONENTES INSTALADOS:")
    print("- 4 tablas de base de datos")
    print("- 1 controlador (remesas.py)")
    print("- 5 vistas HTML")
    print("- Funciones auxiliares")
    print()
    print("📊 FUNCIONALIDADES DISPONIBLES:")
    print("- Registro de remesas diarias")
    print("- Configuración de límites de venta")
    print("- Historial de movimientos")
    print("- Ajustes manuales con auditoría")
    print("- Dashboard de disponibilidad")
    print("- Alertas automáticas")
    print()
    print("🚀 PRÓXIMOS PASOS:")
    print("1. Agregar enlace al menú de navegación")
    print("2. Configurar alertas por email (opcional)")
    print("3. Integrar con módulo de ventas")
    print("4. Probar funcionalidad completa")
    print()
    print("📍 ACCESO AL MÓDULO:")
    print("URL: http://127.0.0.1:8000/divisas2os/remesas")
    print("Requiere: Rol de Administrador")
    print()
    print("="*60)

def generar_codigo_menu():
    """Generar código para agregar al menú"""
    
    codigo_menu = """
# Agregar al menú de administración en models/menu.py o layout.html

{{if auth.has_membership('administrador'):}}
<li class="nav-item dropdown">
  <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">
    <i class="fas fa-money-bill-wave me-1"></i>Remesas
  </a>
  <div class="dropdown-menu">
    <a class="dropdown-item" href="{{=URL('remesas','index')}}">
      <i class="fas fa-tachometer-alt me-2"></i>Dashboard
    </a>
    <a class="dropdown-item" href="{{=URL('remesas','registrar_remesa')}}">
      <i class="fas fa-plus-circle me-2"></i>Registrar Remesa
    </a>
    <a class="dropdown-item" href="{{=URL('remesas','configurar_limites')}}">
      <i class="fas fa-cog me-2"></i>Configurar Límites
    </a>
    <a class="dropdown-item" href="{{=URL('remesas','historial_movimientos')}}">
      <i class="fas fa-history me-2"></i>Historial
    </a>
  </div>
</li>
{{pass}}
"""
    
    with open("codigo_menu_remesas.txt", 'w', encoding='utf-8') as f:
        f.write(codigo_menu)
    
    print("\n📝 Código del menú generado: codigo_menu_remesas.txt")

if __name__ == "__main__":
    print("🏦 INSTALACIÓN DEL MÓDULO DE REMESAS Y LÍMITES")
    print("="*60)
    
    # Verificar archivos
    archivos_ok = verificar_archivos()
    
    if not archivos_ok:
        print("\n❌ Faltan archivos necesarios. Ejecuta primero agregar_modulo_remesas.py")
        exit(1)
    
    # Crear tablas
    tablas_ok = crear_tablas_bd()
    
    if not tablas_ok:
        print("\n❌ Error creando tablas")
        exit(1)
    
    # Insertar datos de ejemplo
    datos_ok = insertar_datos_ejemplo()
    
    # Generar código del menú
    generar_codigo_menu()
    
    # Mostrar resumen
    mostrar_resumen_instalacion()
    
    if tablas_ok and datos_ok:
        print("\n🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
    else:
        print("\n⚠️  Instalación completada con advertencias")