# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
import os
import re

REQUIRED_WEB2PY_VERSION = "3.0.10"

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

web2py_version_string = request.global_settings.web2py_version.split("-")[0]
web2py_version = list(map(int, web2py_version_string.split(".")[:3]))
if web2py_version < list(map(int, REQUIRED_WEB2PY_VERSION.split(".")[:3])):
    raise HTTP(500, f"Requires web2py version {REQUIRED_WEB2PY_VERSION} or newer, not {web2py_version_string}")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if "GAE_APPLICATION" not in os.environ:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get("db.uri"),
             pool_size=configuration.get("db.pool_size"),
             migrate_enabled=configuration.get("db.migrate"),
             check_reserved=["all"])
else:
    # ---------------------------------------------------------------------
    # connect to Google Firestore
    # ---------------------------------------------------------------------
    db = DAL("firestore")
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be "controller/function.extension"
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get("app.production"):
    response.generic_patterns.append("*")

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = "bootstrap3_stacked"
response.form_label_separator = ""

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = "concat,minify,inline"
# response.optimize_js = "concat,minify,inline"

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = "0.0.0"

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get("host.names"))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields["auth_user"] = [
    Field('telefono', 'string', length=20, label='Teléfono'),
    Field('direccion', 'text', label='Dirección'),
    Field('fecha_nacimiento', 'date', label='Fecha de Nacimiento'),
    Field('estado', 'string', default='activo', label='Estado')
]

# Configurar separador de etiquetas
auth.settings.label_separator = ''

auth.define_tables(username=False, signature=False)

# Configurar etiquetas y comentarios después de definir las tablas
db.auth_user.first_name.label = 'Nombres'
db.auth_user.first_name.comment = 'Ingrese sus nombres completos'

db.auth_user.last_name.label = 'Apellidos'
db.auth_user.last_name.comment = 'Ingrese sus apellidos completos'

db.auth_user.email.label = 'Correo Electrónico'
db.auth_user.email.comment = 'Será usado para iniciar sesión'

db.auth_user.password.label = 'Contraseña'
db.auth_user.password.comment = 'Cualquier contraseña'

# Configurar etiquetas y comentarios para campos extra
db.auth_user.telefono.label = 'Teléfono'
db.auth_user.telefono.comment = 'Formato: 04141234567'
db.auth_user.direccion.label = 'Dirección'
db.auth_user.direccion.comment = 'Dirección completa de residencia'
db.auth_user.fecha_nacimiento.label = 'Fecha de Nacimiento'
db.auth_user.fecha_nacimiento.comment = 'Formato: AAAA-MM-DD'

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = "logging" if request.is_local else configuration.get("smtp.server")
mail.settings.sender = configuration.get("smtp.sender")
mail.settings.login = configuration.get("smtp.login")
mail.settings.tls = configuration.get("smtp.tls") or False
mail.settings.ssl = configuration.get("smtp.ssl") or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.password_min_length = 1
auth.settings.login_after_registration = False

# -------------------------------------------------------------------------
# Configuración de Seguridad Avanzada
# -------------------------------------------------------------------------

# Configuración de validación de contraseña
auth.settings.password_field = 'password'
db.auth_user.password.requires = [IS_NOT_EMPTY(error_message='La contraseña es requerida'), CRYPT()]

# Configuración adicional de seguridad - SIMPLIFICADA
auth.settings.login_next = URL('default', 'dashboard')
auth.settings.logout_next = URL('default', 'index')
auth.settings.profile_next = URL('default', 'dashboard')
auth.settings.register_next = URL('default', 'index')

# Configurar sesión
auth.settings.expiration = 3600  # Sesión expira en 1 hora

# Configurar campos obligatorios para registro
auth.settings.register_fields = [
    'first_name', 'last_name', 'email', 'password', 'password_two',
    'telefono', 'direccion', 'fecha_nacimiento'
]

# Configurar etiquetas de campos en español
db.auth_user.first_name.label = 'Nombres'
db.auth_user.last_name.label = 'Apellidos'
db.auth_user.email.label = 'Correo Electrónico'
db.auth_user.password.label = 'Contraseña'
db.auth_user.telefono.label = 'Teléfono'
db.auth_user.direccion.label = 'Dirección'
db.auth_user.fecha_nacimiento.label = 'Fecha de Nacimiento'

# Configurar comentarios de ayuda para los campos
db.auth_user.first_name.comment = 'Ingrese sus nombres completos'
db.auth_user.last_name.comment = 'Ingrese sus apellidos completos'
db.auth_user.email.comment = 'Este será su nombre de usuario para ingresar al sistema'
db.auth_user.password.comment = 'Cualquier contraseña'
db.auth_user.telefono.comment = 'Formato: 04141234567 (11 dígitos)'
db.auth_user.direccion.comment = 'Dirección completa de residencia'
db.auth_user.fecha_nacimiento.comment = 'Formato: AAAA-MM-DD (debe ser mayor de edad)'

# Personalizar mensajes de validación
db.auth_user.first_name.requires = [
    IS_NOT_EMPTY(error_message='El nombre es requerido'),
    #IS_LENGTH(1, 100, error_message='El nombre debe tener entre 1 y 100 caracteres')
]

db.auth_user.last_name.requires = [
    IS_NOT_EMPTY(error_message='El apellido es requerido'),
    #IS_LENGTH(1, 100, error_message='El apellido debe tener entre 1 y 100 caracteres')
]

db.auth_user.email.requires = [
    IS_NOT_EMPTY(error_message='El email es requerido'),
    IS_EMAIL(error_message='Formato de email inválido'),
    IS_NOT_IN_DB(db, 'auth_user.email', error_message='Este email ya está registrado')
]

# -------------------------------------------------------------------------
# Funciones de Seguridad Adicionales
# -------------------------------------------------------------------------

def registrar_intento_login(email, exitoso=True, ip_address=None):
    """Registra intentos de login para auditoría"""
    if not ip_address:
        ip_address = request.env.remote_addr
    
    # Crear tabla de intentos de login si no existe
    if 'intentos_login' not in db.tables:
        db.define_table('intentos_login',
            Field('email', 'string', length=255),
            Field('ip_address', 'string', length=45),
            Field('exitoso', 'boolean'),
            Field('fecha_intento', 'datetime', default=request.now),
            Field('user_agent', 'text')
        )
    
    db.intentos_login.insert(
        email=email,
        ip_address=ip_address,
        exitoso=exitoso,
        user_agent=request.env.http_user_agent or ''
    )
    db.commit()

def verificar_intentos_fallidos(email, limite=5, ventana_minutos=15):
    """Verifica si hay demasiados intentos fallidos recientes"""
    if 'intentos_login' not in db.tables:
        return False
    
    from datetime import datetime, timedelta
    
    tiempo_limite = datetime.now() - timedelta(minutes=ventana_minutos)
    
    intentos_fallidos = db(
        (db.intentos_login.email == email) &
        (db.intentos_login.exitoso == False) &
        (db.intentos_login.fecha_intento > tiempo_limite)
    ).count()
    
    return intentos_fallidos >= limite

def bloquear_usuario_temporalmente(user_id, minutos=30):
    """Bloquea temporalmente un usuario"""
    if 'bloqueos_temporales' not in db.tables:
        db.define_table('bloqueos_temporales',
            Field('user_id', 'reference auth_user'),
            Field('fecha_bloqueo', 'datetime', default=request.now),
            Field('fecha_desbloqueo', 'datetime'),
            Field('motivo', 'string', length=255),
            Field('activo', 'boolean', default=True)
        )
    
    from datetime import datetime, timedelta
    
    fecha_desbloqueo = datetime.now() + timedelta(minutes=minutos)
    
    db.bloqueos_temporales.insert(
        user_id=user_id,
        fecha_desbloqueo=fecha_desbloqueo,
        motivo='Demasiados intentos de login fallidos',
        activo=True
    )
    db.commit()

def usuario_bloqueado_temporalmente(user_id):
    """Verifica si un usuario está bloqueado temporalmente"""
    if 'bloqueos_temporales' not in db.tables:
        return False
    
    from datetime import datetime
    
    bloqueo = db(
        (db.bloqueos_temporales.user_id == user_id) &
        (db.bloqueos_temporales.activo == True) &
        (db.bloqueos_temporales.fecha_desbloqueo > datetime.now())
    ).select().first()
    
    return bloqueo is not None

# -------------------------------------------------------------------------
# Hooks de Autenticación Personalizados
# -------------------------------------------------------------------------

def custom_login_onaccept(form):
    """Hook ejecutado después de login exitoso - SIMPLIFICADO"""
    try:
        if auth.user:
            # Solo asignar rol si no tiene ninguno
            if not auth.has_membership():
                # Buscar si ya existe un registro de cliente
                cliente = db(db.clientes.user_id == auth.user.id).select().first()
                if cliente:
                    auth.add_membership('cliente', auth.user.id)
    except Exception as e:
        # No fallar el login por errores en el hook
        pass

def custom_login_onfail(form):
    """Hook ejecutado después de login fallido - SIMPLIFICADO"""
    try:
        # Solo logging básico, sin bloqueos
        email = form.vars.email if form.vars else 'unknown'
        print(f"Login fallido para: {email}")
    except Exception as e:
        # No interferir con el proceso de login
        pass

def custom_register_onaccept(form):
    """Hook ejecutado después de registro exitoso"""
    if form.vars:
        # El usuario se registra como cliente por defecto
        user_id = form.vars.id
        auth.add_membership('cliente', user_id)
        
        # Crear registro en tabla clientes si se proporciona cédula
        # (esto se manejará en el controlador de clientes)

# Asignar hooks personalizados - SOLO LOS SEGUROS
auth.settings.login_onaccept = custom_login_onaccept
# auth.settings.login_onfail = custom_login_onfail  # Deshabilitado para evitar interferencias
# auth.settings.register_onaccept = custom_register_onaccept

# -------------------------------------------------------------------------
# Sistema de Logging de Auditoría
# -------------------------------------------------------------------------

# Tabla de logs de auditoría
db.define_table('logs_auditoria',
    Field('usuario_id', 'reference auth_user'),
    Field('accion', 'string', length=100),
    Field('modulo', 'string', length=50),
    Field('tabla_afectada', 'string', length=50),
    Field('registro_id', 'integer'),
    Field('datos_anteriores', 'json'),
    Field('datos_nuevos', 'json'),
    Field('ip_address', 'string', length=45),
    Field('user_agent', 'text'),
    Field('fecha_accion', 'datetime', default=request.now),
    Field('resultado', 'string', length=20, default='exitoso'),
    Field('mensaje_error', 'text'),
    Field('session_id', 'string', length=100),
    format='%(accion)s - %(modulo)s - %(fecha_accion)s'
)

# Validaciones para logs de auditoría
db.logs_auditoria.accion.requires = IS_IN_SET([
    'login', 'logout', 'registro', 'crear', 'actualizar', 'eliminar',
    'consultar', 'transaccion_compra', 'transaccion_venta', 'cambio_password',
    'bloqueo_usuario', 'desbloqueo_usuario', 'cambio_rol', 'acceso_denegado'
], error_message='Acción de auditoría inválida')

db.logs_auditoria.modulo.requires = IS_IN_SET([
    'auth', 'clientes', 'cuentas', 'divisas', 'transacciones', 
    'tasas_cambio', 'reportes', 'configuracion', 'admin'
], error_message='Módulo inválido')

db.logs_auditoria.resultado.requires = IS_IN_SET([
    'exitoso', 'fallido', 'bloqueado', 'denegado'
], error_message='Resultado inválido')

# -------------------------------------------------------------------------
# Funciones de Logging de Auditoría
# -------------------------------------------------------------------------

def log_auditoria(accion, modulo, tabla_afectada=None, registro_id=None, 
                  datos_anteriores=None, datos_nuevos=None, resultado='exitoso', 
                  mensaje_error=None, usuario_id=None):
    """
    Registra una acción en el log de auditoría
    
    Args:
        accion: Tipo de acción realizada
        modulo: Módulo donde se realizó la acción
        tabla_afectada: Tabla de la base de datos afectada
        registro_id: ID del registro afectado
        datos_anteriores: Datos antes del cambio (para updates)
        datos_nuevos: Datos después del cambio
        resultado: Resultado de la operación
        mensaje_error: Mensaje de error si la operación falló
        usuario_id: ID del usuario (si no se proporciona, usa el usuario actual)
    """
    try:
        if not usuario_id:
            usuario_id = auth.user_id
        
        # Convertir registro_id a entero si es necesario
        if registro_id is not None:
            try:
                if hasattr(registro_id, 'id'):
                    registro_id = registro_id.id
                elif hasattr(registro_id, '_id'):
                    registro_id = registro_id._id
                registro_id = int(str(registro_id).strip()) if registro_id else None
            except:
                registro_id = None
        
        # Obtener información de la sesión
        ip_address = request.env.remote_addr or 'unknown'
        user_agent = request.env.http_user_agent or ''
        session_id = str(session._session_id) if hasattr(session, '_session_id') else ''
        
        # Insertar log
        db.logs_auditoria.insert(
            usuario_id=usuario_id,
            accion=accion,
            modulo=modulo,
            tabla_afectada=tabla_afectada,
            registro_id=registro_id,
            datos_anteriores=datos_anteriores,
            datos_nuevos=datos_nuevos,
            ip_address=ip_address,
            user_agent=user_agent,
            resultado=resultado,
            mensaje_error=mensaje_error,
            session_id=session_id
        )
        db.commit()
        
    except Exception as e:
        # Si falla el logging, no debe afectar la operación principal
        import logging
        logging.error(f"Error en log de auditoría: {str(e)}")

def log_transaccion(tipo_operacion, cuenta_id, monto_origen, moneda_origen, 
                   monto_destino, moneda_destino, tasa_aplicada, 
                   numero_comprobante, resultado='exitoso', mensaje_error=None):
    """Registra específicamente transacciones de divisas"""
    
    # Convertir cuenta_id a entero si es necesario
    try:
        if hasattr(cuenta_id, 'id'):
            cuenta_id = cuenta_id.id
        elif hasattr(cuenta_id, '_id'):
            cuenta_id = cuenta_id._id
        cuenta_id = int(str(cuenta_id).strip()) if cuenta_id else None
    except:
        cuenta_id = None
    
    datos_transaccion = {
        'tipo_operacion': tipo_operacion,
        'cuenta_id': cuenta_id,
        'monto_origen': float(monto_origen) if monto_origen else None,
        'moneda_origen': moneda_origen,
        'monto_destino': float(monto_destino) if monto_destino else None,
        'moneda_destino': moneda_destino,
        'tasa_aplicada': float(tasa_aplicada) if tasa_aplicada else None,
        'numero_comprobante': numero_comprobante
    }
    
    accion = f'transaccion_{tipo_operacion}'
    
    log_auditoria(
        accion=accion,
        modulo='divisas',
        tabla_afectada='transacciones',
        datos_nuevos=datos_transaccion,
        resultado=resultado,
        mensaje_error=mensaje_error
    )

def log_cambio_saldo(cuenta_id, moneda, saldo_anterior, saldo_nuevo, motivo):
    """Registra cambios en saldos de cuentas"""
    
    # Convertir cuenta_id a entero si es necesario
    try:
        if hasattr(cuenta_id, 'id'):
            cuenta_id = cuenta_id.id
        elif hasattr(cuenta_id, '_id'):
            cuenta_id = cuenta_id._id
        cuenta_id = int(str(cuenta_id).strip()) if cuenta_id else None
    except:
        cuenta_id = None
    
    datos_cambio = {
        'cuenta_id': cuenta_id,
        'moneda': moneda,
        'saldo_anterior': float(saldo_anterior),
        'saldo_nuevo': float(saldo_nuevo),
        'motivo': motivo
    }
    
    log_auditoria(
        accion='actualizar',
        modulo='cuentas',
        tabla_afectada='cuentas',
        registro_id=cuenta_id,
        datos_anteriores={'saldo': float(saldo_anterior)},
        datos_nuevos={'saldo': float(saldo_nuevo)},
        resultado='exitoso'
    )

def log_acceso_modulo(modulo, accion='consultar', resultado='exitoso', mensaje_error=None):
    """Registra accesos a módulos del sistema"""
    
    log_auditoria(
        accion=accion,
        modulo=modulo,
        resultado=resultado,
        mensaje_error=mensaje_error
    )

def log_cambio_configuracion(clave, valor_anterior, valor_nuevo):
    """Registra cambios en la configuración del sistema"""
    
    datos_cambio = {
        'clave': clave,
        'valor_anterior': valor_anterior,
        'valor_nuevo': valor_nuevo
    }
    
    log_auditoria(
        accion='actualizar',
        modulo='configuracion',
        tabla_afectada='configuracion',
        datos_anteriores={'valor': valor_anterior},
        datos_nuevos={'valor': valor_nuevo},
        resultado='exitoso'
    )

# -------------------------------------------------------------------------
# Funciones de Consulta de Logs
# -------------------------------------------------------------------------

def obtener_logs_usuario(user_id, limite=100, offset=0):
    """Obtiene los logs de un usuario específico"""
    
    logs = db(db.logs_auditoria.usuario_id == user_id).select(
        orderby=~db.logs_auditoria.fecha_accion,
        limitby=(offset, offset + limite)
    )
    
    return logs

def obtener_logs_modulo(modulo, fecha_inicio=None, fecha_fin=None, limite=100):
    """Obtiene los logs de un módulo específico"""
    
    query = db.logs_auditoria.modulo == modulo
    
    if fecha_inicio:
        query &= db.logs_auditoria.fecha_accion >= fecha_inicio
    
    if fecha_fin:
        query &= db.logs_auditoria.fecha_accion <= fecha_fin
    
    logs = db(query).select(
        orderby=~db.logs_auditoria.fecha_accion,
        limitby=(0, limite)
    )
    
    return logs

def obtener_logs_transacciones(fecha_inicio=None, fecha_fin=None, limite=100):
    """Obtiene logs específicos de transacciones"""
    
    query = db.logs_auditoria.accion.belongs(['transaccion_compra', 'transaccion_venta'])
    
    if fecha_inicio:
        query &= db.logs_auditoria.fecha_accion >= fecha_inicio
    
    if fecha_fin:
        query &= db.logs_auditoria.fecha_accion <= fecha_fin
    
    logs = db(query).select(
        orderby=~db.logs_auditoria.fecha_accion,
        limitby=(0, limite)
    )
    
    return logs

def obtener_estadisticas_auditoria(fecha_inicio=None, fecha_fin=None):
    """Obtiene estadísticas de auditoría"""
    
    query = db.logs_auditoria.id > 0
    
    if fecha_inicio:
        query &= db.logs_auditoria.fecha_accion >= fecha_inicio
    
    if fecha_fin:
        query &= db.logs_auditoria.fecha_accion <= fecha_fin
    
    # Contar por acción
    stats_accion = db(query).select(
        db.logs_auditoria.accion,
        db.logs_auditoria.id.count(),
        groupby=db.logs_auditoria.accion
    )
    
    # Contar por módulo
    stats_modulo = db(query).select(
        db.logs_auditoria.modulo,
        db.logs_auditoria.id.count(),
        groupby=db.logs_auditoria.modulo
    )
    
    # Contar por resultado
    stats_resultado = db(query).select(
        db.logs_auditoria.resultado,
        db.logs_auditoria.id.count(),
        groupby=db.logs_auditoria.resultado
    )
    
    return {
        'por_accion': stats_accion,
        'por_modulo': stats_modulo,
        'por_resultado': stats_resultado
    }

# -------------------------------------------------------------------------
# Hooks de Auditoría para Tablas Críticas
# -------------------------------------------------------------------------

def audit_callback_insert(table, fields):
    """Callback para auditar inserciones"""
    tabla_nombre = str(table)
    
    # Solo auditar tablas críticas
    if tabla_nombre in ['clientes', 'cuentas', 'transacciones', 'tasas_cambio', 'configuracion']:
        log_auditoria(
            accion='crear',
            modulo=tabla_nombre,
            tabla_afectada=tabla_nombre,
            datos_nuevos=dict(fields)
        )

def audit_callback_insert_safe(table, fields, record_id):
    """Callback seguro para auditar inserciones con manejo correcto de ID"""
    try:
        tabla_nombre = str(table)
        
        # Solo auditar tablas críticas
        if tabla_nombre in ['clientes', 'cuentas', 'transacciones', 'tasas_cambio', 'configuracion']:
            # Convertir ID de forma segura
            safe_id = None
            if record_id is not None:
                try:
                    safe_id = int(record_id)
                except (ValueError, TypeError):
                    safe_id = None
            
            log_auditoria(
                accion='crear',
                modulo=tabla_nombre,
                tabla_afectada=tabla_nombre,
                registro_id=safe_id,
                datos_nuevos=dict(fields)
            )
    except Exception as e:
        # No fallar si hay error en auditoría
        import logging
        logging.error(f"Error en audit_callback_insert_safe: {str(e)}")

def audit_callback_update_safe(table, fields, record_id):
    """Callback seguro para auditar actualizaciones con manejo correcto de ID"""
    try:
        tabla_nombre = str(table)
        
        # Solo auditar tablas críticas
        if tabla_nombre in ['clientes', 'cuentas', 'transacciones', 'tasas_cambio', 'configuracion']:
            # Convertir ID de forma segura
            safe_id = None
            if record_id is not None:
                try:
                    safe_id = int(record_id)
                except (ValueError, TypeError):
                    safe_id = None
            
            # Obtener datos anteriores de forma segura
            datos_anteriores = {}
            if safe_id:
                try:
                    record = db(table.id == safe_id).select().first()
                    datos_anteriores = dict(record) if record else {}
                except:
                    datos_anteriores = {}
            
            log_auditoria(
                accion='actualizar',
                modulo=tabla_nombre,
                tabla_afectada=tabla_nombre,
                registro_id=safe_id,
                datos_anteriores=datos_anteriores,
                datos_nuevos=dict(fields)
            )
    except Exception as e:
        # No fallar si hay error en auditoría
        import logging
        logging.error(f"Error en audit_callback_update_safe: {str(e)}")

def audit_callback_update(table, fields, record_id):
    """Callback para auditar actualizaciones"""
    tabla_nombre = str(table)
    
    # Solo auditar tablas críticas
    if tabla_nombre in ['clientes', 'cuentas', 'transacciones', 'tasas_cambio', 'configuracion']:
        # Obtener datos anteriores
        record = db(table.id == record_id).select().first()
        datos_anteriores = dict(record) if record else {}
        
        log_auditoria(
            accion='actualizar',
            modulo=tabla_nombre,
            tabla_afectada=tabla_nombre,
            registro_id=record_id,
            datos_anteriores=datos_anteriores,
            datos_nuevos=dict(fields)
        )

def audit_callback_delete(table, record_id):
    """Callback para auditar eliminaciones"""
    tabla_nombre = str(table)
    
    # Solo auditar tablas críticas
    if tabla_nombre in ['clientes', 'cuentas', 'transacciones', 'tasas_cambio', 'configuracion']:
        # Obtener datos antes de eliminar
        record = db(table.id == record_id).select().first()
        datos_anteriores = dict(record) if record else {}
        
        log_auditoria(
            accion='eliminar',
            modulo=tabla_nombre,
            tabla_afectada=tabla_nombre,
            registro_id=record_id,
            datos_anteriores=datos_anteriores
        )







# Configurar mensajes de autenticación en español (solo mensajes básicos válidos)
auth.messages.verify_email = 'Haga clic en el enlace %(link)s para verificar su email'
auth.messages.verify_email_subject = 'Verificación de email - Sistema de Divisas'

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get("app.author")
response.meta.description = configuration.get("app.description")
response.meta.keywords = configuration.get("app.keywords")
response.meta.generator = configuration.get("app.generator")
response.show_toolbar = configuration.get("app.toolbar")

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get("google.analytics_id")

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get("scheduler.enabled"):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get("scheduler.heartbeat"))

# -------------------------------------------------------------------------
# Sistema de Divisas Bancario - Definición de Tablas
# -------------------------------------------------------------------------

# Tabla de Clientes (extiende auth_user)
db.define_table('clientes',
    Field('user_id', 'reference auth_user', unique=True),
    Field('cedula', 'string', length=20, unique=True),
    Field('fecha_registro', 'datetime', default=request.now),
    format='%(cedula)s'
)

# Tabla de Cuentas
db.define_table('cuentas',
    Field('cliente_id', 'reference clientes'),
    Field('numero_cuenta', 'string', length=20, unique=True),
    Field('tipo_cuenta', 'string', default='corriente'),
    Field('saldo_ves', 'decimal(15,2)', default=0),
    Field('saldo_usd', 'decimal(15,2)', default=0),
    Field('saldo_eur', 'decimal(15,2)', default=0),
    Field('saldo_usdt', 'decimal(15,2)', default=0),
    Field('estado', 'string', default='activa'),
    Field('fecha_creacion', 'datetime', default=request.now),
    format='%(numero_cuenta)s'
)

# Tabla de Tasas de Cambio
db.define_table('tasas_cambio',
    Field('fecha', 'date', default=request.now.date()),
    Field('hora', 'time', default=request.now.time()),
    Field('usd_ves', 'decimal(10,4)'),
    Field('eur_ves', 'decimal(10,4)'),
    Field('usdt_ves', 'decimal(10,4)'),
    Field('fuente', 'string', default='BCV'),
    Field('activa', 'boolean', default=True),
    format='%(fecha)s - USD: %(usd_ves)s'
)

# Tabla de Transacciones
db.define_table('transacciones',
    Field('cuenta_id', 'reference cuentas'),
    Field('tipo_operacion', 'string'), # 'compra' o 'venta'
    Field('moneda_origen', 'string', length=3),
    Field('moneda_destino', 'string', length=3),
    Field('monto_origen', 'decimal(15,2)'),
    Field('monto_destino', 'decimal(15,2)'),
    Field('tasa_aplicada', 'decimal(10,4)'),
    Field('comision', 'decimal(15,2)', default=0),
    Field('numero_comprobante', 'string', length=50, unique=True),
    Field('estado', 'string', default='completada'),
    Field('fecha_transaccion', 'datetime', default=request.now),
    Field('observaciones', 'text'),
    format='%(numero_comprobante)s'
)

# Tabla de Movimientos de Cuenta (para historial detallado)
db.define_table('movimientos_cuenta',
    Field('cuenta_id', 'reference cuentas'),
    Field('tipo_movimiento', 'string'), # 'debito' o 'credito'
    Field('moneda', 'string', length=3),
    Field('monto', 'decimal(15,2)'),
    Field('saldo_anterior', 'decimal(15,2)', default=0),
    Field('saldo_nuevo', 'decimal(15,2)', default=0),
    Field('descripcion', 'text'),
    Field('transaccion_relacionada', 'reference transacciones'),
    Field('fecha_movimiento', 'datetime', default=request.now),
    Field('usuario_id', 'reference auth_user'),
    format='%(descripcion)s'
)

# Tabla de Configuración del Sistema
db.define_table('configuracion',
    Field('clave', 'string', length=50, unique=True),
    Field('valor', 'text'),
    Field('descripcion', 'text'),
    Field('fecha_actualizacion', 'datetime', default=request.now),
    format='%(clave)s'
)

# -------------------------------------------------------------------------
# Configurar callbacks de auditoría
# -------------------------------------------------------------------------

# Configurar callbacks de auditoría para las tablas
db.clientes._after_insert.append(lambda fields, id: audit_callback_insert_safe(db.clientes, fields, id))
db.clientes._after_update.append(lambda fields, id: audit_callback_update_safe(db.clientes, fields, id))
db.clientes._before_delete.append(lambda record_id: audit_callback_delete(db.clientes, record_id))

db.cuentas._after_insert.append(lambda fields, id: audit_callback_insert_safe(db.cuentas, fields, id))
db.cuentas._after_update.append(lambda fields, id: audit_callback_update_safe(db.cuentas, fields, id))
db.cuentas._before_delete.append(lambda record_id: audit_callback_delete(db.cuentas, record_id))

db.transacciones._after_insert.append(lambda fields, id: audit_callback_insert_safe(db.transacciones, fields, id))
db.transacciones._after_update.append(lambda fields, id: audit_callback_update_safe(db.transacciones, fields, id))
db.transacciones._before_delete.append(lambda record_id: audit_callback_delete(db.transacciones, record_id))

# Callbacks de auditoría para tasas_cambio (con conversión de ID)
db.tasas_cambio._after_insert.append(lambda fields, id: audit_callback_insert_safe(db.tasas_cambio, fields, id))
db.tasas_cambio._after_update.append(lambda fields, id: audit_callback_update_safe(db.tasas_cambio, fields, id))
db.tasas_cambio._before_delete.append(lambda record_id: audit_callback_delete(db.tasas_cambio, record_id))

db.configuracion._after_insert.append(lambda fields, id: audit_callback_insert_safe(db.configuracion, fields, id))
db.configuracion._after_update.append(lambda fields, id: audit_callback_update_safe(db.configuracion, fields, id))
db.configuracion._before_delete.append(lambda record_id: audit_callback_delete(db.configuracion, record_id))

# -------------------------------------------------------------------------
# Validaciones y Restricciones de Datos
# -------------------------------------------------------------------------

# Validaciones para auth_user (campos adicionales)
db.auth_user.telefono.requires = [
    IS_NOT_EMPTY(error_message='El teléfono es requerido'),
    IS_MATCH(r'^0[0-9]{10}$', error_message='Formato de teléfono inválido. Use formato venezolano: 04141234567 (11 dígitos)')
]

db.auth_user.direccion.requires = IS_NOT_EMPTY(error_message='La dirección es requerida')

def validar_edad_minima(fecha_nacimiento):
    """Validar que el usuario sea mayor de 18 años"""
    from datetime import date
    if isinstance(fecha_nacimiento, str):
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        except:
            return (fecha_nacimiento, 'Formato de fecha inválido')
    
    if isinstance(fecha_nacimiento, date):
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        if edad < 18:
            return (fecha_nacimiento, 'Debe ser mayor de 18 años')
    
    return (fecha_nacimiento, None)

db.auth_user.fecha_nacimiento.requires = [
    IS_NOT_EMPTY(error_message='La fecha de nacimiento es requerida'),
    IS_DATE(error_message='Formato de fecha inválido'),
    validar_edad_minima
]

db.auth_user.estado.requires = IS_IN_SET(['activo', 'inactivo'], 
                                        error_message='Estado debe ser activo o inactivo')

# Validaciones para clientes
db.clientes.user_id.requires = IS_IN_DB(db, 'auth_user.id', '%(first_name)s %(last_name)s')

db.clientes.cedula.requires = [
    IS_NOT_EMPTY(error_message='La cédula es requerida'),
    IS_MATCH(r'^[VE]-?\d{7,8}$', error_message='Formato de cédula inválido (V-12345678 o E-12345678)'),
    IS_NOT_IN_DB(db, 'clientes.cedula', error_message='Esta cédula ya está registrada')
]

# Validaciones para cuentas
db.cuentas.cliente_id.requires = IS_IN_DB(db, 'clientes.id', '%(cedula)s')

db.cuentas.numero_cuenta.requires = [
    IS_NOT_EMPTY(error_message='El número de cuenta es requerido'),
    IS_LENGTH(20, 20, error_message='El número de cuenta debe tener exactamente 20 caracteres'),
    IS_MATCH(r'^\d{20}$', error_message='El número de cuenta debe contener solo dígitos'),
    IS_NOT_IN_DB(db, 'cuentas.numero_cuenta', error_message='Este número de cuenta ya existe')
]

db.cuentas.tipo_cuenta.requires = IS_IN_SET(['corriente', 'ahorro'], 
                                           error_message='Tipo de cuenta debe ser corriente o ahorro')

db.cuentas.saldo_ves.requires = IS_DECIMAL_IN_RANGE(0, 999999999999.99, 
                                                   error_message='Saldo VES debe ser un valor positivo')
db.cuentas.saldo_usd.requires = IS_DECIMAL_IN_RANGE(0, 999999999999.99, 
                                                   error_message='Saldo USD debe ser un valor positivo')
db.cuentas.saldo_eur.requires = IS_DECIMAL_IN_RANGE(0, 999999999999.99, 
                                                   error_message='Saldo EUR debe ser un valor positivo')

db.cuentas.estado.requires = IS_IN_SET(['activa', 'inactiva', 'bloqueada'], 
                                      error_message='Estado debe ser activa, inactiva o bloqueada')

# Validaciones para tasas de cambio
db.tasas_cambio.fecha.requires = IS_DATE(error_message='Formato de fecha inválido')
db.tasas_cambio.hora.requires = IS_TIME(error_message='Formato de hora inválido')

db.tasas_cambio.usd_ves.requires = [
    IS_NOT_EMPTY(error_message='La tasa USD/VES es requerida'),
    IS_DECIMAL_IN_RANGE(0.0001, 999999.9999, error_message='Tasa USD/VES debe ser un valor positivo')
]

db.tasas_cambio.eur_ves.requires = [
    IS_NOT_EMPTY(error_message='La tasa EUR/VES es requerida'),
    IS_DECIMAL_IN_RANGE(0.0001, 999999.9999, error_message='Tasa EUR/VES debe ser un valor positivo')
]

db.tasas_cambio.fuente.requires = IS_IN_SET(['BCV', 'Manual', 'Backup'], 
                                           error_message='Fuente debe ser BCV, Manual o Backup')

# Validaciones para transacciones
db.transacciones.cuenta_id.requires = IS_IN_DB(db, 'cuentas.id', '%(numero_cuenta)s')

db.transacciones.tipo_operacion.requires = IS_IN_SET(['compra', 'venta'], 
                                                    error_message='Tipo de operación debe ser compra o venta')

db.transacciones.moneda_origen.requires = IS_IN_SET(['VES', 'USD', 'EUR'], 
                                                   error_message='Moneda origen debe ser VES, USD o EUR')

db.transacciones.moneda_destino.requires = IS_IN_SET(['VES', 'USD', 'EUR'], 
                                                    error_message='Moneda destino debe ser VES, USD o EUR')

db.transacciones.monto_origen.requires = [
    IS_NOT_EMPTY(error_message='El monto origen es requerido'),
    IS_DECIMAL_IN_RANGE(0.01, 999999999999.99, error_message='Monto origen debe ser mayor a 0')
]

db.transacciones.monto_destino.requires = [
    IS_NOT_EMPTY(error_message='El monto destino es requerido'),
    IS_DECIMAL_IN_RANGE(0.01, 999999999999.99, error_message='Monto destino debe ser mayor a 0')
]

db.transacciones.tasa_aplicada.requires = [
    IS_NOT_EMPTY(error_message='La tasa aplicada es requerida'),
    IS_DECIMAL_IN_RANGE(0.0001, 999999.9999, error_message='Tasa aplicada debe ser un valor positivo')
]

db.transacciones.comision.requires = IS_DECIMAL_IN_RANGE(0, 999999999999.99, 
                                                        error_message='Comisión debe ser un valor positivo o cero')

db.transacciones.numero_comprobante.requires = [
    IS_NOT_EMPTY(error_message='El número de comprobante es requerido'),
    IS_LENGTH(1, 50, error_message='Número de comprobante debe tener entre 1 y 50 caracteres'),
    IS_NOT_IN_DB(db, 'transacciones.numero_comprobante', error_message='Este número de comprobante ya existe')
]

db.transacciones.estado.requires = IS_IN_SET(['pendiente', 'completada', 'cancelada', 'fallida'], 
                                            error_message='Estado debe ser pendiente, completada, cancelada o fallida')

# Validaciones para configuración
db.configuracion.clave.requires = [
    IS_NOT_EMPTY(error_message='La clave es requerida'),
    IS_LENGTH(1, 50, error_message='Clave debe tener entre 1 y 50 caracteres'),
    IS_NOT_IN_DB(db, 'configuracion.clave', error_message='Esta clave ya existe')
]

db.configuracion.valor.requires = IS_NOT_EMPTY(error_message='El valor es requerido')
# Validaciones para movimientos de cuenta
db.movimientos_cuenta.cuenta_id.requires = IS_IN_DB(db, 'cuentas.id', '%(numero_cuenta)s')

db.movimientos_cuenta.tipo_movimiento.requires = IS_IN_SET(['debito', 'credito'], 
                                                          error_message='Tipo de movimiento debe ser debito o credito')

db.movimientos_cuenta.moneda.requires = IS_IN_SET(['VES', 'USD', 'EUR'], 
                                                 error_message='Moneda debe ser VES, USD o EUR')

db.movimientos_cuenta.monto.requires = [
    IS_NOT_EMPTY(error_message='El monto es requerido'),
    IS_DECIMAL_IN_RANGE(0.01, 999999999999.99, error_message='Monto debe ser mayor a 0')
]

db.movimientos_cuenta.saldo_anterior.requires = IS_DECIMAL_IN_RANGE(0, 999999999999.99, 
                                                                   error_message='Saldo anterior debe ser un valor positivo o cero')

db.movimientos_cuenta.saldo_nuevo.requires = IS_DECIMAL_IN_RANGE(0, 999999999999.99, 
                                                                error_message='Saldo nuevo debe ser un valor positivo o cero')

db.movimientos_cuenta.descripcion.requires = IS_NOT_EMPTY(error_message='La descripción es requerida')

db.configuracion.descripcion.requires = IS_NOT_EMPTY(error_message='La descripción es requerida')

# -------------------------------------------------------------------------
# Configuración de Roles y Permisos
# -------------------------------------------------------------------------

# Crear roles del sistema si no existen
if db(db.auth_group.role == 'administrador').isempty():
    auth.add_group('administrador', 'Administrador del sistema')

if db(db.auth_group.role == 'cliente').isempty():
    auth.add_group('cliente', 'Cliente bancario')

if db(db.auth_group.role == 'operador').isempty():
    auth.add_group('operador', 'Operador bancario')

# -------------------------------------------------------------------------
# Configuración de Permisos por Módulo
# -------------------------------------------------------------------------

# Función para configurar permisos iniciales
def configurar_permisos_iniciales():
    """Configura los permisos iniciales del sistema por rol"""
    
    # Obtener IDs de los grupos
    admin_group = db(db.auth_group.role == 'administrador').select().first()
    cliente_group = db(db.auth_group.role == 'cliente').select().first()
    operador_group = db(db.auth_group.role == 'operador').select().first()
    
    if not admin_group or not cliente_group or not operador_group:
        return
    
    # Permisos para ADMINISTRADOR - Acceso completo
    permisos_admin = [
        # Gestión de clientes
        ('read', 'clientes', 0),
        ('create', 'clientes', 0),
        ('update', 'clientes', 0),
        ('delete', 'clientes', 0),
        # Gestión de cuentas
        ('read', 'cuentas', 0),
        ('create', 'cuentas', 0),
        ('update', 'cuentas', 0),
        ('delete', 'cuentas', 0),
        # Transacciones
        ('read', 'transacciones', 0),
        ('create', 'transacciones', 0),
        ('update', 'transacciones', 0),
        ('delete', 'transacciones', 0),
        # Tasas de cambio
        ('read', 'tasas_cambio', 0),
        ('create', 'tasas_cambio', 0),
        ('update', 'tasas_cambio', 0),
        ('delete', 'tasas_cambio', 0),
        # Reportes
        ('read', 'reportes', 0),
        ('create', 'reportes', 0),
        # Configuración
        ('read', 'configuracion', 0),
        ('create', 'configuracion', 0),
        ('update', 'configuracion', 0),
        ('delete', 'configuracion', 0),
        # Módulos específicos
        ('access', 'admin_panel', 0),
        ('access', 'reportes_admin', 0),
        ('access', 'gestion_usuarios', 0)
    ]
    
    # Permisos para OPERADOR - Operaciones bancarias
    permisos_operador = [
        # Gestión de clientes (solo lectura y actualización)
        ('read', 'clientes', 0),
        ('update', 'clientes', 0),
        # Gestión de cuentas
        ('read', 'cuentas', 0),
        ('create', 'cuentas', 0),
        ('update', 'cuentas', 0),
        # Transacciones
        ('read', 'transacciones', 0),
        ('create', 'transacciones', 0),
        ('update', 'transacciones', 0),
        # Tasas de cambio (solo lectura)
        ('read', 'tasas_cambio', 0),
        # Reportes básicos
        ('read', 'reportes', 0),
        # Módulos específicos
        ('access', 'operaciones_divisas', 0),
        ('access', 'consulta_clientes', 0)
    ]
    
    # Permisos para CLIENTE - Solo sus propios datos
    permisos_cliente = [
        # Sus propios datos de cliente (lectura y actualización limitada)
        ('read', 'clientes', 0),
        ('update', 'clientes', 0),
        # Sus propias cuentas
        ('read', 'cuentas', 0),
        # Sus propias transacciones
        ('read', 'transacciones', 0),
        ('create', 'transacciones', 0),
        # Tasas de cambio (solo lectura)
        ('read', 'tasas_cambio', 0),
        # Módulos específicos
        ('access', 'perfil_cliente', 0),
        ('access', 'operaciones_propias', 0),
        ('access', 'consulta_saldos', 0)
    ]
    
    # Asignar permisos a cada grupo
    for permiso in permisos_admin:
        if not auth.has_permission(permiso[0], permiso[1], permiso[2], admin_group.id):
            auth.add_permission(admin_group.id, permiso[0], permiso[1], permiso[2])
    
    for permiso in permisos_operador:
        if not auth.has_permission(permiso[0], permiso[1], permiso[2], operador_group.id):
            auth.add_permission(operador_group.id, permiso[0], permiso[1], permiso[2])
    
    for permiso in permisos_cliente:
        if not auth.has_permission(permiso[0], permiso[1], permiso[2], cliente_group.id):
            auth.add_permission(cliente_group.id, permiso[0], permiso[1], permiso[2])

# Ejecutar configuración de permisos
configurar_permisos_iniciales()

# -------------------------------------------------------------------------
# Funciones de Control de Acceso
# -------------------------------------------------------------------------

def es_administrador(user_id=None):
    """Verifica si el usuario es administrador"""
    if not user_id:
        user_id = auth.user_id
    if not user_id:
        return False
    return auth.has_membership('administrador', user_id)

def es_operador(user_id=None):
    """Verifica si el usuario es operador"""
    if not user_id:
        user_id = auth.user_id
    if not user_id:
        return False
    return auth.has_membership('operador', user_id)

def es_cliente(user_id=None):
    """Verifica si el usuario es cliente"""
    if not user_id:
        user_id = auth.user_id
    if not user_id:
        return False
    return auth.has_membership('cliente', user_id)

def obtener_rol_usuario(user_id=None):
    """Obtiene el rol principal del usuario"""
    if not user_id:
        user_id = auth.user_id
    if not user_id:
        return None
    
    if es_administrador(user_id):
        return 'administrador'
    elif es_operador(user_id):
        return 'operador'
    elif es_cliente(user_id):
        return 'cliente'
    else:
        return None

def puede_acceder_modulo(modulo, user_id=None):
    """Verifica si el usuario puede acceder a un módulo específico"""
    if not user_id:
        user_id = auth.user_id
    if not user_id:
        return False
    
    return auth.has_permission('access', modulo, 0, user_id)

def puede_gestionar_cliente(cliente_id, user_id=None):
    """Verifica si el usuario puede gestionar un cliente específico"""
    if not user_id:
        user_id = auth.user_id
    if not user_id:
        return False
    
    # Administradores y operadores pueden gestionar cualquier cliente
    if es_administrador(user_id) or es_operador(user_id):
        return True
    
    # Los clientes solo pueden gestionar sus propios datos
    if es_cliente(user_id):
        cliente = db(db.clientes.id == cliente_id).select().first()
        if cliente and cliente.user_id == user_id:
            return True
    
    return False

def puede_gestionar_cuenta(cuenta_id, user_id=None):
    """Verifica si el usuario puede gestionar una cuenta específica"""
    if not user_id:
        user_id = auth.user_id
    if not user_id:
        return False
    
    # Administradores y operadores pueden gestionar cualquier cuenta
    if es_administrador(user_id) or es_operador(user_id):
        return True
    
    # Los clientes solo pueden gestionar sus propias cuentas
    if es_cliente(user_id):
        cuenta = db(db.cuentas.id == cuenta_id).select().first()
        if cuenta:
            cliente = db(db.clientes.id == cuenta.cliente_id).select().first()
            if cliente and cliente.user_id == user_id:
                return True
    
    return False

# -------------------------------------------------------------------------
# Decoradores para Control de Acceso
# -------------------------------------------------------------------------

def requiere_rol(*roles_permitidos):
    """Decorador que requiere que el usuario tenga uno de los roles especificados"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not auth.is_logged_in():
                redirect(auth.settings.login_url)
            
            rol_usuario = obtener_rol_usuario()
            if rol_usuario not in roles_permitidos:
                session.flash = 'No tiene permisos para acceder a esta función'
                redirect(URL('default', 'index'))
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def requiere_permiso(permiso, tabla, record_id=0):
    """Decorador que requiere un permiso específico"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not auth.is_logged_in():
                redirect(auth.settings.login_url)
            
            if not auth.has_permission(permiso, tabla, record_id):
                session.flash = 'No tiene permisos para realizar esta acción'
                redirect(URL('default', 'index'))
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# -------------------------------------------------------------------------
# Configuración inicial del sistema
# -------------------------------------------------------------------------

# Insertar configuraciones iniciales si no existen
if db(db.configuracion.clave == 'sistema_activo').isempty():
    db.configuracion.insert(
        clave='sistema_activo',
        valor='true',
        descripcion='Indica si el sistema está activo para transacciones'
    )

if db(db.configuracion.clave == 'comision_compra').isempty():
    db.configuracion.insert(
        clave='comision_compra',
        valor='0.005',
        descripcion='Comisión por operaciones de compra de divisas (0.5%)'
    )

if db(db.configuracion.clave == 'comision_venta').isempty():
    db.configuracion.insert(
        clave='comision_venta',
        valor='0.005',
        descripcion='Comisión por operaciones de venta de divisas (0.5%)'
    )

if db(db.configuracion.clave == 'url_bcv').isempty():
    db.configuracion.insert(
        clave='url_bcv',
        valor='https://www.bcv.org.ve/',
        descripcion='URL base del Banco Central de Venezuela para obtener tasas'
    )

# -------------------------------------------------------------------------
# Optimizaciones de Rendimiento - Índices de Base de Datos
# -------------------------------------------------------------------------

# Crear índices para consultas frecuentes
try:
    # Índices para tabla clientes
    db.executesql('CREATE INDEX IF NOT EXISTS idx_clientes_user_id ON clientes(user_id);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_clientes_cedula ON clientes(cedula);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_clientes_fecha_registro ON clientes(fecha_registro);')
    
    # Índices para tabla cuentas
    db.executesql('CREATE INDEX IF NOT EXISTS idx_cuentas_cliente_id ON cuentas(cliente_id);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_cuentas_numero_cuenta ON cuentas(numero_cuenta);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_cuentas_estado ON cuentas(estado);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_cuentas_fecha_creacion ON cuentas(fecha_creacion);')
    
    # Índices para tabla transacciones
    db.executesql('CREATE INDEX IF NOT EXISTS idx_transacciones_cuenta_id ON transacciones(cuenta_id);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_transacciones_fecha ON transacciones(fecha_transaccion);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_transacciones_tipo_operacion ON transacciones(tipo_operacion);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_transacciones_estado ON transacciones(estado);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_transacciones_numero_comprobante ON transacciones(numero_comprobante);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_transacciones_fecha_tipo ON transacciones(fecha_transaccion, tipo_operacion);')
    
    # Índices para tabla tasas_cambio
    db.executesql('CREATE INDEX IF NOT EXISTS idx_tasas_fecha ON tasas_cambio(fecha);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_tasas_activa ON tasas_cambio(activa);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_tasas_fecha_activa ON tasas_cambio(fecha, activa);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_tasas_fecha_hora ON tasas_cambio(fecha, hora);')
    
    # Índices para tabla movimientos_cuenta
    db.executesql('CREATE INDEX IF NOT EXISTS idx_movimientos_cuenta_id ON movimientos_cuenta(cuenta_id);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_movimientos_fecha ON movimientos_cuenta(fecha_movimiento);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_movimientos_transaccion ON movimientos_cuenta(transaccion_relacionada);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_movimientos_cuenta_fecha ON movimientos_cuenta(cuenta_id, fecha_movimiento);')
    
    # Índices para tabla logs_auditoria
    db.executesql('CREATE INDEX IF NOT EXISTS idx_logs_usuario_id ON logs_auditoria(usuario_id);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_logs_fecha_accion ON logs_auditoria(fecha_accion);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_logs_modulo ON logs_auditoria(modulo);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_logs_accion ON logs_auditoria(accion);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_logs_fecha_modulo ON logs_auditoria(fecha_accion, modulo);')
    
    # Índices para auth_user (campos adicionales)
    db.executesql('CREATE INDEX IF NOT EXISTS idx_auth_user_email ON auth_user(email);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_auth_user_estado ON auth_user(estado);')
    
    # Índices compuestos para consultas complejas
    db.executesql('CREATE INDEX IF NOT EXISTS idx_transacciones_cuenta_fecha_tipo ON transacciones(cuenta_id, fecha_transaccion, tipo_operacion);')
    db.executesql('CREATE INDEX IF NOT EXISTS idx_cuentas_cliente_estado ON cuentas(cliente_id, estado);')
    
except Exception as e:
    # Si hay error creando índices, no debe afectar la aplicación
    import logging
    logging.error(f"Error creando índices de base de datos: {str(e)}")

# -------------------------------------------------------------------------
# Sistema de Cache para Tasas de Cambio
# -------------------------------------------------------------------------

# Configurar cache para tasas de cambio
def obtener_tasas_cache():
    """Obtiene las tasas de cambio desde cache o base de datos"""
    def _obtener_tasas():
        tasa_actual = db(db.tasas_cambio.activa == True).select(
            orderby=~db.tasas_cambio.fecha | ~db.tasas_cambio.hora
        ).first()
        
        if tasa_actual:
            return {
                'usd_ves': float(tasa_actual.usd_ves),
                'eur_ves': float(tasa_actual.eur_ves),
                'fecha': str(tasa_actual.fecha),
                'hora': str(tasa_actual.hora),
                'fuente': tasa_actual.fuente,
                'timestamp': str(tasa_actual.fecha) + ' ' + str(tasa_actual.hora)
            }
        return None
    
    return cache.ram('tasas_cambio', _obtener_tasas, time_expire=300)  # 5 minutos

def limpiar_cache_tasas():
    """Limpia el cache de tasas de cambio"""
    cache.ram.clear('tasas_cambio')

# -------------------------------------------------------------------------
# Cache para Consultas Frecuentes
# -------------------------------------------------------------------------

# Cache para saldos de cuentas (1 minuto)
def obtener_saldos_cuenta_cache(cuenta_id):
    """Obtiene los saldos de una cuenta desde cache"""
    def _obtener_saldos():
        cuenta = db(db.cuentas.id == cuenta_id).select().first()
        if cuenta:
            return {
                'saldo_ves': float(cuenta.saldo_ves),
                'saldo_usd': float(cuenta.saldo_usd),
                'saldo_eur': float(cuenta.saldo_eur)
            }
        return None
    
    key = f"saldos_{cuenta_id}"
    return cache.ram(key, _obtener_saldos, time_expire=60)

def limpiar_cache_saldos(cuenta_id=None):
    """Limpia el cache de saldos"""
    if cuenta_id:
        key = f"saldos_{cuenta_id}"
        cache.ram.clear(key)
    else:
        cache.ram.clear('saldos_*')

# Cache para estadísticas del dashboard (5 minutos)
def obtener_estadisticas_dashboard_cache(user_id):
    """Obtiene estadísticas del dashboard desde cache"""
    def _obtener_estadisticas():
        # Obtener estadísticas básicas del usuario
        cliente = db((db.clientes.user_id == user_id) & 
                    (db.clientes.id == db.cuentas.cliente_id)).select().first()
        
        if cliente:
            return {
                'total_cuentas': db(db.cuentas.cliente_id == cliente.clientes.id).count(),
                'saldo_total_ves': db(db.cuentas.cliente_id == cliente.clientes.id).select(
                    db.cuentas.saldo_ves.sum()).first()[db.cuentas.saldo_ves.sum()] or 0,
                'saldo_total_usd': db(db.cuentas.cliente_id == cliente.clientes.id).select(
                    db.cuentas.saldo_usd.sum()).first()[db.cuentas.saldo_usd.sum()] or 0,
                'saldo_total_eur': db(db.cuentas.cliente_id == cliente.clientes.id).select(
                    db.cuentas.saldo_eur.sum()).first()[db.cuentas.saldo_eur.sum()] or 0
            }
        return None
    
    key = f"stats_{user_id}"
    return cache.ram(key, _obtener_estadisticas, time_expire=300)

def limpiar_cache_estadisticas(user_id=None):
    """Limpia el cache de estadísticas"""
    if user_id:
        key = f"stats_{user_id}"
        cache.ram.clear(key)
    else:
        cache.ram.clear('stats_*')

# -------------------------------------------------------------------------
# Configuración de breadcrumbs globales
# -------------------------------------------------------------------------
from breadcrumbs import set_breadcrumbs
set_breadcrumbs(response, request)

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

# -------------------------------------------------------------------------
# Funciones de Utilidad para Administración de Usuarios
# -------------------------------------------------------------------------

def aprobar_usuario_pendiente(email):
    """
    Aprueba un usuario que está pendiente de aprobación
    """
    try:
        # Buscar el usuario por email
        usuario = db(db.auth_user.email == email).select().first()
        
        if not usuario:
            return False, "Usuario no encontrado"
        
        if usuario.registration_key == '':
            return False, "El usuario ya está aprobado"
        
        # Aprobar el usuario
        db(db.auth_user.email == email).update(
            registration_key='',
            registration_id=''
        )
        
        # Asignar rol de cliente por defecto
        auth.add_membership('cliente', usuario.id)
        
        db.commit()
        return True, f"Usuario {email} aprobado exitosamente"
        
    except Exception as e:
        db.rollback()
        return False, f"Error al aprobar usuario: {str(e)}"

def listar_usuarios_pendientes():
    """
    Lista todos los usuarios pendientes de aprobación
    """
    try:
        usuarios_pendientes = db(
            (db.auth_user.registration_key != '') & 
            (db.auth_user.registration_key != None)
        ).select()
        
        return [(u.id, u.email, u.first_name, u.last_name) for u in usuarios_pendientes]
        
    except Exception as e:
        return []

def crear_primer_administrador():
    """
    Crea el primer administrador del sistema si no existe ninguno
    """
    try:
        # Verificar si ya existe un administrador
        admin_existente = db(
            (db.auth_membership.group_id == db.auth_group.id) &
            (db.auth_group.role == 'administrador')
        ).select().first()
        
        if admin_existente:
            return False, "Ya existe un administrador en el sistema"
        
        # Buscar el primer usuario registrado
        primer_usuario = db(db.auth_user.id > 0).select(orderby=db.auth_user.id).first()
        
        if not primer_usuario:
            # No hay usuarios, crear administrador por defecto
            admin_id = db.auth_user.insert(
                first_name='Administrador',
                last_name='Sistema',
                email='admin@sistema.com',
                password='admin123',  # Se hasheará automáticamente
                telefono='04141234567',
                direccion='Sistema',
                estado='activo'
            )
            primer_usuario = db(db.auth_user.id == admin_id).select().first()
        
        # Aprobar el usuario si está pendiente
        if primer_usuario.registration_key:
            db(db.auth_user.id == primer_usuario.id).update(
                registration_key='',
                registration_id=''
            )
        
        # Crear grupo de administrador si no existe
        grupo_admin = db(db.auth_group.role == 'administrador').select().first()
        if not grupo_admin:
            grupo_admin_id = db.auth_group.insert(
                role='administrador',
                description='Administradores del sistema'
            )
        else:
            grupo_admin_id = grupo_admin.id
        
        # Asignar rol de administrador
        auth.add_membership('administrador', primer_usuario.id)
        
        db.commit()
        return True, f"Administrador creado: {primer_usuario.email} / contraseña: admin123"
        
    except Exception as e:
        db.rollback()
        return False, f"Error al crear administrador: {str(e)}"

# =========================================================================
# MÓDULO DE REMESAS Y LÍMITES DIARIOS
# Gestión de liquidez y control de ventas de divisas
# =========================================================================

# Tabla de Remesas Diarias
# Registra las remesas recibidas cada día por moneda
db.define_table('remesas_diarias',
    Field('fecha', 'date', notnull=True, default=request.now.date()),
    Field('moneda', 'string', length=10, notnull=True),  # USD, EUR, USDT
    Field('monto_recibido', 'decimal(15,2)', notnull=True, default=0),
    Field('monto_disponible', 'decimal(15,2)', notnull=True, default=0),
    Field('monto_vendido', 'decimal(15,2)', notnull=True, default=0),
    Field('monto_reservado', 'decimal(15,2)', notnull=True, default=0),
    Field('fuente_remesa', 'string', length=100),  # Banco corresponsal, etc.
    Field('numero_referencia', 'string', length=50),
    Field('observaciones', 'text'),
    Field('usuario_registro', 'reference auth_user'),
    Field('fecha_registro', 'datetime', default=request.now),
    Field('activa', 'boolean', default=True),
    format='%(fecha)s - %(moneda)s',
    migrate=False
)

# Validaciones
db.remesas_diarias.moneda.requires = IS_IN_SET(['USD', 'EUR', 'USDT'], 
                                                error_message='Moneda debe ser USD, EUR o USDT')
db.remesas_diarias.monto_recibido.requires = IS_DECIMAL_IN_RANGE(0, 999999999.99, 
                                                                  error_message='Monto inválido')
db.remesas_diarias.fecha.requires = IS_DATE(format='%Y-%m-%d')

# Tabla de Límites de Venta Diarios
# Define los límites máximos de venta por moneda y día
db.define_table('limites_venta',
    Field('fecha', 'date', notnull=True, default=request.now.date()),
    Field('moneda', 'string', length=10, notnull=True),
    Field('limite_diario', 'decimal(15,2)', notnull=True, default=0),
    Field('monto_vendido', 'decimal(15,2)', notnull=True, default=0),
    Field('monto_disponible', 'decimal(15,2)', notnull=True, default=0),
    Field('porcentaje_utilizado', 'decimal(5,2)', compute=lambda r: 
          (r['monto_vendido'] / r['limite_diario'] * 100) if r['limite_diario'] > 0 else 0),
    Field('alerta_80_enviada', 'boolean', default=False),
    Field('alerta_95_enviada', 'boolean', default=False),
    Field('usuario_configuracion', 'reference auth_user'),
    Field('fecha_configuracion', 'datetime', default=request.now),
    Field('activo', 'boolean', default=True),
    format='%(fecha)s - %(moneda)s',
    migrate=False
)

# Validaciones
db.limites_venta.moneda.requires = IS_IN_SET(['USD', 'EUR', 'USDT'])
db.limites_venta.limite_diario.requires = IS_DECIMAL_IN_RANGE(0, 999999999.99)

# Tabla de Historial de Movimientos de Remesas
# Auditoría completa de todos los movimientos
db.define_table('movimientos_remesas',
    Field('remesa_id', 'reference remesas_diarias', notnull=True),
    Field('tipo_movimiento', 'string', length=20, notnull=True),  # RECEPCION, VENTA, AJUSTE, DEVOLUCION
    Field('monto', 'decimal(15,2)', notnull=True),
    Field('saldo_anterior', 'decimal(15,2)', notnull=True),
    Field('saldo_nuevo', 'decimal(15,2)', notnull=True),
    Field('transaccion_id', 'reference transacciones'),  # Si está relacionado con una venta
    Field('descripcion', 'text'),
    Field('usuario', 'reference auth_user'),
    Field('fecha_movimiento', 'datetime', default=request.now),
    Field('ip_address', 'string', length=50),
    format='%(tipo_movimiento)s - %(monto)s',
    migrate=False
)

# Validaciones
db.movimientos_remesas.tipo_movimiento.requires = IS_IN_SET(
    ['RECEPCION', 'VENTA', 'AJUSTE', 'DEVOLUCION', 'RESERVA', 'LIBERACION'],
    error_message='Tipo de movimiento inválido'
)

# Tabla de Configuración de Alertas
# Configuración de notificaciones cuando se alcanzan umbrales
db.define_table('alertas_limites',
    Field('tipo_alerta', 'string', length=20, notnull=True),  # LIMITE_80, LIMITE_95, LIMITE_100
    Field('moneda', 'string', length=10, notnull=True),
    Field('umbral_porcentaje', 'decimal(5,2)', notnull=True),
    Field('mensaje_alerta', 'text'),
    Field('enviar_email', 'boolean', default=True),
    Field('emails_destino', 'list:string'),
    Field('activa', 'boolean', default=True),
    Field('fecha_creacion', 'datetime', default=request.now),
    format='%(tipo_alerta)s - %(moneda)s',
    migrate=False
)


# =========================================================================
# FUNCIONES DE VALIDACIÓN DE LÍMITES PARA VENTAS
# Integración del módulo de remesas con el sistema de ventas
# =========================================================================

def validar_limite_venta(moneda, monto_venta, fecha=None):
    """
    Valida si una venta puede realizarse sin exceder límites
    
    Args:
        moneda (str): USD, EUR, USDT
        monto_venta (float): Monto a vender
        fecha (date): Fecha de la venta (default: hoy)
    
    Returns:
        dict: {
            'puede_vender': bool,
            'razon': str,
            'limite_disponible': float,
            'remesa_disponible': float
        }
    """
    if not fecha:
        fecha = request.now.date()
    
    try:
        # Obtener límite del día
        limite = db(
            (db.limites_venta.fecha == fecha) &
            (db.limites_venta.moneda == moneda) &
            (db.limites_venta.activo == True)
        ).select().first()
        
        # Obtener remesa del día
        remesa = db(
            (db.remesas_diarias.fecha == fecha) &
            (db.remesas_diarias.moneda == moneda) &
            (db.remesas_diarias.activa == True)
        ).select().first()
        
        resultado = {
            'puede_vender': False,
            'razon': '',
            'limite_disponible': 0,
            'remesa_disponible': 0,
            'limite_diario': 0,
            'limite_utilizado': 0
        }
        
        # Verificar si existe límite
        if not limite:
            resultado['razon'] = f'No hay límite configurado para {moneda} en {fecha}'
            return resultado
        
        # Verificar si existe remesa
        if not remesa:
            resultado['razon'] = f'No hay remesa disponible para {moneda} en {fecha}'
            return resultado
        
        # Obtener valores actuales
        limite_disponible = float(limite.monto_disponible)
        remesa_disponible = float(remesa.monto_disponible)
        limite_diario = float(limite.limite_diario)
        limite_utilizado = float(limite.monto_vendido)
        
        resultado.update({
            'limite_disponible': limite_disponible,
            'remesa_disponible': remesa_disponible,
            'limite_diario': limite_diario,
            'limite_utilizado': limite_utilizado
        })
        
        # Validar límite diario
        if monto_venta > limite_disponible:
            resultado['razon'] = f'Venta de ${monto_venta:,.2f} excede límite disponible de ${limite_disponible:,.2f}'
            return resultado
        
        # Validar remesa disponible
        if monto_venta > remesa_disponible:
            resultado['razon'] = f'Venta de ${monto_venta:,.2f} excede remesa disponible de ${remesa_disponible:,.2f}'
            return resultado
        
        # Si pasa todas las validaciones
        resultado['puede_vender'] = True
        resultado['razon'] = 'Venta autorizada'
        
        return resultado
        
    except Exception as e:
        logger.error(f"Error validando límite de venta: {str(e)}")
        return {
            'puede_vender': False,
            'razon': f'Error del sistema: {str(e)}',
            'limite_disponible': 0,
            'remesa_disponible': 0
        }

def procesar_venta_con_limites(moneda, monto_venta, transaccion_id=None, fecha=None):
    """
    Procesa una venta actualizando límites y remesas
    
    Args:
        moneda (str): USD, EUR, USDT
        monto_venta (float): Monto vendido
        transaccion_id (int): ID de la transacción
        fecha (date): Fecha de la venta
    
    Returns:
        dict: {'success': bool, 'mensaje': str}
    """
    if not fecha:
        fecha = request.now.date()
    
    try:
        # Validar antes de procesar
        validacion = validar_limite_venta(moneda, monto_venta, fecha)
        
        if not validacion['puede_vender']:
            return {
                'success': False,
                'mensaje': validacion['razon']
            }
        
        # Obtener registros
        limite = db(
            (db.limites_venta.fecha == fecha) &
            (db.limites_venta.moneda == moneda) &
            (db.limites_venta.activo == True)
        ).select().first()
        
        remesa = db(
            (db.remesas_diarias.fecha == fecha) &
            (db.remesas_diarias.moneda == moneda) &
            (db.remesas_diarias.activa == True)
        ).select().first()
        
        # Actualizar límite
        nuevo_vendido_limite = float(limite.monto_vendido) + monto_venta
        nuevo_disponible_limite = float(limite.limite_diario) - nuevo_vendido_limite
        nuevo_porcentaje = (nuevo_vendido_limite / float(limite.limite_diario)) * 100
        
        limite.update_record(
            monto_vendido=nuevo_vendido_limite,
            monto_disponible=nuevo_disponible_limite,
            porcentaje_utilizado=nuevo_porcentaje
        )
        
        # Actualizar remesa
        nuevo_vendido_remesa = float(remesa.monto_vendido) + monto_venta
        nuevo_disponible_remesa = float(remesa.monto_disponible) - monto_venta
        
        remesa.update_record(
            monto_vendido=nuevo_vendido_remesa,
            monto_disponible=nuevo_disponible_remesa
        )
        
        # Registrar movimiento
        db.movimientos_remesas.insert(
            remesa_id=remesa.id,
            tipo_movimiento='VENTA',
            monto=monto_venta,
            saldo_anterior=float(remesa.monto_disponible) + monto_venta,
            saldo_nuevo=nuevo_disponible_remesa,
            transaccion_id=transaccion_id,
            descripcion=f'Venta de {moneda} por ${monto_venta:,.2f}',
            usuario=auth.user_id if auth.user else None,
            ip_address=request.client
        )
        
        # Verificar alertas
        if nuevo_porcentaje >= 80 and not limite.alerta_80_enviada:
            enviar_alerta_limite(moneda, 80, nuevo_porcentaje)
            limite.update_record(alerta_80_enviada=True)
        
        if nuevo_porcentaje >= 95 and not limite.alerta_95_enviada:
            enviar_alerta_limite(moneda, 95, nuevo_porcentaje)
            limite.update_record(alerta_95_enviada=True)
        
        db.commit()
        
        return {
            'success': True,
            'mensaje': f'Venta procesada. Límite utilizado: {nuevo_porcentaje:.1f}%'
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error procesando venta con límites: {str(e)}")
        return {
            'success': False,
            'mensaje': f'Error procesando venta: {str(e)}'
        }

def enviar_alerta_limite(moneda, umbral, porcentaje_actual):
    """
    Envía alerta cuando se alcanza un umbral de límite
    """
    mensaje = f"ALERTA: Límite de {moneda} al {porcentaje_actual:.1f}% (umbral {umbral}%)"
    logger.warning(mensaje)
    
    # Aquí se puede implementar envío de email
    # mail.send(
    #     to=['admin@banco.com'],
    #     subject=f'Alerta de Límite - {moneda}',
    #     message=mensaje
    # )
