# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Sistema de Divisas Bancario - Controlador Principal
# -------------------------------------------------------------------------

from datetime import datetime, timedelta
import json

# ---- Dashboard principal ----
def index():
    """Dashboard principal del sistema de divisas"""
    if auth.is_logged_in():
        return dashboard()
    else:
        # Página de bienvenida para usuarios no autenticados
        # Obtener tasas actuales para mostrar
        tasas_actuales = obtener_tasas_actuales()
        return dict(
            message=T('Bienvenido al Sistema de Divisas Bancario'),
            tasas=tasas_actuales,
            mostrar_login=True
        )

@auth.requires_login()
def dashboard():
    """Dashboard personalizado según el rol del usuario"""
    user_id = auth.user.id
    
    # Verificar si el usuario es cliente
    cliente = db(db.clientes.user_id == user_id).select().first()
    
    if cliente:
        return dashboard_cliente(cliente)
    else:
        # Verificar si es administrador u operador
        if auth.has_membership('administrador') or auth.has_membership('operador'):
            return dashboard_administrativo()
        else:
            # Usuario sin rol específico - mostrar dashboard básico
            return dashboard_basico()

def dashboard_cliente(cliente):
    """Dashboard específico para clientes"""
    # Obtener cuentas del cliente
    cuentas = db(db.cuentas.cliente_id == cliente.id).select()
    
    # Calcular totales por moneda (convertir a float para evitar problemas de tipos)
    total_ves = sum([float(cuenta.saldo_ves or 0) for cuenta in cuentas])
    total_usd = sum([float(cuenta.saldo_usd or 0) for cuenta in cuentas])
    total_eur = sum([float(cuenta.saldo_eur or 0) for cuenta in cuentas])
    
    # Obtener últimas transacciones
    ultimas_transacciones = db(
        (db.transacciones.cuenta_id.belongs([c.id for c in cuentas]))
    ).select(
        orderby=~db.transacciones.fecha_transaccion,
        limitby=(0, 5)
    )
    
    # Obtener tasas actuales
    tasas_actuales = obtener_tasas_actuales()
    
    # Calcular equivalencias en VES
    equivalencia_total_ves = total_ves
    if tasas_actuales and tasas_actuales.usd_ves:
        equivalencia_total_ves += total_usd * float(tasas_actuales.usd_ves)
    if tasas_actuales and tasas_actuales.eur_ves:
        equivalencia_total_ves += total_eur * float(tasas_actuales.eur_ves)
    
    return dict(
        tipo_dashboard='cliente',
        cliente=cliente,
        cuentas=cuentas,
        total_ves=total_ves,
        total_usd=total_usd,
        total_eur=total_eur,
        equivalencia_total_ves=equivalencia_total_ves,
        ultimas_transacciones=ultimas_transacciones,
        tasas_actuales=tasas_actuales,
        accesos_rapidos=generar_accesos_rapidos_cliente()
    )

def dashboard_administrativo():
    """Dashboard para administradores y operadores"""
    # Estadísticas del día
    hoy = datetime.now().date()
    
    # Transacciones del día
    transacciones_hoy = db(
        db.transacciones.fecha_transaccion >= hoy
    ).count()
    
    # Volumen de transacciones por moneda
    volumen_ves = db(
        (db.transacciones.fecha_transaccion >= hoy) &
        (db.transacciones.moneda_origen == 'VES')
    ).select(
        db.transacciones.monto_origen.sum()
    ).first()[db.transacciones.monto_origen.sum()] or 0
    
    volumen_usd = db(
        (db.transacciones.fecha_transaccion >= hoy) &
        (db.transacciones.moneda_origen == 'USD')
    ).select(
        db.transacciones.monto_origen.sum()
    ).first()[db.transacciones.monto_origen.sum()] or 0
    
    volumen_eur = db(
        (db.transacciones.fecha_transaccion >= hoy) &
        (db.transacciones.moneda_origen == 'EUR')
    ).select(
        db.transacciones.monto_origen.sum()
    ).first()[db.transacciones.monto_origen.sum()] or 0
    
    # Total de clientes activos
    clientes_activos = db(
        (db.clientes.id > 0) &
        (db.auth_user.id == db.clientes.user_id) &
        (db.auth_user.estado == 'activo')
    ).count()
    
    # Cuentas activas
    cuentas_activas = db(db.cuentas.estado == 'activa').count()
    
    # Obtener tasas actuales
    tasas_actuales = obtener_tasas_actuales()
    
    # Últimas transacciones del sistema
    ultimas_transacciones = db().select(
        db.transacciones.ALL,
        orderby=~db.transacciones.fecha_transaccion,
        limitby=(0, 10)
    )
    
    return dict(
        tipo_dashboard='administrativo',
        transacciones_hoy=transacciones_hoy,
        volumen_ves=volumen_ves,
        volumen_usd=volumen_usd,
        volumen_eur=volumen_eur,
        clientes_activos=clientes_activos,
        cuentas_activas=cuentas_activas,
        tasas_actuales=tasas_actuales,
        ultimas_transacciones=ultimas_transacciones,
        accesos_rapidos=generar_accesos_rapidos_admin()
    )

def dashboard_basico():
    """Dashboard básico para usuarios sin rol específico"""
    tasas_actuales = obtener_tasas_actuales()
    
    return dict(
        tipo_dashboard='basico',
        tasas_actuales=tasas_actuales,
        mensaje='Complete su registro como cliente para acceder a todas las funcionalidades'
    )

def obtener_tasas_actuales():
    """Obtiene las tasas de cambio más recientes"""
    tasa = db(db.tasas_cambio.activa == True).select(
        orderby=~db.tasas_cambio.fecha | ~db.tasas_cambio.hora,
        limitby=(0, 1)
    ).first()
    
    return tasa

def generar_accesos_rapidos_cliente():
    """Genera los accesos rápidos para clientes"""
    return [
        {
            'titulo': 'Comprar Divisas',
            'descripcion': 'Comprar USD o EUR con VES',
            'url': URL('divisas', 'comprar'),
            'icono': 'fas fa-shopping-cart',
            'color': 'success'
        },
        {
            'titulo': 'Vender Divisas',
            'descripcion': 'Vender USD o EUR por VES',
            'url': URL('divisas', 'vender'),
            'icono': 'fas fa-hand-holding-usd',
            'color': 'warning'
        },
        {
            'titulo': 'Mis Cuentas',
            'descripcion': 'Consultar saldos y movimientos',
            'url': URL('cuentas', 'consultar'),
            'icono': 'fas fa-university',
            'color': 'info'
        },
        {
            'titulo': 'Historial',
            'descripcion': 'Ver historial de transacciones',
            'url': URL('divisas', 'historial_transacciones'),
            'icono': 'fas fa-history',
            'color': 'secondary'
        }
    ]

def generar_accesos_rapidos_admin():
    """Genera los accesos rápidos para administradores"""
    return [
        {
            'titulo': 'Comprar Divisas',
            'descripcion': 'Realizar compras de divisas',
            'url': URL('divisas', 'comprar'),
            'icono': 'fas fa-shopping-cart',
            'color': 'success'
        },
        {
            'titulo': 'Vender Divisas',
            'descripcion': 'Realizar ventas de divisas',
            'url': URL('divisas', 'vender'),
            'icono': 'fas fa-hand-holding-usd',
            'color': 'warning'
        },
        {
            'titulo': 'Gestión de Clientes',
            'descripcion': 'Administrar clientes del sistema',
            'url': URL('clientes', 'listar'),
            'icono': 'fas fa-users',
            'color': 'primary'
        },
        {
            'titulo': 'Reportes',
            'descripcion': 'Generar reportes del sistema',
            'url': URL('reportes', 'index'),
            'icono': 'fas fa-chart-bar',
            'color': 'info'
        },
        {
            'titulo': 'Tasas de Cambio',
            'descripcion': 'Gestionar tasas de cambio',
            'url': URL('api', 'index'),
            'icono': 'fas fa-exchange-alt',
            'color': 'secondary'
        },
        {
            'titulo': 'Configuración',
            'descripcion': 'Configurar parámetros del sistema',
            'url': URL('appadmin', 'index'),
            'icono': 'fas fa-cogs',
            'color': 'dark'
        }
    ]

def generar_breadcrumbs():
    """Genera breadcrumbs basados en el controlador y función actual"""
    breadcrumbs = [
        {'titulo': 'Inicio', 'url': URL('default', 'index'), 'activo': False}
    ]
    
    # Mapeo de controladores a títulos
    controladores = {
        'default': 'Dashboard',
        'clientes': 'Clientes',
        'cuentas': 'Cuentas',
        'divisas': 'Divisas',
        'reportes': 'Reportes',
        'api': 'Tasas BCV'
    }
    
    # Mapeo de funciones a títulos
    funciones = {
        'index': 'Inicio',
        'dashboard': 'Dashboard',
        'listar': 'Listado',
        'registrar': 'Registro',
        'perfil': 'Perfil',
        'crear': 'Crear',
        'consultar': 'Consultar',
        'movimientos': 'Movimientos',
        'comprar': 'Comprar',
        'vender': 'Vender',
        'historial_transacciones': 'Historial',
        'reportes_administrativos': 'Reportes Administrativos',
        'exportar': 'Exportar'
    }
    
    # Agregar breadcrumb del controlador si no es default
    if request.controller != 'default':
        titulo_controlador = controladores.get(request.controller, request.controller.title())
        breadcrumbs.append({
            'titulo': titulo_controlador,
            'url': URL(request.controller, 'index'),
            'activo': False
        })
    
    # Agregar breadcrumb de la función si no es index
    if request.function != 'index':
        titulo_funcion = funciones.get(request.function, request.function.replace('_', ' ').title())
        breadcrumbs.append({
            'titulo': titulo_funcion,
            'url': None,
            'activo': True
        })
    
    return breadcrumbs

# Hacer breadcrumbs disponibles globalmente
response.breadcrumbs = generar_breadcrumbs()

# ---- API para obtener datos del dashboard -----
@auth.requires_login()
def api_dashboard_data():
    """API para obtener datos actualizados del dashboard"""
    if not request.env.request_method == 'GET': 
        raise HTTP(403)
    
    user_id = auth.user.id
    cliente = db(db.clientes.user_id == user_id).select().first()
    
    if cliente:
        # Datos para cliente
        cuentas = db(db.cuentas.cliente_id == cliente.id).select()
        total_ves = sum([float(cuenta.saldo_ves or 0) for cuenta in cuentas])
        total_usd = sum([float(cuenta.saldo_usd or 0) for cuenta in cuentas])
        total_eur = sum([float(cuenta.saldo_eur or 0) for cuenta in cuentas])
        
        tasas = obtener_tasas_actuales()
        
        return response.json({
            'status': 'success',
            'data': {
                'total_ves': total_ves,
                'total_usd': total_usd,
                'total_eur': total_eur,
                'tasa_usd': float(tasas.usd_ves) if tasas else 0,
                'tasa_eur': float(tasas.eur_ves) if tasas else 0,
                'ultima_actualizacion': str(tasas.fecha) if tasas else None
            }
        })
    else:
        return response.json({'status': 'error', 'message': 'Cliente no encontrado'})

# ---- Función para obtener widget de tasas -----
def widget_tasas():
    """Renderiza el widget de tasas actuales"""
    tasas = obtener_tasas_actuales()
    return dict(tasas=tasas) 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

# -------------------------------------------------------------------------
# Funciones de Administración de Usuarios
# -------------------------------------------------------------------------

def admin_usuarios():
    """
    Página de administración de usuarios (solo para desarrollo)
    """
    
    # Crear primer administrador automáticamente
    if request.vars.crear_admin:
        exito, mensaje = crear_primer_administrador()
        if exito:
            session.flash = mensaje
        else:
            response.flash = mensaje
        redirect(URL('admin_usuarios'))
    
    # Aprobar usuario específico
    if request.vars.aprobar and request.vars.email:
        exito, mensaje = aprobar_usuario_pendiente(request.vars.email)
        if exito:
            session.flash = mensaje
        else:
            response.flash = mensaje
        redirect(URL('admin_usuarios'))
    
    # Listar usuarios pendientes
    usuarios_pendientes = listar_usuarios_pendientes()
    
    # Listar todos los usuarios
    todos_usuarios = db(db.auth_user.id > 0).select(
        db.auth_user.id,
        db.auth_user.email,
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.auth_user.registration_key,
        orderby=db.auth_user.id
    )
    
    return dict(
        usuarios_pendientes=usuarios_pendientes,
        todos_usuarios=todos_usuarios
    )