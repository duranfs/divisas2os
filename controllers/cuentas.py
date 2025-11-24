# -*- coding: utf-8 -*-
"""
Controlador de Cuentas Bancarias
Sistema de Divisas Bancario

Funciones principales:
- Creación de cuentas con número único
- Consulta de saldos por moneda
- Historial de movimientos
"""

import random
import string
from datetime import datetime, timedelta
from gluon.storage import Storage

# -------------------------------------------------------------------------
# Funciones de validación de permisos y seguridad
# -------------------------------------------------------------------------

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

def sanitize_account_search_input(input_value, max_length=100):
    """
    Sanitiza entradas de búsqueda para cuentas
    Requisitos: 2.4, 7.2
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
    
    # Remover caracteres potencialmente peligrosos para SQL
    dangerous_chars = ['\'', '"', ';', '--', '/*', '*/', 'xp_', 'sp_', 'DROP', 'DELETE', 'INSERT', 'UPDATE', 'UNION', 'SELECT']
    for char in dangerous_chars:
        input_str = input_str.replace(char, '')
    
    return input_str

def sanitize_account_number_input(numero_cuenta):
    """
    Sanitiza entrada de número de cuenta
    Requisitos: 7.2
    """
    if not numero_cuenta:
        return ''
    
    numero_str = str(numero_cuenta).strip()
    
    # Limitar longitud (números de cuenta son de 20 dígitos)
    if len(numero_str) > 25:
        numero_str = numero_str[:25]
    
    # Escapar HTML
    import html
    numero_str = html.escape(numero_str)
    
    # Solo permitir números y guiones
    import re
    numero_clean = re.sub(r'[^0-9-]', '', numero_str)
    
    return numero_clean

def sanitize_amount_input(amount_input):
    """
    Sanitiza entrada de montos
    Requisitos: 7.2
    """
    if not amount_input:
        return ''
    
    amount_str = str(amount_input).strip()
    
    # Escapar HTML
    import html
    amount_str = html.escape(amount_str)
    
    # Solo permitir números, punto decimal y coma
    import re
    amount_clean = re.sub(r'[^0-9.,]', '', amount_str)
    
    # Validar que sea un número válido
    try:
        # Reemplazar coma por punto para validación
        amount_test = amount_clean.replace(',', '.')
        float(amount_test)
        return amount_clean
    except ValueError:
        return ''

def validate_account_search_parameters(params):
    """
    Valida y sanitiza parámetros de búsqueda de cuentas
    Requisitos: 2.4, 7.2
    """
    sanitized_params = {}
    security_issues = []
    
    # Sanitizar búsqueda general
    if 'buscar' in params:
        original_value = params['buscar']
        sanitized_value = sanitize_account_search_input(original_value)
        sanitized_params['buscar'] = sanitized_value
        
        if original_value and original_value != sanitized_value:
            security_issues.append(f"Búsqueda sanitizada: '{original_value}' -> '{sanitized_value}'")
    
    # Sanitizar número de cuenta
    if 'numero_cuenta' in params:
        original_value = params['numero_cuenta']
        sanitized_value = sanitize_account_number_input(original_value)
        sanitized_params['numero_cuenta'] = sanitized_value
        
        if original_value and original_value != sanitized_value:
            security_issues.append(f"Número cuenta sanitizado: '{original_value}' -> '{sanitized_value}'")
    
    # Sanitizar estado (lista cerrada)
    if 'estado' in params:
        estado = str(params['estado']).strip().lower()
        if estado in ['todos', 'activa', 'inactiva', 'bloqueada']:
            sanitized_params['estado'] = estado
        else:
            sanitized_params['estado'] = 'todos'
            if params['estado'] != 'todos':
                security_issues.append(f"Estado inválido rechazado: '{params['estado']}'")
    
    # Sanitizar tipo de cuenta (lista cerrada)
    if 'tipo' in params:
        tipo = str(params['tipo']).strip().lower()
        if tipo in ['todos', 'corriente', 'ahorro']:
            sanitized_params['tipo'] = tipo
        else:
            sanitized_params['tipo'] = 'todos'
            if params['tipo'] != 'todos':
                security_issues.append(f"Tipo inválido rechazado: '{params['tipo']}'")
    
    # Sanitizar montos
    if 'saldo_min' in params:
        original_value = params['saldo_min']
        sanitized_value = sanitize_amount_input(original_value)
        sanitized_params['saldo_min'] = sanitized_value
        
        if original_value and original_value != sanitized_value:
            security_issues.append(f"Saldo mínimo sanitizado: '{original_value}' -> '{sanitized_value}'")
    
    if 'saldo_max' in params:
        original_value = params['saldo_max']
        sanitized_value = sanitize_amount_input(original_value)
        sanitized_params['saldo_max'] = sanitized_value
        
        if original_value and original_value != sanitized_value:
            security_issues.append(f"Saldo máximo sanitizado: '{original_value}' -> '{sanitized_value}'")
    
    # Sanitizar moneda (lista cerrada)
    if 'moneda_saldo' in params:
        moneda = str(params['moneda_saldo']).strip().upper()
        if moneda in ['VES', 'USD', 'EUR', 'USDT']:
            sanitized_params['moneda_saldo'] = moneda
        else:
            sanitized_params['moneda_saldo'] = 'VES'
            if params['moneda_saldo'] != 'VES':
                security_issues.append(f"Moneda inválida rechazada: '{params['moneda_saldo']}'")
    
    # Sanitizar página
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
            f"Parámetros sanitizados en búsqueda de cuentas: {'; '.join(security_issues)}"
        )
    
    return sanitized_params

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

# -------------------------------------------------------------------------
# Decoradores de autenticación y autorización
# -------------------------------------------------------------------------

@auth.requires_login()
def index():
    """Dashboard principal de cuentas - Versión simplificada y robusta"""
    try:
        # Enfoque directo: buscar si el usuario es cliente primero
        cliente_record = db(db.clientes.user_id == auth.user.id).select().first()
        
        if cliente_record:
            # Es un cliente - obtener información completa
            usuario = db(db.auth_user.id == auth.user.id).select().first()
            
            # Crear objeto cliente combinado
            cliente = Storage()
            cliente.id = cliente_record.id
            cliente.user_id = cliente_record.user_id
            cliente.cedula = cliente_record.cedula or ''
            cliente.fecha_registro = cliente_record.fecha_registro
            cliente.first_name = usuario.first_name if usuario else ''
            cliente.last_name = usuario.last_name if usuario else ''
            cliente.email = usuario.email if usuario else ''
            
        else:
            # No es cliente - verificar si es administrador/operador
            user_roles = get_user_roles()
            if 'administrador' in user_roles or 'operador' in user_roles:
                cliente_id = request.vars.cliente_id
                if cliente_id:
                    try:
                        cliente_id = int(cliente_id)
                        cliente_record = db(db.clientes.id == cliente_id).select().first()
                        if not cliente_record:
                            session.flash = "Cliente no encontrado"
                            redirect(URL('clientes', 'listar'))
                        
                        # Obtener usuario del cliente seleccionado
                        usuario = db(db.auth_user.id == cliente_record.user_id).select().first()
                        
                        # Crear objeto cliente
                        cliente = Storage()
                        cliente.id = cliente_record.id
                        cliente.user_id = cliente_record.user_id
                        cliente.cedula = cliente_record.cedula or ''
                        cliente.fecha_registro = cliente_record.fecha_registro
                        cliente.first_name = usuario.first_name if usuario else ''
                        cliente.last_name = usuario.last_name if usuario else ''
                        cliente.email = usuario.email if usuario else ''
                        
                    except (ValueError, TypeError):
                        session.flash = "ID de cliente inválido"
                        redirect(URL('clientes', 'listar'))
                else:
                    # Redirigir a lista para seleccionar cliente
                    redirect(URL('clientes', 'listar'))
            else:
                session.flash = "Debe completar su registro como cliente"
                redirect(URL('clientes', 'registrar'))
        
        # Log de acceso para auditoría
        import logging
        logger = logging.getLogger("web2py.app.cuentas")
        logger.info(f"Acceso a dashboard de cuentas por usuario {auth.user.id} - Cliente: {cliente.id if cliente else 'N/A'}")
        
        # Obtener todas las cuentas del cliente con información adicional
        cuentas = db(db.cuentas.cliente_id == cliente.id).select(
            orderby=db.cuentas.fecha_creacion
        )
        
        # Calcular totales por moneda
        total_ves = sum([float(cuenta.saldo_ves or 0) for cuenta in cuentas])
        total_usd = sum([float(cuenta.saldo_usd or 0) for cuenta in cuentas])
        total_eur = sum([float(cuenta.saldo_eur or 0) for cuenta in cuentas])
        total_usdt = sum([float(cuenta.saldo_usdt or 0) for cuenta in cuentas])
        
        # Obtener tasas actuales para mostrar equivalencias
        tasa_actual = db(db.tasas_cambio.activa == True).select(
            orderby=~db.tasas_cambio.fecha | ~db.tasas_cambio.hora
        ).first()
        
        # Calcular equivalencias si hay tasas disponibles
        equivalencias = {}
        if tasa_actual:
            # Convertir todo a VES como base
            total_ves_equivalente = total_ves
            if total_usd and tasa_actual.usd_ves:
                total_ves_equivalente += total_usd * float(tasa_actual.usd_ves)
            if total_eur and tasa_actual.eur_ves:
                total_ves_equivalente += total_eur * float(tasa_actual.eur_ves)
            if total_usdt and tasa_actual.usdt_ves:
                total_ves_equivalente += total_usdt * float(tasa_actual.usdt_ves)
            
            equivalencias = {
                'total_ves': total_ves_equivalente,
                'total_usd': total_ves_equivalente / float(tasa_actual.usd_ves) if tasa_actual.usd_ves else 0,
                'total_eur': total_ves_equivalente / float(tasa_actual.eur_ves) if tasa_actual.eur_ves else 0,
                'total_usdt': total_ves_equivalente / float(tasa_actual.usdt_ves) if tasa_actual.usdt_ves else 0
            }
        
        # Obtener últimas transacciones del cliente
        ultimas_transacciones = []
        if cuentas:
            cuenta_ids = [cuenta.id for cuenta in cuentas]
            ultimas_transacciones = db(db.transacciones.cuenta_id.belongs(cuenta_ids)).select(
                orderby=~db.transacciones.fecha_transaccion,
                limitby=(0, 5)
            )
        
        # Estadísticas del cliente
        stats = {
            'total_cuentas': len(cuentas),
            'cuentas_activas': len([c for c in cuentas if c.estado == 'activa']),
            'total_transacciones': len(ultimas_transacciones)
        }
        
        return dict(
            cuentas=cuentas,
            cliente=cliente,
            total_ves=total_ves,
            total_usd=total_usd,
            total_eur=total_eur,
            total_usdt=total_usdt,
            tasa_actual=tasa_actual,
            equivalencias=equivalencias,
            ultimas_transacciones=ultimas_transacciones,
            stats=stats
        )
        
    except Exception as e:
        # Log del error
        import logging
        logger = logging.getLogger("web2py.app.cuentas")
        logger.error(f"Error al cargar dashboard de cuentas del cliente: {str(e)}")
        
        # Mostrar mensaje de error al usuario
        response.flash = "Error al cargar sus cuentas. Intente nuevamente."
        return dict(
            cuentas=[],
            cliente=None,
            total_ves=0,
            total_usd=0,
            total_eur=0,
            total_usdt=0,
            tasa_actual=None,
            equivalencias={},
            ultimas_transacciones=[],
            stats={'total_cuentas': 0, 'cuentas_activas': 0, 'total_transacciones': 0},
            error_message="No se pudieron cargar los datos de sus cuentas."
        )

@auth.requires_login()
def crear():
    """Crear nueva cuenta bancaria"""
    # Verificar si es administrador o cliente
    es_admin = auth.has_membership('administrador')
    
    if es_admin:
        # Administrador puede crear cuenta para cualquier cliente
        form = SQLFORM(db.cuentas, fields=['cliente_id', 'tipo_cuenta'])
    else:
        # Cliente solo puede crear su propia cuenta
        cliente = db(db.clientes.user_id == auth.user.id).select().first()
        
        if not cliente:
            session.flash = "Debe completar su registro como cliente primero"
            redirect(URL('clientes', 'registrar'))
        
        # Crear formulario sin campo cliente_id
        form = SQLFORM(db.cuentas, fields=['tipo_cuenta'])
        form.vars.cliente_id = cliente.id
    
    if form.validate():
        try:
            # Generar número de cuenta único
            numero_cuenta = generar_numero_cuenta()
            
            # Insertar la cuenta
            cuenta_id = db.cuentas.insert(
                cliente_id=form.vars.cliente_id,
                tipo_cuenta=form.vars.tipo_cuenta,
                numero_cuenta=numero_cuenta,
                saldo_ves=0,
                saldo_usd=0,
                saldo_eur=0,
                saldo_usdt=0,
                estado='activa'
            )
            db.commit()
            
            # Mostrar mensaje de éxito
            response.flash = f"Cuenta creada exitosamente. Número de cuenta: {numero_cuenta}"
            
        except Exception as e:
            db.rollback()
            response.flash = f"Error al crear la cuenta: {str(e)}"
    elif form.errors:
        response.flash = "Por favor corrija los errores en el formulario"
    
    return dict(form=form)

@auth.requires_login()
def consultar():
    """Consultar saldos de una cuenta específica - Requisitos: 2.1, 7.1"""
    cuenta_id = request.args(0)
    
    if not cuenta_id:
        session.flash = "Debe especificar una cuenta"
        redirect(URL('cuentas', 'index'))
    
    # Validar acceso a la cuenta con función mejorada
    user_roles = get_user_roles()
    has_access, access_error = validate_account_access(cuenta_id, auth.user.id, user_roles)
    
    if not has_access:
        session.flash = access_error
        redirect(URL('default', 'index'))
    
    # Obtener la cuenta (ya validada)
    cuenta = db(db.cuentas.id == cuenta_id).select().first()
    
    if not cuenta:
        session.flash = "Cuenta no encontrada"
        redirect(URL('cuentas', 'index'))
    
    # Log de acceso para auditoría
    import logging
    logger = logging.getLogger("web2py.app.cuentas")
    logger.info(f"Consulta de saldos de cuenta {cuenta_id} por usuario {auth.user.id}")
    
    # Obtener tasas actuales para conversiones
    tasa_actual = db(db.tasas_cambio.activa == True).select(
        orderby=~db.tasas_cambio.fecha | ~db.tasas_cambio.hora
    ).first()
    
    # Calcular equivalencias si hay tasas disponibles
    equivalencias = {}
    if tasa_actual:
        # Convertir todo a VES como base (convertir a float para evitar errores de tipos)
        total_ves_equivalente = float(cuenta.saldo_ves or 0)
        if cuenta.saldo_usd:
            total_ves_equivalente += float(cuenta.saldo_usd) * float(tasa_actual.usd_ves)
        if cuenta.saldo_eur:
            total_ves_equivalente += float(cuenta.saldo_eur) * float(tasa_actual.eur_ves)
        
        equivalencias = {
            'total_ves': total_ves_equivalente,
            'total_usd': total_ves_equivalente / float(tasa_actual.usd_ves) if tasa_actual.usd_ves else 0,
            'total_eur': total_ves_equivalente / float(tasa_actual.eur_ves) if tasa_actual.eur_ves else 0
        }
    
    return dict(
        cuenta=cuenta,
        cliente=cliente,
        tasa_actual=tasa_actual,
        equivalencias=equivalencias
    )

@auth.requires_login()
def movimientos():
    """Historial de movimientos de una cuenta"""
    cuenta_id = request.args(0)
    
    # Verificar que el usuario sea cliente
    cliente = db(db.clientes.user_id == auth.user.id).select().first()
    
    if not cliente:
        session.flash = "Acceso no autorizado"
        redirect(URL('default', 'index'))
    
    # Obtener todas las cuentas del cliente
    cuentas_cliente = db(db.cuentas.cliente_id == cliente.id).select()
    
    # Si no se especifica cuenta_id, usar la primera cuenta del cliente
    if not cuenta_id:
        if not cuentas_cliente:
            session.flash = "No tiene cuentas registradas"
            redirect(URL('cuentas', 'index'))
        
        # Usar la primera cuenta
        cuenta_id = cuentas_cliente[0].id
    
    cuenta = db(
        (db.cuentas.id == cuenta_id) & 
        (db.cuentas.cliente_id == cliente.id)
    ).select().first()
    
    if not cuenta:
        session.flash = "Cuenta no encontrada o acceso no autorizado"
        redirect(URL('cuentas', 'index'))
    
    # Parámetros de filtrado
    fecha_desde = request.vars.fecha_desde
    fecha_hasta = request.vars.fecha_hasta
    tipo_operacion = request.vars.tipo_operacion
    moneda = request.vars.moneda
    
    # Construir query base
    query = (db.transacciones.cuenta_id == cuenta.id)
    
    # Aplicar filtros
    if fecha_desde:
        try:
            fecha_desde_dt = datetime.strptime(fecha_desde, '%Y-%m-%d')
            query &= (db.transacciones.fecha_transaccion >= fecha_desde_dt)
        except ValueError:
            pass
    
    if fecha_hasta:
        try:
            fecha_hasta_dt = datetime.strptime(fecha_hasta, '%Y-%m-%d') + timedelta(days=1)
            query &= (db.transacciones.fecha_transaccion < fecha_hasta_dt)
        except ValueError:
            pass
    
    if tipo_operacion and tipo_operacion != 'todos':
        query &= (db.transacciones.tipo_operacion == tipo_operacion)
    
    if moneda and moneda != 'todas':
        query &= ((db.transacciones.moneda_origen == moneda) | 
                 (db.transacciones.moneda_destino == moneda))
    
    # Obtener transacciones con paginación
    page = int(request.vars.page or 1)
    items_per_page = 20
    
    transacciones = db(query).select(
        orderby=~db.transacciones.fecha_transaccion,
        limitby=((page-1)*items_per_page, page*items_per_page)
    )
    
    # Contar total para paginación
    total_transacciones = db(query).count()
    total_pages = (total_transacciones + items_per_page - 1) // items_per_page
    
    return dict(
        cuenta=cuenta,
        cliente=cliente,
        cuentas_cliente=cuentas_cliente,
        transacciones=transacciones,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        tipo_operacion=tipo_operacion,
        moneda=moneda,
        page=page,
        total_pages=total_pages,
        total_transacciones=total_transacciones
    )

@auth.requires_login()
def detalle():
    """Ver detalles de una cuenta específica - Requisitos: 2.1, 7.1"""
    cuenta_id = request.args(0)
    
    if not cuenta_id:
        session.flash = "Debe especificar una cuenta"
        redirect(URL('cuentas', 'index'))
    
    # Validar acceso a la cuenta con función mejorada
    user_roles = get_user_roles()
    has_access, access_error = validate_account_access(cuenta_id, auth.user.id, user_roles)
    
    if not has_access:
        session.flash = access_error
        redirect(URL('cuentas', 'index'))
    
    # Obtener la cuenta (ya validada)
    cuenta = db(db.cuentas.id == cuenta_id).select().first()
    
    if not cuenta:
        session.flash = "Cuenta no encontrada"
        redirect(URL('cuentas', 'index'))
    
    # Obtener cliente asociado a la cuenta
    cliente = db(db.clientes.id == cuenta.cliente_id).select().first()
    
    # Obtener últimas 5 transacciones
    ultimas_transacciones = db(db.transacciones.cuenta_id == cuenta.id).select(
        orderby=~db.transacciones.fecha_transaccion,
        limitby=(0, 5)
    )
    
    # Obtener estadísticas del mes actual
    inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    transacciones_mes = db(
        (db.transacciones.cuenta_id == cuenta.id) &
        (db.transacciones.fecha_transaccion >= inicio_mes)
    ).select()
    
    estadisticas_mes = {
        'total_transacciones': len(transacciones_mes),
        'compras': len([t for t in transacciones_mes if t.tipo_operacion == 'compra']),
        'ventas': len([t for t in transacciones_mes if t.tipo_operacion == 'venta']),
        'monto_total_ves': sum([t.monto_origen if t.moneda_origen == 'VES' else t.monto_destino 
                               for t in transacciones_mes if 'VES' in [t.moneda_origen, t.moneda_destino]])
    }
    
    return dict(
        cuenta=cuenta,
        cliente=cliente,
        ultimas_transacciones=ultimas_transacciones,
        estadisticas_mes=estadisticas_mes
    )

# -------------------------------------------------------------------------
# Funciones administrativas (requieren rol de administrador)
# -------------------------------------------------------------------------


@auth.requires_membership('administrador')
def listar_todas():
    """Listar todas las cuentas del sistema (solo administradores) - Versión corregida"""
    try:
        # Log de acceso para auditoría
        import logging
        logger = logging.getLogger("web2py.app.cuentas")
        logger.info(f"Acceso a lista completa de cuentas por administrador {auth.user.id} ({auth.user.email})")
        
        # Obtener y sanitizar parámetros de búsqueda de forma simple
        buscar = str(request.vars.buscar or '').strip()[:100]  # Limitar longitud
        numero_cuenta = str(request.vars.numero_cuenta or '').strip()[:25]
        estado = str(request.vars.estado or 'todos').strip().lower()
        tipo = str(request.vars.tipo or 'todos').strip().lower()
        saldo_min = str(request.vars.saldo_min or '').strip()
        saldo_max = str(request.vars.saldo_max or '').strip()
        moneda_saldo = str(request.vars.moneda_saldo or 'VES').strip().upper()
        
        # Validar página
        try:
            page = int(request.vars.page or 1)
            if page < 1:
                page = 1
        except (ValueError, TypeError):
            page = 1
        
        # Validar estado y tipo (listas cerradas)
        if estado not in ['todos', 'activa', 'inactiva', 'bloqueada']:
            estado = 'todos'
        
        if tipo not in ['todos', 'corriente', 'ahorro']:
            tipo = 'todos'
        
        if moneda_saldo not in ['VES', 'USD', 'EUR', 'USDT']:
            moneda_saldo = 'VES'
        
        # Query base con JOIN explícito para obtener datos del cliente
        query = (db.cuentas.cliente_id == db.clientes.id) & \
                (db.clientes.user_id == db.auth_user.id)
        
        # Aplicar filtros de búsqueda general
        if buscar:
            query &= ((db.cuentas.numero_cuenta.contains(buscar)) |
                     (db.clientes.cedula.contains(buscar)) |
                     (db.auth_user.first_name.contains(buscar)) |
                     (db.auth_user.last_name.contains(buscar)) |
                     (db.auth_user.email.contains(buscar)))
        
        # Filtro específico por número de cuenta
        if numero_cuenta:
            query &= (db.cuentas.numero_cuenta.contains(numero_cuenta))
        
        # Filtros por estado y tipo
        if estado != 'todos':
            query &= (db.cuentas.estado == estado)
        
        if tipo != 'todos':
            query &= (db.cuentas.tipo_cuenta == tipo)
        
        # Filtros por rango de saldos
        if saldo_min:
            try:
                saldo_min_val = float(saldo_min)
                if moneda_saldo == 'VES':
                    query &= (db.cuentas.saldo_ves >= saldo_min_val)
                elif moneda_saldo == 'USD':
                    query &= (db.cuentas.saldo_usd >= saldo_min_val)
                elif moneda_saldo == 'EUR':
                    query &= (db.cuentas.saldo_eur >= saldo_min_val)
                elif moneda_saldo == 'USDT':
                    query &= (db.cuentas.saldo_usdt >= saldo_min_val)
            except (ValueError, TypeError):
                pass  # Ignorar valores inválidos
        
        if saldo_max:
            try:
                saldo_max_val = float(saldo_max)
                if moneda_saldo == 'VES':
                    query &= (db.cuentas.saldo_ves <= saldo_max_val)
                elif moneda_saldo == 'USD':
                    query &= (db.cuentas.saldo_usd <= saldo_max_val)
                elif moneda_saldo == 'EUR':
                    query &= (db.cuentas.saldo_eur <= saldo_max_val)
                elif moneda_saldo == 'USDT':
                    query &= (db.cuentas.saldo_usdt <= saldo_max_val)
            except (ValueError, TypeError):
                pass  # Ignorar valores inválidos
        
        # Configurar paginación
        items_per_page = 25
        
        cuentas = db(query).select(
            db.cuentas.ALL,
            db.clientes.cedula,
            db.auth_user.first_name,
            db.auth_user.last_name,
            db.auth_user.email,
            orderby=~db.cuentas.fecha_creacion,
            limitby=((page-1)*items_per_page, page*items_per_page)
        )
        
        # Contar total para paginación
        total_cuentas = db(query).count()
        total_pages = (total_cuentas + items_per_page - 1) // items_per_page
        
        # Obtener estadísticas generales
        from gluon.storage import Storage
        stats = Storage(
            total=db(db.cuentas.id > 0).count(),
            activas=db(db.cuentas.estado == 'activa').count(),
            inactivas=db(db.cuentas.estado == 'inactiva').count(),
            corrientes=db(db.cuentas.tipo_cuenta == 'corriente').count(),
            ahorros=db(db.cuentas.tipo_cuenta == 'ahorro').count()
        )
        
        return dict(
            cuentas=cuentas,
            buscar=buscar,
            numero_cuenta=numero_cuenta,
            estado=estado,
            tipo=tipo,
            saldo_min=saldo_min,
            saldo_max=saldo_max,
            moneda_saldo=moneda_saldo,
            page=page,
            total_pages=total_pages,
            total_cuentas=total_cuentas,
            stats=stats
        )
        
    except Exception as e:
        # Log del error
        import logging
        logger = logging.getLogger("web2py.app.cuentas")
        logger.error(f"Error al obtener lista de cuentas: {str(e)}")
        
        # Mostrar mensaje de error al usuario
        response.flash = f"Error al cargar la lista de cuentas: {str(e)}"
        
        from gluon.storage import Storage
        return dict(
            cuentas=[],
            error_message="No se pudieron cargar los datos de cuentas.",
            buscar='',
            numero_cuenta='',
            estado='todos',
            tipo='todos',
            saldo_min='',
            saldo_max='',
            moneda_saldo='VES',
            page=1,
            total_pages=0,
            total_cuentas=0,
            stats=Storage(total=0, activas=0, inactivas=0, corrientes=0, ahorros=0)
        )



@auth.requires_membership('administrador')
def gestionar():
    """Gestionar cuenta específica (solo administradores)"""
    cuenta_id = request.args(0)
    
    if not cuenta_id:
        session.flash = "Debe especificar una cuenta"
        redirect(URL('cuentas', 'listar_todas'))
    
    # Obtener cuenta
    cuenta_record = db(db.cuentas.id == cuenta_id).select().first()
    
    if not cuenta_record:
        session.flash = "Cuenta no encontrada"
        redirect(URL('cuentas', 'listar_todas'))
    
    # Obtener cliente asociado
    cliente = db(db.clientes.id == cuenta_record.cliente_id).select().first()
    if not cliente:
        session.flash = "Cliente no encontrado"
        redirect(URL('cuentas', 'listar_todas'))
    
    # Obtener usuario asociado
    usuario = db(db.auth_user.id == cliente.user_id).select().first()
    if not usuario:
        session.flash = "Usuario no encontrado"
        redirect(URL('cuentas', 'listar_todas'))
    
    # Formulario para editar estado y saldos (incluyendo USDT)
    form = SQLFORM(db.cuentas, cuenta_record.id, 
                   fields=['estado', 'saldo_ves', 'saldo_usd', 'saldo_eur', 'saldo_usdt'],
                   showid=False)
    
    if form.process().accepted:
        session.flash = "Cuenta actualizada exitosamente"
        redirect(URL('cuentas', 'gestionar', args=[cuenta_id]))
    elif form.errors:
        response.flash = "Por favor corrija los errores en el formulario"
    
    # Obtener últimas transacciones
    transacciones = db(db.transacciones.cuenta_id == cuenta_id).select(
        orderby=~db.transacciones.fecha_transaccion,
        limitby=(0, 10)
    )
    
    return dict(
        cuenta=cuenta_record,
        cliente=cliente,
        usuario=usuario,
        form=form,
        transacciones=transacciones
    )

# -------------------------------------------------------------------------
# Funciones auxiliares
# -------------------------------------------------------------------------

def generar_numero_cuenta():
    """Generar número de cuenta único de 20 dígitos"""
    while True:
        # Generar número aleatorio de 20 dígitos
        numero = ''.join([str(random.randint(0, 9)) for _ in range(20)])
        
        # Verificar que no exista en la base de datos
        if db(db.cuentas.numero_cuenta == numero).isempty():
            return numero

def obtener_saldo_cuenta(cuenta_id, moneda):
    """Obtener saldo de una cuenta en una moneda específica"""
    cuenta = db(db.cuentas.id == cuenta_id).select().first()
    
    if not cuenta:
        return 0
    
    if moneda == 'VES':
        return cuenta.saldo_ves or 0
    elif moneda == 'USD':
        return cuenta.saldo_usd or 0
    elif moneda == 'EUR':
        return cuenta.saldo_eur or 0
    else:
        return 0

def actualizar_saldo_cuenta(cuenta_id, moneda, monto, operacion='suma'):
    """Actualizar saldo de una cuenta"""
    cuenta = db(db.cuentas.id == cuenta_id).select().first()
    
    if not cuenta:
        return False
    
    saldo_actual = obtener_saldo_cuenta(cuenta_id, moneda)
    
    if operacion == 'suma':
        nuevo_saldo = saldo_actual + monto
    elif operacion == 'resta':
        nuevo_saldo = saldo_actual - monto
        if nuevo_saldo < 0:
            return False  # No permitir saldos negativos
    else:
        return False
    
    # Actualizar según la moneda
    if moneda == 'VES':
        db(db.cuentas.id == cuenta_id).update(saldo_ves=nuevo_saldo)
    elif moneda == 'USD':
        db(db.cuentas.id == cuenta_id).update(saldo_usd=nuevo_saldo)
    elif moneda == 'EUR':
        db(db.cuentas.id == cuenta_id).update(saldo_eur=nuevo_saldo)
    else:
        return False
    
    return True

def validar_fondos_suficientes(cuenta_id, moneda, monto):
    """Validar si una cuenta tiene fondos suficientes"""
    saldo_actual = obtener_saldo_cuenta(cuenta_id, moneda)
    return saldo_actual >= monto
# -------------------------------------------------------------------------
# Nueva función simplificada para clientes
# -------------------------------------------------------------------------

@auth.requires_login()
def mis_cuentas():
    """Vista simplificada de cuentas para clientes - sin dependencia de roles complejos"""
    try:
        # Buscar directamente si el usuario es cliente
        cliente_record = db(db.clientes.user_id == auth.user.id).select().first()
        
        if not cliente_record:
            # No es cliente registrado
            session.flash = "Debe completar su registro como cliente"
            redirect(URL('clientes', 'registrar'))
        
        # Obtener información del usuario
        usuario = db(db.auth_user.id == auth.user.id).select().first()
        
        # Crear objeto cliente combinado
        cliente = Storage()
        cliente.id = cliente_record.id
        cliente.user_id = cliente_record.user_id
        cliente.cedula = cliente_record.cedula
        cliente.fecha_registro = cliente_record.fecha_registro
        cliente.first_name = usuario.first_name if usuario else ''
        cliente.last_name = usuario.last_name if usuario else ''
        cliente.email = usuario.email if usuario else ''
        
        # Obtener cuentas del cliente
        cuentas = db(db.cuentas.cliente_id == cliente.id).select(
            orderby=db.cuentas.fecha_creacion
        )
        
        # Calcular totales por moneda
        total_ves = sum([float(cuenta.saldo_ves or 0) for cuenta in cuentas])
        total_usd = sum([float(cuenta.saldo_usd or 0) for cuenta in cuentas])
        total_eur = sum([float(cuenta.saldo_eur or 0) for cuenta in cuentas])
        total_usdt = sum([float(cuenta.saldo_usdt or 0) for cuenta in cuentas])
        
        # Log de acceso
        import logging
        logger = logging.getLogger("web2py.app.cuentas")
        logger.info(f"Acceso a mis_cuentas por cliente {cliente.id} - Usuario: {auth.user.id}")
        
        return dict(
            cliente=cliente,
            cuentas=cuentas,
            total_ves=total_ves,
            total_usd=total_usd,
            total_eur=total_eur,
            total_usdt=total_usdt
        )
        
    except Exception as e:
        # Log del error
        import logging
        logger = logging.getLogger("web2py.app.cuentas")
        logger.error(f"Error en mis_cuentas para usuario {auth.user.id if auth.user else 'None'}: {str(e)}")
        
        session.flash = f"Error al cargar cuentas: {str(e)}"
        redirect(URL('default', 'dashboard'))
# -------------------------------------------------------------------------
# Función de debug temporal
# -------------------------------------------------------------------------

@auth.requires_login()
def debug_cliente():
    """Función temporal para debuggear problema de clientes"""
    
    debug_info = []
    
    # 1. Información del usuario autenticado
    debug_info.append(f"Usuario autenticado: {auth.user.id if auth.user else 'None'}")
    debug_info.append(f"Email del usuario: {auth.user.email if auth.user else 'None'}")
    
    # 2. Buscar en tabla clientes
    if auth.user:
        cliente_record = db(db.clientes.user_id == auth.user.id).select().first()
        debug_info.append(f"Cliente encontrado: {cliente_record.id if cliente_record else 'None'}")
        
        if cliente_record:
            debug_info.append(f"Cédula del cliente: {cliente_record.cedula}")
            debug_info.append(f"Fecha registro: {cliente_record.fecha_registro}")
            
            # 3. Buscar cuentas del cliente
            cuentas = db(db.cuentas.cliente_id == cliente_record.id).select()
            debug_info.append(f"Cuentas encontradas: {len(cuentas)}")
            
            for cuenta in cuentas:
                debug_info.append(f"  - Cuenta: {cuenta.numero_cuenta}, VES: {cuenta.saldo_ves}, Estado: {cuenta.estado}")
        
        # 4. Verificar roles usando get_user_roles
        try:
            user_roles = get_user_roles()
            debug_info.append(f"Roles del usuario (get_user_roles): {user_roles}")
        except Exception as e:
            debug_info.append(f"Error obteniendo roles: {str(e)}")
        
        # 5. Verificar membresías directamente en BD
        try:
            memberships = db(db.auth_membership.user_id == auth.user.id).select(
                db.auth_membership.ALL,
                db.auth_group.role,
                join=db.auth_group.on(db.auth_membership.group_id == db.auth_group.id)
            )
            debug_info.append(f"Membresías directas en BD: {[m.auth_group.role for m in memberships]}")
        except Exception as e:
            debug_info.append(f"Error obteniendo membresías: {str(e)}")
        
        # 6. Verificar auth.user_groups
        try:
            debug_info.append(f"auth.user_groups: {auth.user_groups}")
        except Exception as e:
            debug_info.append(f"Error con auth.user_groups: {str(e)}")
    
    return dict(debug_info=debug_info)
# -------------------------------------------------------------------------
# Función de debug para diagnosticar problema de clientes
# -------------------------------------------------------------------------

@auth.requires_login()
def debug_cliente():
    """Función de debug para ver exactamente qué datos tiene el cliente"""
    
    debug_info = {}
    
    # 1. Información básica del usuario autenticado
    debug_info['auth_user'] = {
        'id': auth.user.id if auth.user else None,
        'email': auth.user.email if auth.user else None,
        'first_name': auth.user.first_name if auth.user else None,
        'last_name': auth.user.last_name if auth.user else None
    }
    
    # 2. Buscar en tabla clientes
    try:
        cliente_record = db(db.clientes.user_id == auth.user.id).select().first()
        if cliente_record:
            debug_info['cliente_record'] = {
                'id': cliente_record.id,
                'user_id': cliente_record.user_id,
                'cedula': cliente_record.cedula,
                'fecha_registro': str(cliente_record.fecha_registro)
            }
        else:
            debug_info['cliente_record'] = None
    except Exception as e:
        debug_info['cliente_record'] = f"Error: {str(e)}"
    
    # 3. Buscar cuentas si es cliente
    debug_info['cuentas'] = []
    if cliente_record:
        try:
            cuentas = db(db.cuentas.cliente_id == cliente_record.id).select()
            for cuenta in cuentas:
                debug_info['cuentas'].append({
                    'id': cuenta.id,
                    'numero_cuenta': cuenta.numero_cuenta,
                    'tipo_cuenta': cuenta.tipo_cuenta,
                    'estado': cuenta.estado,
                    'saldo_ves': float(cuenta.saldo_ves or 0),
                    'saldo_usd': float(cuenta.saldo_usd or 0),
                    'saldo_eur': float(cuenta.saldo_eur or 0)
                })
        except Exception as e:
            debug_info['cuentas'] = f"Error: {str(e)}"
    
    # 4. Verificar roles
    try:
        user_roles = get_user_roles()
        debug_info['roles'] = user_roles
    except Exception as e:
        debug_info['roles'] = f"Error: {str(e)}"
    
    # 5. Información de la sesión
    debug_info['session_info'] = {
        'flash': response.flash,
        'user_id': auth.user_id
    }
    
    return dict(debug_info=debug_info)