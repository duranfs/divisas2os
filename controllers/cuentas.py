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

# -------------------------------------------------------------------------
# Decoradores de autenticación y autorización
# -------------------------------------------------------------------------

@auth.requires_login()
def index():
    """Dashboard principal de cuentas del cliente"""
    # Obtener el cliente actual
    cliente = db(db.clientes.user_id == auth.user.id).select().first()
    
    if not cliente:
        session.flash = "Debe completar su registro como cliente primero"
        redirect(URL('clientes', 'registrar'))
    
    # Obtener todas las cuentas del cliente
    cuentas = db(db.cuentas.cliente_id == cliente.id).select(
        orderby=db.cuentas.fecha_creacion
    )
    
    # Calcular totales por moneda
    total_ves = sum([cuenta.saldo_ves or 0 for cuenta in cuentas])
    total_usd = sum([cuenta.saldo_usd or 0 for cuenta in cuentas])
    total_eur = sum([cuenta.saldo_eur or 0 for cuenta in cuentas])
    
    # Obtener tasas actuales para mostrar equivalencias
    tasa_actual = db(db.tasas_cambio.activa == True).select(
        orderby=~db.tasas_cambio.fecha | ~db.tasas_cambio.hora
    ).first()
    
    return dict(
        cuentas=cuentas,
        cliente=cliente,
        total_ves=total_ves,
        total_usd=total_usd,
        total_eur=total_eur,
        tasa_actual=tasa_actual
    )

@auth.requires_login()
def crear():
    """Crear nueva cuenta bancaria"""
    # Verificar que el usuario sea cliente registrado
    cliente = db(db.clientes.user_id == auth.user.id).select().first()
    
    if not cliente:
        session.flash = "Debe completar su registro como cliente primero"
        redirect(URL('clientes', 'registrar'))
    
    # Crear formulario
    form = SQLFORM(db.cuentas, fields=['tipo_cuenta'])
    form.vars.cliente_id = cliente.id
    
    if form.process().accepted:
        # Generar número de cuenta único
        numero_cuenta = generar_numero_cuenta()
        
        # Obtener el ID de la cuenta recién creada
        cuenta_id = form.vars.id
        if not cuenta_id:
            # Si no está disponible en form.vars, buscar la cuenta más reciente del cliente
            cuenta_reciente = db(db.cuentas.cliente_id == cliente.id).select(
                orderby=~db.cuentas.id,
                limitby=(0, 1)
            ).first()
            cuenta_id = cuenta_reciente.id if cuenta_reciente else None
        
        if cuenta_id:
            # Actualizar el registro con el número de cuenta generado
            db(db.cuentas.id == cuenta_id).update(numero_cuenta=numero_cuenta)
            session.flash = f"Cuenta creada exitosamente. Número: {numero_cuenta}"
        else:
            session.flash = "Cuenta creada pero no se pudo asignar número. Contacte al administrador."
        
        redirect(URL('cuentas', 'index'))
    elif form.errors:
        response.flash = "Por favor corrija los errores en el formulario"
    
    return dict(form=form, cliente=cliente)

@auth.requires_login()
def consultar():
    """Consultar saldos de una cuenta específica"""
    cuenta_id = request.args(0)
    
    if not cuenta_id:
        session.flash = "Debe especificar una cuenta"
        redirect(URL('cuentas', 'index'))
    
    # Verificar que la cuenta pertenezca al cliente actual
    cliente = db(db.clientes.user_id == auth.user.id).select().first()
    
    if not cliente:
        session.flash = "Acceso no autorizado"
        redirect(URL('default', 'index'))
    
    cuenta = db(
        (db.cuentas.id == cuenta_id) & 
        (db.cuentas.cliente_id == cliente.id)
    ).select().first()
    
    if not cuenta:
        session.flash = "Cuenta no encontrada o acceso no autorizado"
        redirect(URL('cuentas', 'index'))
    
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
    
    if not cuenta_id:
        session.flash = "Debe especificar una cuenta"
        redirect(URL('cuentas', 'index'))
    
    # Verificar que la cuenta pertenezca al cliente actual
    cliente = db(db.clientes.user_id == auth.user.id).select().first()
    
    if not cliente:
        session.flash = "Acceso no autorizado"
        redirect(URL('default', 'index'))
    
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
    """Ver detalles de una cuenta específica"""
    cuenta_id = request.args(0)
    
    if not cuenta_id:
        session.flash = "Debe especificar una cuenta"
        redirect(URL('cuentas', 'index'))
    
    # Verificar que la cuenta pertenezca al cliente actual
    cliente = db(db.clientes.user_id == auth.user.id).select().first()
    
    if not cliente:
        session.flash = "Acceso no autorizado"
        redirect(URL('default', 'index'))
    
    cuenta = db(
        (db.cuentas.id == cuenta_id) & 
        (db.cuentas.cliente_id == cliente.id)
    ).select().first()
    
    if not cuenta:
        session.flash = "Cuenta no encontrada o acceso no autorizado"
        redirect(URL('cuentas', 'index'))
    
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
    """Listar todas las cuentas del sistema (solo administradores)"""
    # Parámetros de búsqueda
    buscar = request.vars.buscar
    estado = request.vars.estado
    tipo = request.vars.tipo
    
    # Query base con JOIN para obtener datos del cliente
    query = (db.cuentas.cliente_id == db.clientes.id) & \
            (db.clientes.user_id == db.auth_user.id)
    
    # Aplicar filtros
    if buscar:
        query &= ((db.cuentas.numero_cuenta.contains(buscar)) |
                 (db.clientes.cedula.contains(buscar)) |
                 (db.auth_user.first_name.contains(buscar)) |
                 (db.auth_user.last_name.contains(buscar)))
    
    if estado and estado != 'todos':
        query &= (db.cuentas.estado == estado)
    
    if tipo and tipo != 'todos':
        query &= (db.cuentas.tipo_cuenta == tipo)
    
    # Obtener cuentas con paginación
    page = int(request.vars.page or 1)
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
    
    return dict(
        cuentas=cuentas,
        buscar=buscar,
        estado=estado,
        tipo=tipo,
        page=page,
        total_pages=total_pages,
        total_cuentas=total_cuentas
    )

@auth.requires_membership('administrador')
def gestionar():
    """Gestionar cuenta específica (solo administradores)"""
    cuenta_id = request.args(0)
    
    if not cuenta_id:
        session.flash = "Debe especificar una cuenta"
        redirect(URL('cuentas', 'listar_todas'))
    
    # Obtener cuenta con datos del cliente
    cuenta = db(
        (db.cuentas.id == cuenta_id) &
        (db.cuentas.cliente_id == db.clientes.id) &
        (db.clientes.user_id == db.auth_user.id)
    ).select(
        db.cuentas.ALL,
        db.clientes.cedula,
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.auth_user.email
    ).first()
    
    if not cuenta:
        session.flash = "Cuenta no encontrada"
        redirect(URL('cuentas', 'listar_todas'))
    
    # Formulario para editar estado y saldos
    form = SQLFORM(db.cuentas, cuenta.cuentas.id, 
                   fields=['estado', 'saldo_ves', 'saldo_usd', 'saldo_eur'],
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
        cuenta=cuenta,
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