# -*- coding: utf-8 -*-
"""
Controlador de Gestión de Clientes
Sistema de Divisas Bancario
"""

import re
import logging
import uuid
from datetime import datetime
from gluon.storage import Storage

# Configurar logger
logger = logging.getLogger("web2py.app.clientes")

# -------------------------------------------------------------------------
# Funciones de utilidad para validación y manejo de errores
# -------------------------------------------------------------------------

def log_error(function_name, error, user_id=None, additional_info=None):
    """
    Función centralizada para logging de errores
    Requisitos: 5.1, 5.2
    """
    import logging
    import traceback
    
    logger = logging.getLogger("web2py.app.clientes")
    
    error_msg = f"Error en {function_name}: {str(error)}"
    if user_id:
        error_msg += f" - Usuario: {user_id}"
    if additional_info:
        error_msg += f" - Info adicional: {additional_info}"
    
    logger.error(error_msg)
    logger.error(f"Traceback: {traceback.format_exc()}")

def log_security_event(event_type, user_id, details, ip_address=None):
    """
    Registra eventos de seguridad para auditoría
    Requisitos: 7.2
    """
    import logging
    
    logger = logging.getLogger("web2py.app.security")
    
    if not ip_address:
        ip_address = request.env.remote_addr or 'unknown'
    
    security_msg = f"SECURITY EVENT - {event_type}: Usuario {user_id} desde IP {ip_address} - {details}"
    logger.warning(security_msg)
    
    # También registrar en la tabla de auditoría si existe
    try:
        if hasattr(db, 'logs_auditoria'):
            db.logs_auditoria.insert(
                usuario_id=user_id,
                accion=f"SECURITY_{event_type}",
                tabla_afectada='security',
                detalles=details,
                ip_address=ip_address,
                fecha=datetime.now()
            )
            db.commit()
    except Exception as e:
        # No fallar si no se puede registrar en auditoría
        logger.error(f"Error registrando evento de seguridad en auditoría: {str(e)}")

def handle_database_error(error, operation="operación de base de datos"):
    """
    Maneja errores específicos de base de datos
    Requisitos: 5.1, 5.3
    """
    error_str = str(error).lower()
    
    if "unique constraint" in error_str or "duplicate" in error_str:
        return "Este registro ya existe en el sistema."
    elif "foreign key" in error_str:
        return "Error de integridad de datos. Verifique las referencias."
    elif "not null" in error_str:
        return "Faltan campos obligatorios."
    elif "database is locked" in error_str:
        return "La base de datos está temporalmente ocupada. Intente nuevamente."
    elif "no such table" in error_str:
        return "Error de configuración del sistema. Contacte al administrador."
    else:
        return f"Error en {operation}. Intente nuevamente o contacte al soporte técnico."

def validate_client_access(cliente_id, user_id, user_roles):
    """
    Valida que el usuario tenga acceso al cliente solicitado
    Requisitos: 1.1, 7.1
    """
    # Validar parámetros de entrada
    if not cliente_id or not user_id:
        return False, "Parámetros de acceso inválidos."
    
    try:
        cliente_id = int(cliente_id)
    except (ValueError, TypeError):
        return False, "ID de cliente inválido."
    
    # Administradores y operadores pueden ver cualquier cliente
    if 'administrador' in user_roles or 'operador' in user_roles:
        # Verificar que el cliente existe
        cliente = db(db.clientes.id == cliente_id).select().first()
        if not cliente:
            return False, "Cliente no encontrado."
        return True, None
    
    # Clientes solo pueden ver su propio perfil
    if 'cliente' in user_roles:
        cliente = db(db.clientes.id == cliente_id).select().first()
        if cliente and cliente.user_id == user_id:
            return True, None
        else:
            return False, "No tiene permisos para ver este cliente."
    
    return False, "No tiene permisos suficientes."

def validate_account_access(cuenta_id, user_id, user_roles):
    """
    Valida que el usuario tenga acceso a la cuenta solicitada
    Requisitos: 2.1, 7.1
    """
    # Validar parámetros de entrada
    if not cuenta_id or not user_id:
        return False, "Parámetros de acceso inválidos."
    
    try:
        cuenta_id = int(cuenta_id)
    except (ValueError, TypeError):
        return False, "ID de cuenta inválido."
    
    # Administradores pueden ver cualquier cuenta
    if 'administrador' in user_roles:
        cuenta = db(db.cuentas.id == cuenta_id).select().first()
        if not cuenta:
            return False, "Cuenta no encontrada."
        return True, None
    
    # Operadores pueden ver cuentas pero con restricciones
    if 'operador' in user_roles:
        cuenta = db(db.cuentas.id == cuenta_id).select().first()
        if not cuenta:
            return False, "Cuenta no encontrada."
        return True, None
    
    # Clientes solo pueden ver sus propias cuentas
    if 'cliente' in user_roles:
        cuenta = db((db.cuentas.id == cuenta_id) & 
                   (db.cuentas.cliente_id == db.clientes.id) &
                   (db.clientes.user_id == user_id)).select().first()
        if cuenta:
            return True, None
        else:
            return False, "No tiene permisos para ver esta cuenta."
    
    return False, "No tiene permisos suficientes."

def get_user_roles(user_id=None):
    """
    Obtiene los roles del usuario de forma segura
    Requisitos: 7.1
    """
    if not user_id:
        user_id = auth.user_id
    
    if not user_id:
        return []
    
    try:
        if hasattr(auth, 'user_groups') and auth.user_groups:
            # Si user_groups contiene objetos con atributo role
            first_value = list(auth.user_groups.values())[0] if auth.user_groups.values() else None
            if first_value and hasattr(first_value, 'role'):
                return [g.role for g in auth.user_groups.values()]
            else:
                # Si user_groups contiene strings directamente
                return list(auth.user_groups.values())
        else:
            # Método alternativo: consultar directamente la base de datos
            user_groups = db((db.auth_membership.user_id == user_id) & 
                           (db.auth_membership.group_id == db.auth_group.id)).select(db.auth_group.role)
            return [g.role for g in user_groups]
    except Exception as e:
        # Si hay error, asumir que no tiene roles
        return []

def validate_user_permissions(required_roles, user_id=None):
    """
    Valida que el usuario tenga uno de los roles requeridos
    Requisitos: 7.1
    """
    if not user_id:
        user_id = auth.user_id
    
    if not user_id or not auth.is_logged_in():
        return False, "Debe iniciar sesión para acceder."
    
    user_roles = get_user_roles(user_id)
    
    # Verificar si el usuario tiene al menos uno de los roles requeridos
    if any(role in user_roles for role in required_roles):
        return True, None
    
    return False, f"Requiere uno de los siguientes roles: {', '.join(required_roles)}"

def sanitize_search_input(input_value, max_length=100, allow_special_chars=False):
    """
    Sanitiza entradas de búsqueda para prevenir inyección SQL y XSS
    Requisitos: 3.1, 3.2, 7.2
    """
    if not input_value:
        return ''
    
    # Convertir a string y limpiar espacios
    input_str = str(input_value).strip()
    
    # Limitar longitud
    if len(input_str) > max_length:
        input_str = input_str[:max_length]
    
    # Escapar caracteres HTML para prevenir XSS
    import html
    input_str = html.escape(input_str)
    
    if not allow_special_chars:
        # Remover caracteres potencialmente peligrosos para SQL
        dangerous_chars = ['\'', '"', ';', '--', '/*', '*/', 'xp_', 'sp_', 'DROP', 'DELETE', 'INSERT', 'UPDATE', 'UNION', 'SELECT']
        for char in dangerous_chars:
            input_str = input_str.replace(char, '')
    
    # Validar que no contenga solo espacios después de la limpieza
    if not input_str.strip():
        return ''
    
    return input_str

def sanitize_email_input(email_input):
    """
    Sanitiza entrada de email con validación específica
    Requisitos: 7.2
    """
    if not email_input:
        return ''
    
    email_str = str(email_input).strip().lower()
    
    # Limitar longitud de email
    if len(email_str) > 100:
        email_str = email_str[:100]
    
    # Escapar HTML
    import html
    email_str = html.escape(email_str)
    
    # Validar formato básico de email (sin usar regex complejo)
    if '@' not in email_str or '.' not in email_str:
        return ''
    
    # Remover caracteres peligrosos específicos para email
    dangerous_chars = ['\'', '"', ';', '--', '/*', '*/', '<', '>', 'script']
    for char in dangerous_chars:
        if char in email_str:
            return ''
    
    return email_str

def sanitize_cedula_input(cedula_input):
    """
    Sanitiza entrada de cédula venezolana
    Requisitos: 7.2
    """
    if not cedula_input:
        return ''
    
    cedula_str = str(cedula_input).strip().upper()
    
    # Limitar longitud
    if len(cedula_str) > 20:
        cedula_str = cedula_str[:20]
    
    # Escapar HTML
    import html
    cedula_str = html.escape(cedula_str)
    
    # Solo permitir formato de cédula venezolana: V-12345678 o E-12345678
    import re
    if not re.match(r'^[VE]-?\d{7,8}$', cedula_str):
        # Si no coincide con el formato, limpiar caracteres no válidos
        cedula_clean = re.sub(r'[^VE0-9-]', '', cedula_str)
        if len(cedula_clean) < 8:  # Mínimo V-1234567
            return ''
        cedula_str = cedula_clean
    
    return cedula_str

def sanitize_date_input(date_input):
    """
    Sanitiza entrada de fecha
    Requisitos: 7.2
    """
    if not date_input:
        return ''
    
    date_str = str(date_input).strip()
    
    # Escapar HTML
    import html
    date_str = html.escape(date_str)
    
    # Validar formato de fecha YYYY-MM-DD
    import re
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return ''
    
    # Validar que sea una fecha válida
    try:
        from datetime import datetime
        datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        return ''

def validate_search_parameters(params):
    """
    Valida y sanitiza todos los parámetros de búsqueda
    Requisitos: 3.1, 3.2, 7.2
    """
    sanitized_params = {}
    security_issues = []
    
    # Sanitizar búsqueda general
    if 'buscar' in params:
        original_value = params['buscar']
        sanitized_value = sanitize_search_input(original_value, max_length=100)
        sanitized_params['buscar'] = sanitized_value
        
        # Detectar intentos de inyección
        if original_value and original_value != sanitized_value:
            security_issues.append(f"Búsqueda sanitizada: '{original_value}' -> '{sanitized_value}'")
    
    # Sanitizar cédula
    if 'cedula' in params:
        original_value = params['cedula']
        sanitized_value = sanitize_cedula_input(original_value)
        sanitized_params['cedula'] = sanitized_value
        
        if original_value and original_value != sanitized_value:
            security_issues.append(f"Cédula sanitizada: '{original_value}' -> '{sanitized_value}'")
    
    # Sanitizar email
    if 'email' in params:
        original_value = params['email']
        sanitized_value = sanitize_email_input(original_value)
        sanitized_params['email'] = sanitized_value
        
        if original_value and original_value != sanitized_value:
            security_issues.append(f"Email sanitizado: '{original_value}' -> '{sanitized_value}'")
    
    # Sanitizar estado (lista cerrada de valores)
    if 'estado' in params:
        estado = str(params['estado']).strip().lower()
        if estado in ['todos', 'activo', 'inactivo']:
            sanitized_params['estado'] = estado
        else:
            sanitized_params['estado'] = 'todos'
            if params['estado'] != 'todos':
                security_issues.append(f"Estado inválido rechazado: '{params['estado']}'")
    
    # Sanitizar fechas
    if 'fecha_desde' in params:
        original_value = params['fecha_desde']
        sanitized_value = sanitize_date_input(original_value)
        sanitized_params['fecha_desde'] = sanitized_value
        
        if original_value and original_value != sanitized_value:
            security_issues.append(f"Fecha desde sanitizada: '{original_value}' -> '{sanitized_value}'")
    
    if 'fecha_hasta' in params:
        original_value = params['fecha_hasta']
        sanitized_value = sanitize_date_input(original_value)
        sanitized_params['fecha_hasta'] = sanitized_value
        
        if original_value and original_value != sanitized_value:
            security_issues.append(f"Fecha hasta sanitizada: '{original_value}' -> '{sanitized_value}'")
    
    # Sanitizar página (solo números)
    if 'page' in params:
        try:
            page = int(params['page'])
            if page < 1:
                page = 1
            sanitized_params['page'] = page
        except (ValueError, TypeError):
            sanitized_params['page'] = 1
            security_issues.append(f"Página inválida rechazada: '{params['page']}'")
    
    # Registrar eventos de seguridad si se detectaron problemas
    if security_issues and auth.user:
        log_security_event(
            'INPUT_SANITIZATION',
            auth.user.id,
            f"Parámetros sanitizados en búsqueda de clientes: {'; '.join(security_issues)}"
        )
    
    return sanitized_params

def optimize_database_indexes():
    """
    Crea índices para optimizar consultas frecuentes
    Requisitos: 4.1
    """
    try:
        # Verificar si los índices ya existen antes de crearlos
        if hasattr(db, '_adapter') and hasattr(db._adapter, 'execute'):
            # Índices para búsquedas frecuentes en clientes
            try:
                db.executesql("CREATE INDEX IF NOT EXISTS idx_clientes_cedula ON clientes(cedula);")
                db.executesql("CREATE INDEX IF NOT EXISTS idx_clientes_user_id ON clientes(user_id);")
                db.executesql("CREATE INDEX IF NOT EXISTS idx_clientes_fecha_registro ON clientes(fecha_registro);")
            except:
                pass  # Los índices pueden ya existir
            
            # Índices para auth_user
            try:
                db.executesql("CREATE INDEX IF NOT EXISTS idx_auth_user_email ON auth_user(email);")
                db.executesql("CREATE INDEX IF NOT EXISTS idx_auth_user_estado ON auth_user(estado);")
                db.executesql("CREATE INDEX IF NOT EXISTS idx_auth_user_names ON auth_user(first_name, last_name);")
            except:
                pass
            
            # Índices para cuentas
            try:
                db.executesql("CREATE INDEX IF NOT EXISTS idx_cuentas_cliente_id ON cuentas(cliente_id);")
                db.executesql("CREATE INDEX IF NOT EXISTS idx_cuentas_numero ON cuentas(numero_cuenta);")
                db.executesql("CREATE INDEX IF NOT EXISTS idx_cuentas_estado ON cuentas(estado);")
            except:
                pass
            
            # Índices para transacciones
            try:
                db.executesql("CREATE INDEX IF NOT EXISTS idx_transacciones_cuenta_id ON transacciones(cuenta_id);")
                db.executesql("CREATE INDEX IF NOT EXISTS idx_transacciones_fecha ON transacciones(fecha_transaccion);")
                db.executesql("CREATE INDEX IF NOT EXISTS idx_transacciones_estado ON transacciones(estado);")
            except:
                pass
                
        return True
    except Exception as e:
        log_error("optimize_database_indexes", str(e))
        return False

def get_optimized_client_query(filters=None):
    """
    Construye una consulta optimizada para clientes con filtros avanzados
    Requisitos: 3.1, 3.4
    """
    # Query base optimizada con JOIN explícito
    query = (db.clientes.user_id == db.auth_user.id)
    
    if filters:
        # Aplicar filtros de forma optimizada
        if filters.get('buscar'):
            search_term = filters['buscar']
            # Usar índices en nombres y email para búsqueda general
            search_query = (
                (db.auth_user.first_name.contains(search_term)) |
                (db.auth_user.last_name.contains(search_term)) |
                (db.auth_user.email.contains(search_term)) |
                (db.clientes.cedula.contains(search_term))
            )
            query &= search_query
        
        if filters.get('cedula'):
            # Usar índice en cédula para búsqueda específica
            query &= (db.clientes.cedula.contains(filters['cedula']))
        
        if filters.get('email'):
            # Búsqueda específica por email
            query &= (db.auth_user.email.contains(filters['email']))
        
        if filters.get('estado') and filters['estado'] != 'todos':
            # Usar índice en estado
            query &= (db.auth_user.estado == filters['estado'])
        
        # Filtros por rango de fechas de registro
        if filters.get('fecha_desde'):
            try:
                from datetime import datetime
                fecha_desde_dt = datetime.strptime(filters['fecha_desde'], '%Y-%m-%d').date()
                query &= (db.clientes.fecha_registro >= fecha_desde_dt)
            except (ValueError, TypeError):
                pass  # Ignorar fechas inválidas
        
        if filters.get('fecha_hasta'):
            try:
                from datetime import datetime, timedelta
                fecha_hasta_dt = datetime.strptime(filters['fecha_hasta'], '%Y-%m-%d').date()
                # Incluir todo el día hasta
                fecha_hasta_dt = fecha_hasta_dt + timedelta(days=1)
                query &= (db.clientes.fecha_registro < fecha_hasta_dt)
            except (ValueError, TypeError):
                pass  # Ignorar fechas inválidas
    
    return query

def get_client_statistics_optimized():
    """
    Obtiene estadísticas de clientes de forma optimizada
    Requisitos: 4.1
    """
    try:
        # Usar consultas separadas más eficientes
        total = db(db.clientes.id > 0).count()
        
        # Consulta optimizada para activos/inactivos
        activos = db((db.clientes.user_id == db.auth_user.id) & 
                    (db.auth_user.estado == 'activo')).count()
        
        inactivos = total - activos  # Más eficiente que otra consulta
        
        return {
            'total': total,
            'activos': activos,
            'inactivos': inactivos
        }
    except Exception as e:
        log_error("get_client_statistics_optimized", str(e))
        return {'total': 0, 'activos': 0, 'inactivos': 0}

def validar_cedula(cedula):
    """
    Valida el formato de cédula venezolana
    Formato aceptado: V-12345678 o E-12345678
    """
    if not cedula:
        return False, "La cédula es requerida"
    
    # Limpiar espacios y convertir a mayúsculas
    cedula = cedula.strip().upper()
    
    # Validar formato con regex
    patron = r'^[VE]-?\d{7,8}$'
    if not re.match(patron, cedula):
        return False, "Formato de cédula inválido. Use V-12345678 o E-12345678"
    
    # Verificar que no esté ya registrada
    cliente_existente = db(db.clientes.cedula == cedula).select().first()
    if cliente_existente:
        return False, "Esta cédula ya está registrada en el sistema"
    
    return True, "Cédula válida"

def generar_numero_cuenta():
    """
    Genera un número de cuenta único de 20 dígitos
    """
    import random
    while True:
        # Generar número de cuenta con prefijo 2001 (código del banco)
        numero = "2001" + "".join([str(random.randint(0, 9)) for _ in range(16)])
        
        # Verificar que no exista
        cuenta_existente = db(db.cuentas.numero_cuenta == numero).select().first()
        if not cuenta_existente:
            return numero

# -------------------------------------------------------------------------
# Función de registro de clientes
# -------------------------------------------------------------------------

@auth.requires_login()
# @requiere_permiso('create', 'clientes')  # Temporalmente deshabilitado
def registrar():
    """
    Función de registro de nuevos clientes con validación de cédula
    Requisitos: 2.1, 2.2
    """
    
    # Solo administradores y operadores pueden registrar clientes
    if not (auth.has_membership('administrador') or auth.has_membership('operador')):
        session.flash = "No tiene permisos para registrar clientes"
        redirect(URL('default', 'index'))
    
    # Crear objeto form vacío para evitar errores en la vista
    form = Storage()
    form.errors = Storage()
    
    # Procesar formulario con validaciones básicas
    if request.vars.first_name:  # Si se envió el formulario
        try:
            # Debug: log de los datos recibidos
            import logging
            logger = logging.getLogger("web2py.app.clientes")
            logger.info(f"Registrando cliente: {request.vars.first_name} {request.vars.last_name}")
            # Validaciones básicas
            errores = False
            
            # Validar email
            if not request.vars.email:
                form.errors.email = "El email es requerido"
                errores = True
            else:
                usuario_existente = db(db.auth_user.email == request.vars.email).select().first()
                if usuario_existente:
                    form.errors.email = "Este email ya está registrado"
                    errores = True
            
            # Validar cédula
            if request.vars.cedula:
                cedula_existente = db(db.clientes.cedula == request.vars.cedula).select().first()
                if cedula_existente:
                    form.errors.cedula = "Esta cédula ya está registrada"
                    errores = True
            
            # Validar teléfono (opcional pero si se proporciona debe tener formato válido)
            if request.vars.telefono and len(request.vars.telefono) < 10:
                form.errors.telefono = "El teléfono debe tener al menos 10 dígitos"
                errores = True
            
            # Validar contraseña
            if not request.vars.password:
                form.errors.password = "La contraseña es requerida"
                errores = True
            elif len(request.vars.password) < 6:
                form.errors.password = "La contraseña debe tener al menos 6 caracteres"
                errores = True
            
            # Validar confirmación de contraseña
            if request.vars.password != request.vars.password_confirm:
                form.errors.password_confirm = "Las contraseñas no coinciden"
                errores = True
            
            # Si hay errores, mostrar el formulario con errores
            if errores:
                response.flash = "Por favor corrija los errores indicados"
                return dict(form=form, registro_exitoso=False)
            
            # Procesar fecha de nacimiento
            fecha_nacimiento = None
            if request.vars.fecha_nacimiento:
                try:
                    from datetime import datetime
                    if isinstance(request.vars.fecha_nacimiento, str):
                        fecha_nacimiento = datetime.strptime(request.vars.fecha_nacimiento, '%Y-%m-%d').date()
                    else:
                        fecha_nacimiento = request.vars.fecha_nacimiento
                except:
                    form.errors.fecha_nacimiento = "Formato de fecha inválido"
                    errores = True
            
            if errores:
                response.flash = "Por favor corrija los errores indicados"
                return dict(form=form, registro_exitoso=False)
            
            # Crear usuario aplicando validadores manualmente para asegurar hash correcto
            from gluon.validators import CRYPT
            
            # Aplicar validador CRYPT manualmente
            password_validator = CRYPT()
            validated_password, error = password_validator(request.vars.password)
            
            if error:
                form.errors.password = "Error al procesar contraseña"
                return dict(form=form, registro_exitoso=False)
            
            user_id = db.auth_user.insert(
                first_name=request.vars.first_name,
                last_name=request.vars.last_name,
                email=request.vars.email,
                password=validated_password,  # Contraseña correctamente hasheada
                telefono=request.vars.telefono or '',
                direccion=request.vars.direccion or '',
                fecha_nacimiento=fecha_nacimiento,
                estado='activo'
            )
            
            # Crear registro en tabla clientes
            cliente_id = db.clientes.insert(
                user_id=user_id,
                cedula=request.vars.cedula or '',
                fecha_registro=datetime.now()
            )
            
            # Asignar rol de cliente
            # Verificar que el grupo 'cliente' existe
            grupo_cliente = db(db.auth_group.role == 'cliente').select().first()
            if grupo_cliente:
                auth.add_membership(grupo_cliente.id, user_id)
            else:
                # Crear el grupo si no existe
                grupo_cliente_id = db.auth_group.insert(role='cliente', description='Clientes del banco')
                auth.add_membership(grupo_cliente_id, user_id)
            
            # Crear cuenta bancaria inicial
            numero_cuenta = generar_numero_cuenta()
            db.cuentas.insert(
                cliente_id=cliente_id,
                numero_cuenta=numero_cuenta,
                tipo_cuenta='corriente',
                saldo_ves=0,
                saldo_usd=0,
                saldo_eur=0,
                estado='activa'
            )
            
            db.commit()
            
            # TODO: Registrar en log de auditoría cuando esté implementada
            # log_auditoria(...)
            
            # Registro exitoso - usar response.flash en lugar de session.flash
            response.flash = f"✅ Cliente registrado exitosamente. Número de cuenta: {numero_cuenta}"
            
            # Limpiar el formulario para mostrar el mensaje de éxito
            form = Storage()
            form.errors = Storage()
            
            return dict(form=form, registro_exitoso=True, numero_cuenta=numero_cuenta)
            
        except Exception as e:
            db.rollback()
            
            # Log del error con detalles
            log_error("registrar", str(e), auth.user.id, 
                     f"email={request.vars.email}, cedula={request.vars.cedula}")
            
            # Mostrar error específico basado en el tipo de error
            error_message = handle_database_error(e, "registro de cliente")
            form.errors.general = error_message
            
            response.flash = "❌ Error al registrar el cliente. Revise los detalles del error."
            return dict(form=form, registro_exitoso=False)
    
    return dict(form=form, registro_exitoso=False)

# -------------------------------------------------------------------------
# Función de gestión de perfil de cliente
# -------------------------------------------------------------------------

@auth.requires_login()
@requiere_permiso('update', 'clientes')
def perfil():
    """
    Función de gestión de perfil de cliente
    Requisitos: 2.2
    """
    
    # Obtener información del cliente actual
    if auth.has_membership('cliente'):
        # Cliente puede ver/editar solo su propio perfil
        cliente = db(db.clientes.user_id == auth.user.id).select().first()
        if cliente:
            usuario = db(db.auth_user.id == cliente.user_id).select().first()
        else:
            usuario = None
    else:
        # Administradores y operadores pueden ver perfil específico
        cliente_id = request.args(0)
        if not cliente_id:
            session.flash = "ID de cliente requerido"
            redirect(URL('clientes', 'listar'))
        
        cliente = db(db.clientes.id == cliente_id).select().first()
        if cliente:
            usuario = db(db.auth_user.id == cliente.user_id).select().first()
        else:
            usuario = None
    
    if not cliente or not usuario:
        session.flash = "Cliente no encontrado"
        redirect(URL('default', 'index'))
    
    # Crear formulario de edición
    form = SQLFORM.factory(
        Field('first_name', 'string', label='Nombres', 
              default=usuario.first_name, requires=IS_NOT_EMPTY()),
        Field('last_name', 'string', label='Apellidos', 
              default=usuario.last_name, requires=IS_NOT_EMPTY()),
        Field('email', 'string', label='Email', 
              default=usuario.email, requires=[IS_NOT_EMPTY(), IS_EMAIL()]),
        Field('telefono', 'string', label='Teléfono', 
              default=usuario.telefono if hasattr(usuario, 'telefono') else '', requires=IS_NOT_EMPTY()),
        Field('direccion', 'text', label='Dirección', 
              default=usuario.direccion if hasattr(usuario, 'direccion') else '', requires=IS_NOT_EMPTY()),
        Field('fecha_nacimiento', 'date', label='Fecha de Nacimiento', 
              default=usuario.fecha_nacimiento if hasattr(usuario, 'fecha_nacimiento') else None, requires=IS_DATE()),
        Field('cedula', 'string', label='Cédula', 
              default=cliente.cedula, writable=False),
        submit_button='Actualizar Perfil',
        formstyle='bootstrap4_inline'
    )
    
    if form.process().accepted:
        try:
            # Verificar que el email no esté usado por otro usuario
            usuario_existente = db((db.auth_user.email == form.vars.email) & 
                                 (db.auth_user.id != usuario.id)).select().first()
            if usuario_existente:
                form.errors.email = "Este email ya está registrado por otro usuario"
                response.flash = "Error en la validación de datos"
                return dict(form=form, cliente=cliente, usuario=usuario)
            
            # Actualizar datos del usuario
            db(db.auth_user.id == usuario.id).update(
                first_name=form.vars.first_name,
                last_name=form.vars.last_name,
                email=form.vars.email,
                telefono=form.vars.telefono,
                direccion=form.vars.direccion,
                fecha_nacimiento=form.vars.fecha_nacimiento
            )
            
            db.commit()
            session.flash = "Perfil actualizado exitosamente"
            
            # Redirigir según el rol
            if auth.has_membership('cliente'):
                redirect(URL('default', 'index'))
            else:
                redirect(URL('clientes', 'listar'))
                
        except Exception as e:
            db.rollback()
            response.flash = f"Error al actualizar perfil: {str(e)}"
            
    elif form.errors:
        response.flash = "Por favor corrija los errores en el formulario"
    
    # Obtener cuentas del cliente
    cuentas = db(db.cuentas.cliente_id == cliente.id).select()
    
    return dict(form=form, cliente=cliente, usuario=usuario, cuentas=cuentas)

@auth.requires_login()
@requiere_rol('administrador', 'operador')
def editar():
    """
    Función de edición de clientes para administradores
    Permite editar todos los datos del cliente incluyendo estado
    """
    
    cliente_id = request.args(0)
    if not cliente_id:
        session.flash = "ID de cliente requerido"
        redirect(URL('clientes', 'listar'))
    
    try:
        cliente_id = int(cliente_id)
    except ValueError:
        session.flash = "ID de cliente inválido"
        redirect(URL('clientes', 'listar'))
    
    # Obtener cliente y usuario
    cliente = db(db.clientes.id == cliente_id).select().first()
    if not cliente:
        session.flash = "Cliente no encontrado"
        redirect(URL('clientes', 'listar'))
    
    usuario = db(db.auth_user.id == cliente.user_id).select().first()
    if not usuario:
        session.flash = "Usuario no encontrado"
        redirect(URL('clientes', 'listar'))
    
    # Crear formulario de edición administrativa (SIN campos de contraseña por ahora)
    form = SQLFORM.factory(
        Field('first_name', 'string', label='Nombres', 
              default=usuario.first_name, requires=IS_NOT_EMPTY()),
        Field('last_name', 'string', label='Apellidos', 
              default=usuario.last_name, requires=IS_NOT_EMPTY()),
        Field('email', 'string', label='Email', 
              default=usuario.email, requires=[IS_NOT_EMPTY(), IS_EMAIL()]),
        Field('telefono', 'string', label='Teléfono', 
              default=usuario.telefono or '', requires=IS_NOT_EMPTY()),
        Field('direccion', 'text', label='Dirección', 
              default=usuario.direccion or '', requires=IS_NOT_EMPTY()),
        Field('fecha_nacimiento', 'date', label='Fecha de Nacimiento', 
              default=usuario.fecha_nacimiento, requires=IS_DATE()),
        Field('cedula', 'string', label='Cédula', 
              default=cliente.cedula, requires=IS_NOT_EMPTY()),
        Field('estado', 'string', label='Estado', 
              default=usuario.estado or 'activo',
              requires=IS_IN_SET(['activo', 'inactivo'], zero=None)),
        submit_button='Actualizar Cliente',
        formstyle='bootstrap4_inline'
    )
    
    if form.process().accepted:
        try:
            # Verificar que el email no esté usado por otro usuario
            usuario_existente = db((db.auth_user.email == form.vars.email) & 
                                 (db.auth_user.id != usuario.id)).select().first()
            if usuario_existente:
                session.flash = "Este email ya está registrado por otro usuario"
                redirect(URL('editar', args=[cliente_id]))
            
            # Verificar que la cédula no esté usada por otro cliente
            cliente_existente = db((db.clientes.cedula == form.vars.cedula) & 
                                 (db.clientes.id != cliente.id)).select().first()
            if cliente_existente:
                session.flash = "Esta cédula ya está registrada por otro cliente"
                redirect(URL('editar', args=[cliente_id]))
            
            # Actualizar datos del usuario
            db(db.auth_user.id == usuario.id).update(
                first_name=form.vars.first_name,
                last_name=form.vars.last_name,
                email=form.vars.email,
                telefono=form.vars.telefono,
                direccion=form.vars.direccion,
                fecha_nacimiento=form.vars.fecha_nacimiento,
                estado=form.vars.estado
            )
            
            # Actualizar cédula del cliente
            db(db.clientes.id == cliente.id).update(
                cedula=form.vars.cedula
            )
            
            db.commit()
            
            # TODO: Registrar en auditoría cuando esté implementada la función
            # registrar_auditoria(...)
            
            session.flash = "Cliente actualizado exitosamente"
            redirect(URL('clientes', 'listar'))
                
        except Exception as e:
            db.rollback()
            response.flash = f"Error al actualizar cliente: {str(e)}"
            
    elif form.errors:
        response.flash = "Por favor corrija los errores en el formulario"
    
    # Obtener cuentas del cliente
    cuentas = db(db.cuentas.cliente_id == cliente.id).select()
    
    return dict(form=form, cliente=cliente, usuario=usuario, cuentas=cuentas)

# -------------------------------------------------------------------------
# Función de listado de clientes para administradores
# -------------------------------------------------------------------------

@auth.requires_login()
@requiere_rol('administrador', 'operador')
def listar():
    """
    Función de listado de clientes para administradores
    Requisitos: 1.1, 3.4, 7.1
    """
    
    # Validar permisos de acceso con función mejorada
    has_permission, error_msg = validate_user_permissions(['administrador', 'operador'])
    if not has_permission:
        session.flash = error_msg
        redirect(URL('default', 'index'))
    
    # Log de acceso para auditoría
    import logging
    logger = logging.getLogger("web2py.app.clientes")
    logger.info(f"Acceso a lista de clientes por usuario {auth.user.id} ({auth.user.email})")
    
    try:
        # Sanitizar y validar todos los parámetros de búsqueda
        raw_params = {
            'buscar': request.vars.buscar,
            'cedula': request.vars.cedula,
            'email': request.vars.email,
            'estado': request.vars.estado,
            'fecha_desde': request.vars.fecha_desde,
            'fecha_hasta': request.vars.fecha_hasta,
            'page': request.vars.page
        }
        
        # Aplicar sanitización completa
        sanitized_params = validate_search_parameters(raw_params)
        
        # Extraer parámetros sanitizados
        buscar = sanitized_params.get('buscar', '')
        cedula = sanitized_params.get('cedula', '')
        email = sanitized_params.get('email', '')
        estado_filtro = sanitized_params.get('estado', 'todos')
        fecha_desde = sanitized_params.get('fecha_desde', '')
        fecha_hasta = sanitized_params.get('fecha_hasta', '')
        page = sanitized_params.get('page', 1)
        
        # Optimizar índices de base de datos si es necesario
        optimize_database_indexes()
        
        # Construir query optimizada con filtros avanzados
        filters = {
            'buscar': buscar if buscar else None,
            'cedula': cedula if cedula else None,
            'email': email if email else None,
            'estado': estado_filtro if estado_filtro != 'todos' else None,
            'fecha_desde': fecha_desde if fecha_desde else None,
            'fecha_hasta': fecha_hasta if fecha_hasta else None
        }
        query = get_optimized_client_query(filters)
        
        # La página ya fue validada en la sanitización
            
        items_per_page = 20
        
        # Obtener total de registros que coinciden con los filtros
        total_clientes = db(query).count()
        
        # Validar que la página solicitada existe
        total_pages = max(1, (total_clientes + items_per_page - 1) // items_per_page)
        if page > total_pages:
            page = total_pages
        
        # Obtener clientes con paginación y ordenamiento
        clientes = db(query).select(
            db.clientes.ALL,
            db.auth_user.ALL,
            limitby=((page-1)*items_per_page, page*items_per_page),
            orderby=~db.clientes.fecha_registro  # Más recientes primero
        )
        
        # Obtener estadísticas optimizadas
        stats = get_client_statistics_optimized()
        
        # Log de la operación para auditoría
        import logging
        logger = logging.getLogger("web2py.app.clientes")
        logger.info(f"Lista de clientes consultada por usuario {auth.user.id} - "
                   f"Filtros: buscar='{buscar}', cedula='{cedula}', email='{email}', estado='{estado_filtro}', "
                   f"fecha_desde='{fecha_desde}', fecha_hasta='{fecha_hasta}' - "
                   f"Resultados: {len(clientes)} de {total_clientes}")
        
        return dict(
            clientes=clientes,
            buscar=buscar,
            cedula=cedula,
            email=email,
            estado_filtro=estado_filtro,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            page=page,
            total_pages=total_pages,
            total_clientes=total_clientes,
            stats=stats,
            items_per_page=items_per_page
        )
        
    except Exception as e:
        # Log del error
        import logging
        import traceback
        logger = logging.getLogger("web2py.app.clientes")
        logger.error(f"Error en función listar(): {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Mostrar mensaje de error al usuario
        response.flash = "Error al cargar la lista de clientes. Intente nuevamente."
        
        # Retornar datos vacíos para evitar errores en la vista
        return dict(
            clientes=[],
            buscar='',
            cedula='',
            email='',
            estado_filtro='todos',
            fecha_desde='',
            fecha_hasta='',
            page=1,
            total_pages=0,
            total_clientes=0,
            stats={'total': 0, 'activos': 0, 'inactivos': 0},
            items_per_page=20,
            error_message="No se pudieron cargar los datos de clientes."
        )

# -------------------------------------------------------------------------
# Función para cambiar estado de cliente
# -------------------------------------------------------------------------

@auth.requires_login()
def cambiar_estado():
    """
    Función para activar/desactivar clientes
    Solo para administradores
    """
    
    if not auth.has_membership('administrador'):
        session.flash = "No tiene permisos para cambiar estados de clientes"
        redirect(URL('clientes', 'listar'))
    
    cliente_id = request.args(0)
    nuevo_estado = request.args(1)
    
    if not cliente_id or nuevo_estado not in ['activo', 'inactivo']:
        session.flash = "Parámetros inválidos"
        redirect(URL('clientes', 'listar'))
    
    try:
        # Obtener cliente
        cliente = db((db.clientes.id == cliente_id) & 
                    (db.clientes.user_id == db.auth_user.id)).select().first()
        
        if not cliente:
            session.flash = "Cliente no encontrado"
            redirect(URL('clientes', 'listar'))
        
        # Actualizar estado
        db(db.auth_user.id == cliente.clientes.user_id).update(estado=nuevo_estado)
        
        # También actualizar estado de cuentas si se desactiva
        if nuevo_estado == 'inactivo':
            db(db.cuentas.cliente_id == cliente_id).update(estado='inactiva')
        elif nuevo_estado == 'activo':
            db(db.cuentas.cliente_id == cliente_id).update(estado='activa')
        
        db.commit()
        session.flash = f"Cliente {nuevo_estado} exitosamente"
        
    except Exception as e:
        db.rollback()
        session.flash = f"Error al cambiar estado: {str(e)}"
    
    redirect(URL('clientes', 'listar'))

# -------------------------------------------------------------------------
# Función para ver detalles de cliente
# -------------------------------------------------------------------------

@auth.requires_login()
def detalle():
    """
    Función para ver detalles completos de un cliente
    Requisitos: 1.1, 5.1, 5.2, 5.3
    """
    
    try:
        # Validar permisos
        user_roles = get_user_roles()
        if not (auth.has_membership('administrador') or auth.has_membership('operador')):
            session.flash = "No tiene permisos para ver detalles de clientes"
            redirect(URL('default', 'index'))
        
        # Validar parámetros de entrada
        cliente_id = request.args(0)
        if not cliente_id:
            session.flash = "ID de cliente requerido"
            redirect(URL('clientes', 'listar'))
        
        # Validar que el ID sea numérico
        try:
            cliente_id = int(cliente_id)
        except (ValueError, TypeError):
            session.flash = "ID de cliente inválido"
            redirect(URL('clientes', 'listar'))
        
        # Validar acceso al cliente
        has_access, access_error = validate_client_access(cliente_id, auth.user.id, user_roles)
        if not has_access:
            session.flash = access_error
            redirect(URL('default', 'index'))
        
        # Obtener información completa del cliente
        cliente = db(db.clientes.id == cliente_id).select().first()
        
        if not cliente:
            session.flash = "Cliente no encontrado"
            redirect(URL('clientes', 'listar'))
        
        # Obtener información del usuario asociado
        usuario = db(db.auth_user.id == cliente.user_id).select().first()
        
        if not usuario:
            # Log del problema de integridad de datos
            log_error("detalle", f"Usuario no encontrado para cliente {cliente_id}", 
                     auth.user.id, f"cliente.user_id={cliente.user_id}")
            
            # Crear objeto con valores por defecto
            from gluon.storage import Storage
            usuario = Storage({
                'first_name': 'No disponible',
                'last_name': '',
                'email': 'No disponible',
                'telefono': 'No especificado',
                'direccion': 'No especificada',
                'fecha_nacimiento': None,
                'estado': 'inactivo'
            })
        
        # Obtener cuentas del cliente con consulta optimizada
        cuentas = []
        try:
            # Usar índice en cliente_id para consulta eficiente
            cuentas = db(db.cuentas.cliente_id == cliente_id).select(
                orderby=db.cuentas.fecha_creacion
            )
        except Exception as e:
            log_error("detalle", f"Error al obtener cuentas del cliente {cliente_id}", 
                     auth.user.id, str(e))
            cuentas = []
        
        # Obtener últimas transacciones con consulta optimizada
        ultimas_transacciones = []
        if cuentas:
            try:
                cuenta_ids = [c.id for c in cuentas]
                # Usar índices en cuenta_id y fecha para consulta eficiente
                ultimas_transacciones = db(
                    db.transacciones.cuenta_id.belongs(cuenta_ids)
                ).select(
                    db.transacciones.ALL,
                    orderby=~db.transacciones.fecha_transaccion,
                    limitby=(0, 10)
                )
            except Exception as e:
                log_error("detalle", f"Error al obtener transacciones del cliente {cliente_id}", 
                         auth.user.id, str(e))
                ultimas_transacciones = []
        
        # Preparar datos seguros para la vista
        from gluon.storage import Storage
        datos_seguros = Storage()
        
        try:
            # Procesar datos de forma segura
            first_name = usuario.get('first_name', 'N/A') if usuario else 'N/A'
            last_name = usuario.get('last_name', '') if usuario else ''
            datos_seguros['nombre_completo'] = f"{first_name} {last_name}".strip()
            
            datos_seguros['email'] = usuario.get('email', 'No disponible') if usuario else 'No disponible'
            datos_seguros['telefono'] = usuario.get('telefono', 'No especificado') if usuario else 'No especificado'
            datos_seguros['direccion'] = usuario.get('direccion', 'No especificada') if usuario else 'No especificada'
            
            # Formatear fecha de nacimiento de forma segura
            if usuario and usuario.get('fecha_nacimiento'):
                try:
                    datos_seguros['fecha_nacimiento_str'] = usuario.fecha_nacimiento.strftime('%d/%m/%Y')
                except (AttributeError, ValueError):
                    datos_seguros['fecha_nacimiento_str'] = 'Formato inválido'
            else:
                datos_seguros['fecha_nacimiento_str'] = 'No especificada'
            
            datos_seguros['estado'] = usuario.get('estado', 'inactivo') if usuario else 'inactivo'
            datos_seguros['estado_activo'] = (usuario.get('estado', 'inactivo') == 'activo') if usuario else False
            
        except Exception as e:
            log_error("detalle", f"Error al procesar datos seguros del cliente {cliente_id}", 
                     auth.user.id, str(e))
            
            # Datos mínimos en caso de error
            datos_seguros = Storage({
                'nombre_completo': 'Error al cargar datos',
                'email': 'No disponible',
                'telefono': 'No disponible',
                'direccion': 'No disponible',
                'fecha_nacimiento_str': 'No disponible',
                'estado': 'inactivo',
                'estado_activo': False
            })
        
        # Log de acceso exitoso
        import logging
        logger = logging.getLogger("web2py.app.clientes")
        logger.info(f"Detalle de cliente {cliente_id} consultado por usuario {auth.user.id}")
        
        return dict(
            cliente=cliente,
            usuario=usuario,
            datos_seguros=datos_seguros,
            cuentas=cuentas,
            ultimas_transacciones=ultimas_transacciones
        )
        
    except Exception as e:
        # Log del error general
        log_error("detalle", str(e), auth.user.id, f"cliente_id={request.args(0)}")
        
        # Mostrar mensaje de error y redirigir
        error_message = handle_database_error(e, "consulta de detalles del cliente")
        session.flash = error_message
        redirect(URL('clientes', 'listar'))

@auth.requires_membership('administrador')
def diagnosticar_detalle():
    """
    Función de diagnóstico para verificar la vista de detalle
    """
    cliente_id = request.args(0) or 1  # Usar ID 1 por defecto
    
    try:
        # Obtener cliente
        cliente = db(db.clientes.id == cliente_id).select().first()
        
        if not cliente:
            return dict(
                error=f"Cliente con ID {cliente_id} no encontrado",
                clientes_disponibles=db(db.clientes.id > 0).select()
            )
        
        # Obtener usuario
        usuario = db(db.auth_user.id == cliente.user_id).select().first()
        
        # Obtener cuentas
        cuentas = db(db.cuentas.cliente_id == cliente_id).select()
        
        return dict(
            cliente=cliente,
            usuario=usuario,
            cuentas=cuentas,
            diagnostico={
                'cliente_existe': bool(cliente),
                'usuario_existe': bool(usuario),
                'num_cuentas': len(cuentas),
                'campos_cliente': list(cliente.keys()) if cliente else [],
                'campos_usuario': list(usuario.keys()) if usuario else []
            }
        )
        
    except Exception as e:
        return dict(
            error=str(e),
            cliente_id=cliente_id
        )

@auth.requires_membership('administrador')
def test_detalle():
    """
    Función de prueba rápida para verificar que la vista de detalle funciona
    """
    # Buscar el primer cliente disponible
    cliente = db(db.clientes.id > 0).select().first()
    
    if not cliente:
        return dict(
            mensaje="No hay clientes en el sistema para probar",
            url_crear=URL('clientes', 'registrar')
        )
    
    # Redirigir a la vista de detalle
    redirect(URL('clientes', 'detalle', args=[cliente.id]))

@auth.requires_login()
def detalle_simple():
    """
    Versión simplificada de la vista de detalle de cliente
    Sin problemas de sintaxis complejos
    """
    
    if not (auth.has_membership('administrador') or auth.has_membership('operador')):
        session.flash = "No tiene permisos para ver detalles de clientes"
        redirect(URL('default', 'index'))
    
    cliente_id = request.args(0)
    if not cliente_id:
        session.flash = "ID de cliente requerido"
        redirect(URL('clientes', 'listar'))
    
    # Obtener información completa del cliente
    cliente = db(db.clientes.id == cliente_id).select().first()
    
    if not cliente:
        session.flash = "Cliente no encontrado"
        redirect(URL('clientes', 'listar'))
    
    # Obtener información del usuario asociado
    usuario = db(db.auth_user.id == cliente.user_id).select().first()
    
    if not usuario:
        # Si no se encuentra el usuario, crear un objeto con valores por defecto
        from gluon.storage import Storage
        usuario = Storage({
            'first_name': 'No disponible',
            'last_name': '',
            'email': 'No disponible',
            'telefono': 'No especificado',
            'direccion': 'No especificada',
            'fecha_nacimiento': None,
            'estado': 'inactivo'
        })
    
    # Obtener cuentas del cliente
    cuentas = db(db.cuentas.cliente_id == cliente_id).select()
    
    # Obtener últimas transacciones
    ultimas_transacciones = []
    if cuentas:
        ultimas_transacciones = db(
            db.transacciones.cuenta_id.belongs([c.id for c in cuentas])
        ).select(
            orderby=~db.transacciones.fecha_transaccion,
            limitby=(0, 10)
        )
    
    # Preparar datos seguros para la vista
    from gluon.storage import Storage
    datos_seguros = Storage()
    datos_seguros['nombre_completo'] = f"{usuario.get('first_name', 'N/A')} {usuario.get('last_name', '')}".strip() if usuario else 'No disponible'
    datos_seguros['email'] = usuario.get('email', 'No disponible') if usuario else 'No disponible'
    datos_seguros['telefono'] = usuario.get('telefono', 'No especificado') if usuario else 'No especificado'
    datos_seguros['direccion'] = usuario.get('direccion', 'No especificada') if usuario else 'No especificada'
    datos_seguros['fecha_nacimiento_str'] = usuario.fecha_nacimiento.strftime('%d/%m/%Y') if usuario and usuario.get('fecha_nacimiento') else 'No especificada'
    datos_seguros['estado'] = usuario.get('estado', 'inactivo') if usuario else 'inactivo'
    datos_seguros['estado_activo'] = (usuario.get('estado', 'inactivo') == 'activo') if usuario else False
    
    return dict(
        cliente=cliente,
        usuario=usuario,
        datos_seguros=datos_seguros,
        cuentas=cuentas,
        ultimas_transacciones=ultimas_transacciones
    )

@auth.requires_login()
def detalle_debug():
    """
    Versión de debug para diagnosticar problemas con la vista de detalle
    """
    
    if not (auth.has_membership('administrador') or auth.has_membership('operador')):
        return dict(error="No tiene permisos para ver detalles de clientes")
    
    cliente_id = request.args(0)
    if not cliente_id:
        return dict(error="ID de cliente requerido")
    
    try:
        # Obtener información completa del cliente
        cliente = db(db.clientes.id == cliente_id).select().first()
        
        if not cliente:
            return dict(error=f"Cliente con ID {cliente_id} no encontrado")
        
        # Obtener información del usuario asociado
        usuario = db(db.auth_user.id == cliente.user_id).select().first()
        
        # Obtener cuentas del cliente
        cuentas = db(db.cuentas.cliente_id == cliente_id).select()
        
        # Obtener últimas transacciones
        ultimas_transacciones = []
        if cuentas:
            ultimas_transacciones = db(
                db.transacciones.cuenta_id.belongs([c.id for c in cuentas])
            ).select(
                orderby=~db.transacciones.fecha_transaccion,
                limitby=(0, 10)
            )
        
        # Preparar datos seguros para la vista
        from gluon.storage import Storage
        datos_seguros = Storage()
        datos_seguros['nombre_completo'] = f"{usuario.get('first_name', 'N/A')} {usuario.get('last_name', '')}".strip() if usuario else 'No disponible'
        datos_seguros['email'] = usuario.get('email', 'No disponible') if usuario else 'No disponible'
        datos_seguros['telefono'] = usuario.get('telefono', 'No especificado') if usuario else 'No especificado'
        datos_seguros['direccion'] = usuario.get('direccion', 'No especificada') if usuario else 'No especificada'
        datos_seguros['fecha_nacimiento_str'] = usuario.fecha_nacimiento.strftime('%d/%m/%Y') if usuario and usuario.get('fecha_nacimiento') else 'No especificada'
        datos_seguros['estado'] = usuario.get('estado', 'inactivo') if usuario else 'inactivo'
        datos_seguros['estado_activo'] = (usuario.get('estado', 'inactivo') == 'activo') if usuario else False
        
        return dict(
            success=True,
            cliente=cliente,
            usuario=usuario,
            datos_seguros=datos_seguros,
            cuentas=cuentas,
            ultimas_transacciones=ultimas_transacciones,
            debug_info={
                'cliente_id': cliente_id,
                'cliente_existe': bool(cliente),
                'usuario_existe': bool(usuario),
                'num_cuentas': len(cuentas),
                'num_transacciones': len(ultimas_transacciones)
            }
        )
        
    except Exception as e:
        return dict(
            error=f"Error en detalle_debug: {str(e)}",
            cliente_id=cliente_id
        )

@auth.requires_login()
def detalle_minimo():
    """
    Versión mínima para probar que la vista funciona
    """
    
    if not (auth.has_membership('administrador') or auth.has_membership('operador')):
        session.flash = "No tiene permisos para ver detalles de clientes"
        redirect(URL('default', 'index'))
    
    cliente_id = request.args(0)
    if not cliente_id:
        session.flash = "ID de cliente requerido"
        redirect(URL('clientes', 'listar'))
    
    # Obtener información completa del cliente
    cliente = db(db.clientes.id == cliente_id).select().first()
    
    if not cliente:
        session.flash = "Cliente no encontrado"
        redirect(URL('clientes', 'listar'))
    
    # Obtener información del usuario asociado
    usuario = db(db.auth_user.id == cliente.user_id).select().first()
    
    # Preparar datos seguros básicos
    from gluon.storage import Storage
    datos_seguros = Storage()
    datos_seguros['nombre_completo'] = f"{usuario.get('first_name', 'N/A')} {usuario.get('last_name', '')}".strip() if usuario else 'No disponible'
    datos_seguros['email'] = usuario.get('email', 'No disponible') if usuario else 'No disponible'
    
    return dict(
        cliente=cliente,
        datos_seguros=datos_seguros
    )

@auth.requires_login()
def detalle_test():
    """
    Versión de prueba para diagnosticar la vista principal
    """
    
    if not (auth.has_membership('administrador') or auth.has_membership('operador')):
        session.flash = "No tiene permisos para ver detalles de clientes"
        redirect(URL('default', 'index'))
    
    cliente_id = request.args(0)
    if not cliente_id:
        session.flash = "ID de cliente requerido"
        redirect(URL('clientes', 'listar'))
    
    # Obtener información completa del cliente
    cliente = db(db.clientes.id == cliente_id).select().first()
    
    if not cliente:
        session.flash = "Cliente no encontrado"
        redirect(URL('clientes', 'listar'))
    
    # Obtener información del usuario asociado
    usuario = db(db.auth_user.id == cliente.user_id).select().first()
    
    # Preparar datos seguros básicos
    from gluon.storage import Storage
    datos_seguros = Storage()
    datos_seguros['nombre_completo'] = f"{usuario.get('first_name', 'N/A')} {usuario.get('last_name', '')}".strip() if usuario else 'No disponible'
    datos_seguros['email'] = usuario.get('email', 'No disponible') if usuario else 'No disponible'
    
    return dict(
        cliente=cliente,
        datos_seguros=datos_seguros
    )

@auth.requires_login()
def cambiar_estado():
    """
    Función para activar o inactivar un cliente
    Solo administradores y operadores pueden cambiar el estado
    """
    try:
        # Verificar permisos
        if not (auth.has_membership('administrador') or auth.has_membership('operador')):
            session.flash = "No tiene permisos para cambiar el estado de clientes"
            redirect(URL('clientes', 'listar'))
        
        # Obtener parámetros
        cliente_id = request.args(0)
        nuevo_estado = request.args(1)
        
        # Validaciones básicas
        if not cliente_id or not nuevo_estado:
            session.flash = "Parámetros inválidos"
            redirect(URL('clientes', 'listar'))
        
        if nuevo_estado not in ['activo', 'inactivo']:
            session.flash = "Estado inválido. Debe ser 'activo' o 'inactivo'"
            redirect(URL('clientes', 'listar'))
        
        # Buscar el cliente
        cliente = db(db.clientes.id == cliente_id).select().first()
        if not cliente:
            session.flash = "Cliente no encontrado"
            redirect(URL('clientes', 'listar'))
        
        # Obtener datos del usuario asociado
        usuario = db(db.auth_user.id == cliente.user_id).select().first()
        if not usuario:
            session.flash = "Usuario asociado no encontrado"
            redirect(URL('clientes', 'listar'))
        
        # Verificar si ya tiene el estado solicitado
        if usuario.estado == nuevo_estado:
            session.flash = f"El cliente ya está {nuevo_estado}"
            redirect(URL('clientes', 'listar'))
        
        # Cambiar el estado
        db(db.auth_user.id == cliente.user_id).update(estado=nuevo_estado)
        
        # Registrar en log de auditoría si existe
        try:
            if hasattr(db, 'logs_auditoria'):
                db.logs_auditoria.insert(
                    usuario_id=auth.user.id,
                    accion=f'cambio_estado_cliente',
                    tabla_afectada='auth_user',
                    registro_id=usuario.id,
                    detalles=f'Cliente {usuario.first_name} {usuario.last_name} (ID: {cliente_id}) cambiado de {usuario.estado} a {nuevo_estado}',
                    ip_address=request.env.remote_addr or 'unknown',
                    fecha=datetime.now()
                )
        except Exception as e:
            # No fallar si no se puede registrar en auditoría
            logger.warning(f"No se pudo registrar en auditoría: {str(e)}")
        
        # Confirmar cambios
        db.commit()
        
        # Mensaje de éxito
        accion = "activado" if nuevo_estado == 'activo' else "inactivado"
        session.flash = f"✅ Cliente {usuario.first_name} {usuario.last_name} ha sido {accion} exitosamente"
        
        # Log del cambio
        logger.info(f"Estado de cliente cambiado - Usuario: {auth.user.email}, Cliente: {usuario.first_name} {usuario.last_name} (ID: {cliente_id}), Nuevo estado: {nuevo_estado}")
        
    except Exception as e:
        # Rollback en caso de error
        db.rollback()
        
        # Log del error
        logger.error(f"Error cambiando estado de cliente: {str(e)}")
        
        # Mensaje de error
        session.flash = f"❌ Error al cambiar el estado del cliente: {str(e)}"
    
    # Redirigir de vuelta a la lista
    redirect(URL('clientes', 'listar'))