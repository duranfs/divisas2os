# -*- coding: utf-8 -*-
"""
Script para regenerar los archivos .table con fake_migrate
"""

import sys
import os

# Configurar path para web2py
web2py_path = r'C:\web2py'
sys.path.insert(0, web2py_path)
os.chdir(web2py_path)

# Importar módulos de web2py
from gluon import *
from gluon.dal import DAL, Field

print("\n" + "=" * 80)
print("REGENERACIÓN DE ARCHIVOS .TABLE")
print("=" * 80)

# Conectar a la base de datos con fake_migrate=True
db_uri = 'sqlite://storage.sqlite'
db_folder = os.path.join(web2py_path, 'applications', 'divisas2os', 'databases')

print(f"\nConectando a la base de datos...")
print(f"URI: {db_uri}")
print(f"Folder: {db_folder}")

try:
    # Crear conexión con fake_migrate=True
    db = DAL(db_uri, folder=db_folder, migrate=True, fake_migrate_all=True)
    
    print("\n✅ Conexión establecida")
    
    # Definir tablas principales (simplificado)
    print("\nRegenerando archivos .table...")
    
    # Auth tables
    db.define_table('auth_user',
        Field('first_name'),
        Field('last_name'),
        Field('email'),
        Field('password'),
        Field('registration_key'),
        Field('reset_password_key'),
        Field('registration_id'),
        Field('telefono'),
        Field('direccion', 'text'),
        Field('fecha_nacimiento', 'date'),
        Field('estado'),
        migrate=True,
        fake_migrate=True
    )
    
    db.define_table('auth_group',
        Field('role'),
        Field('description', 'text'),
        migrate=True,
        fake_migrate=True
    )
    
    db.define_table('auth_membership',
        Field('user_id', 'reference auth_user'),
        Field('group_id', 'reference auth_group'),
        migrate=True,
        fake_migrate=True
    )
    
    db.define_table('auth_permission',
        Field('group_id', 'reference auth_group'),
        Field('name'),
        Field('table_name'),
        Field('record_id', 'integer'),
        migrate=True,
        fake_migrate=True
    )
    
    db.define_table('auth_event',
        Field('time_stamp', 'datetime'),
        Field('client_ip'),
        Field('user_id', 'reference auth_user'),
        Field('origin'),
        Field('description', 'text'),
        migrate=True,
        fake_migrate=True
    )
    
    db.define_table('auth_cas',
        Field('user_id', 'reference auth_user'),
        Field('created_on', 'datetime'),
        Field('service'),
        Field('ticket'),
        Field('renew', 'boolean'),
        migrate=True,
        fake_migrate=True
    )
    
    # Clientes
    db.define_table('clientes',
        Field('cedula', 'string', length=20),
        Field('nombre', 'string', length=100),
        Field('apellido', 'string', length=100),
        Field('telefono', 'string', length=20),
        Field('email', 'string', length=100),
        Field('direccion', 'text'),
        Field('fecha_registro', 'datetime'),
        Field('estado', 'string'),
        migrate=True,
        fake_migrate=True
    )
    
    # Cuentas - CON LOS NUEVOS CAMPOS
    db.define_table('cuentas',
        Field('cliente_id', 'reference clientes'),
        Field('numero_cuenta', 'string', length=20),
        Field('tipo_cuenta', 'string'),
        Field('saldo_ves', 'decimal(15,2)'),
        Field('saldo_usd', 'decimal(15,2)'),
        Field('saldo_eur', 'decimal(15,2)'),
        Field('estado', 'string'),
        Field('fecha_creacion', 'datetime'),
        Field('saldo_usdt', 'decimal(15,2)'),
        Field('moneda', 'string', length=10),  # NUEVO CAMPO
        Field('saldo', 'decimal(15,4)'),  # NUEVO CAMPO
        Field('fecha_actualizacion', 'datetime'),
        migrate=True,
        fake_migrate=True
    )
    
    # Tasas de cambio
    db.define_table('tasas_cambio',
        Field('fecha', 'date'),
        Field('hora', 'time'),
        Field('usd_ves', 'decimal(10,4)'),
        Field('eur_ves', 'decimal(10,4)'),
        Field('usdt_ves', 'decimal(10,4)'),
        Field('fuente', 'string'),
        Field('activa', 'boolean'),
        migrate=True,
        fake_migrate=True
    )
    
    # Transacciones - CON LOS NUEVOS CAMPOS
    db.define_table('transacciones',
        Field('cuenta_origen_id', 'reference cuentas'),  # NUEVO CAMPO
        Field('cuenta_destino_id', 'reference cuentas'),  # NUEVO CAMPO
        Field('cuenta_id', 'reference cuentas'),
        Field('tipo_operacion', 'string'),
        Field('moneda_origen', 'string', length=3),
        Field('moneda_destino', 'string', length=3),
        Field('monto_origen', 'decimal(15,2)'),
        Field('monto_destino', 'decimal(15,2)'),
        Field('tasa_aplicada', 'decimal(10,4)'),
        Field('comision', 'decimal(15,2)'),
        Field('numero_comprobante', 'string', length=50),
        Field('estado', 'string'),
        Field('fecha_transaccion', 'datetime'),
        Field('observaciones', 'text'),
        migrate=True,
        fake_migrate=True
    )
    
    # Movimientos de cuenta
    db.define_table('movimientos_cuenta',
        Field('cuenta_id', 'reference cuentas'),
        Field('tipo_movimiento', 'string'),
        Field('moneda', 'string', length=3),
        Field('monto', 'decimal(15,2)'),
        Field('saldo_anterior', 'decimal(15,2)'),
        Field('saldo_nuevo', 'decimal(15,2)'),
        Field('transaccion_id', 'reference transacciones'),
        Field('fecha_movimiento', 'datetime'),
        Field('descripcion', 'text'),
        migrate=True,
        fake_migrate=True
    )
    
    # Configuración
    db.define_table('configuracion',
        Field('clave', 'string', length=50),
        Field('valor', 'text'),
        Field('descripcion', 'text'),
        Field('tipo_dato', 'string'),
        Field('fecha_actualizacion', 'datetime'),
        migrate=True,
        fake_migrate=True
    )
    
    # Logs de auditoría
    db.define_table('logs_auditoria',
        Field('usuario_id', 'reference auth_user'),
        Field('accion', 'string'),
        Field('tabla_afectada', 'string'),
        Field('registro_id', 'integer'),
        Field('datos_anteriores', 'text'),
        Field('datos_nuevos', 'text'),
        Field('ip_address', 'string'),
        Field('fecha_hora', 'datetime'),
        Field('descripcion', 'text'),
        migrate=True,
        fake_migrate=True
    )
    
    # Scheduler tables
    db.define_table('scheduler_task',
        Field('application_name'),
        Field('task_name'),
        Field('group_name'),
        Field('status'),
        Field('function_name'),
        Field('uuid'),
        Field('args', 'text'),
        Field('vars', 'text'),
        Field('enabled', 'boolean'),
        Field('start_time', 'datetime'),
        Field('next_run_time', 'datetime'),
        Field('stop_time', 'datetime'),
        Field('repeats', 'integer'),
        Field('retry_failed', 'integer'),
        Field('period', 'integer'),
        Field('prevent_drift', 'boolean'),
        Field('cronline'),
        Field('timeout', 'integer'),
        Field('sync_output', 'integer'),
        Field('times_run', 'integer'),
        Field('times_failed', 'integer'),
        Field('last_run_time', 'datetime'),
        Field('assigned_worker_name'),
        migrate=True,
        fake_migrate=True
    )
    
    db.define_table('scheduler_run',
        Field('task_id', 'reference scheduler_task'),
        Field('status'),
        Field('start_time', 'datetime'),
        Field('stop_time', 'datetime'),
        Field('run_output', 'text'),
        Field('run_result', 'text'),
        Field('traceback', 'text'),
        Field('worker_name'),
        migrate=True,
        fake_migrate=True
    )
    
    db.define_table('scheduler_worker',
        Field('worker_name'),
        Field('first_heartbeat', 'datetime'),
        Field('last_heartbeat', 'datetime'),
        Field('status'),
        Field('is_ticker', 'boolean'),
        Field('group_names', 'list:string'),
        Field('worker_stats', 'text'),
        migrate=True,
        fake_migrate=True
    )
    
    db.define_table('scheduler_task_deps',
        Field('task_parent', 'integer'),
        Field('task_child', 'integer'),
        Field('can_visit', 'boolean'),
        migrate=True,
        fake_migrate=True
    )
    
    # Commit
    db.commit()
    
    print("\n✅ Archivos .table regenerados exitosamente")
    
    # Listar archivos generados
    import glob
    table_files = glob.glob(os.path.join(db_folder, '*.table'))
    print(f"\nArchivos .table generados: {len(table_files)}")
    for tf in sorted(table_files):
        print(f"  - {os.path.basename(tf)}")
    
    print("\n" + "=" * 80)
    print("✅ REGENERACIÓN COMPLETADA")
    print("=" * 80)
    print("\nAhora web2py debería poder iniciar correctamente")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
