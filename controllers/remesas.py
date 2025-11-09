# -*- coding: utf-8 -*-
"""
Controlador de Remesas y Límites Diarios
Gestión de liquidez y control de ventas
"""

import logging
from decimal import Decimal
from datetime import datetime, timedelta

logger = logging.getLogger("web2py.app.divisas")

# =========================================================================
# FUNCIONES AUXILIARES
# =========================================================================

def obtener_disponibilidad_moneda(moneda, fecha=None):
    """
    Obtiene la disponibilidad actual de una moneda
    Retorna: dict con monto_disponible, limite_diario, porcentaje_usado
    """
    if not fecha:
        fecha = request.now.date()
    
    # Obtener remesa del día
    remesa = db((db.remesas_diarias.fecha == fecha) & 
                (db.remesas_diarias.moneda == moneda) &
                (db.remesas_diarias.activa == True)).select().first()
    
    # Obtener límite del día
    limite = db((db.limites_venta.fecha == fecha) & 
                (db.limites_venta.moneda == moneda) &
                (db.limites_venta.activo == True)).select().first()
    
    resultado = {
        'moneda': moneda,
        'fecha': fecha,
        'remesa_disponible': float(remesa.monto_disponible) if remesa else 0,
        'remesa_total': float(remesa.monto_recibido) if remesa else 0,
        'remesa_vendido': float(remesa.monto_vendido) if remesa else 0,
        'limite_diario': float(limite.limite_diario) if limite else 0,
        'limite_vendido': float(limite.monto_vendido) if limite else 0,
        'limite_disponible': float(limite.monto_disponible) if limite else 0,
        'porcentaje_limite': float(limite.porcentaje_utilizado) if limite else 0,
        'puede_vender': True
    }
    
    # Determinar si se puede vender
    if remesa and remesa.monto_disponible <= 0:
        resultado['puede_vender'] = False
        resultado['razon'] = 'Sin remesa disponible'
    elif limite and limite.monto_disponible <= 0:
        resultado['puede_vender'] = False
        resultado['razon'] = 'Límite diario alcanzado'
    
    return resultado

def registrar_movimiento_remesa(remesa_id, tipo_movimiento, monto, descripcion='', transaccion_id=None):
    """
    Registra un movimiento en el historial de remesas
    """
    remesa = db.remesas_diarias[remesa_id]
    if not remesa:
        return False
    
    saldo_anterior = remesa.monto_disponible
    
    # Calcular nuevo saldo según tipo de movimiento
    if tipo_movimiento in ['VENTA', 'AJUSTE']:
        saldo_nuevo = saldo_anterior - monto
    elif tipo_movimiento in ['RECEPCION', 'DEVOLUCION', 'LIBERACION']:
        saldo_nuevo = saldo_anterior + monto
    else:
        saldo_nuevo = saldo_anterior
    
    # Registrar movimiento
    db.movimientos_remesas.insert(
        remesa_id=remesa_id,
        tipo_movimiento=tipo_movimiento,
        monto=monto,
        saldo_anterior=saldo_anterior,
        saldo_nuevo=saldo_nuevo,
        transaccion_id=transaccion_id,
        descripcion=descripcion,
        usuario=auth.user_id if auth.user else None,
        ip_address=request.client
    )
    
    # Actualizar remesa
    remesa.update_record(monto_disponible=saldo_nuevo)
    
    return True

def calcular_estadisticas_mes(moneda, fecha_desde, fecha_hasta):
    """Calcular estadísticas del mes para una moneda"""
    
    remesas_mes = db(
        (db.remesas_diarias.fecha >= fecha_desde) &
        (db.remesas_diarias.fecha <= fecha_hasta) &
        (db.remesas_diarias.moneda == moneda)
    ).select()
    
    total_recibido = sum([float(r.monto_recibido) for r in remesas_mes])
    total_vendido = sum([float(r.monto_vendido) for r in remesas_mes])
    
    return {
        'total_recibido': total_recibido,
        'total_vendido': total_vendido,
        'disponible': total_recibido - total_vendido,
        'dias_con_remesas': len(remesas_mes),
        'promedio_diario': total_recibido / len(remesas_mes) if remesas_mes else 0
    }

# =========================================================================
# CONTROLADORES
# =========================================================================

@auth.requires_membership('administrador')
def index():
    """Dashboard de remesas y límites"""
    
    fecha_hoy = request.now.date()
    
    # Obtener disponibilidad de cada moneda
    disponibilidad_usd = obtener_disponibilidad_moneda('USD', fecha_hoy)
    disponibilidad_eur = obtener_disponibilidad_moneda('EUR', fecha_hoy)
    disponibilidad_usdt = obtener_disponibilidad_moneda('USDT', fecha_hoy)
    
    # Obtener remesas del día
    remesas_hoy = db(
        (db.remesas_diarias.fecha == fecha_hoy) &
        (db.remesas_diarias.activa == True)
    ).select(orderby=db.remesas_diarias.moneda)
    
    # Obtener límites del día
    limites_hoy = db(
        (db.limites_venta.fecha == fecha_hoy) &
        (db.limites_venta.activo == True)
    ).select(orderby=db.limites_venta.moneda)
    
    # Estadísticas del mes
    primer_dia_mes = fecha_hoy.replace(day=1)
    
    stats_mes = {
        'USD': calcular_estadisticas_mes('USD', primer_dia_mes, fecha_hoy),
        'EUR': calcular_estadisticas_mes('EUR', primer_dia_mes, fecha_hoy),
        'USDT': calcular_estadisticas_mes('USDT', primer_dia_mes, fecha_hoy)
    }
    
    return dict(
        disponibilidad_usd=disponibilidad_usd,
        disponibilidad_eur=disponibilidad_eur,
        disponibilidad_usdt=disponibilidad_usdt,
        remesas_hoy=remesas_hoy,
        limites_hoy=limites_hoy,
        stats_mes=stats_mes,
        fecha_hoy=fecha_hoy
    )

@auth.requires_membership('administrador')
def registrar_remesa():
    """Registrar nueva remesa diaria"""
    
    form = SQLFORM(db.remesas_diarias)
    form.vars.usuario_registro = auth.user_id
    
    if form.process().accepted:
        remesa_id = form.vars.id
        
        # Registrar movimiento
        registrar_movimiento_remesa(
            remesa_id=remesa_id,
            tipo_movimiento='RECEPCION',
            monto=form.vars.monto_recibido,
            descripcion=f"Remesa recibida: {form.vars.fuente_remesa or 'N/A'}"
        )
        
        session.flash = f'Remesa de {form.vars.moneda} registrada exitosamente'
        redirect(URL('index'))
    
    return dict(form=form)

@auth.requires_membership('administrador')
def configurar_limites():
    """Configurar límites de venta diarios"""
    
    if request.vars.fecha and request.vars.moneda:
        # Formulario específico para fecha y moneda
        fecha = request.vars.fecha
        moneda = request.vars.moneda
        
        # Buscar límite existente
        limite_existente = db(
            (db.limites_venta.fecha == fecha) &
            (db.limites_venta.moneda == moneda) &
            (db.limites_venta.activo == True)
        ).select().first()
        
        if limite_existente:
            form = SQLFORM(db.limites_venta, limite_existente, showid=False)
        else:
            form = SQLFORM(db.limites_venta)
            form.vars.fecha = fecha
            form.vars.moneda = moneda
    else:
        form = SQLFORM(db.limites_venta)
    
    form.vars.usuario_configuracion = auth.user_id
    
    if form.process().accepted:
        session.flash = 'Límite configurado exitosamente'
        redirect(URL('index'))
    
    return dict(form=form)

@auth.requires_membership('administrador')
def historial_movimientos():
    """Ver historial de movimientos de remesas"""
    
    # Filtros
    fecha_desde = request.vars.fecha_desde or (request.now.date() - timedelta(days=7))
    fecha_hasta = request.vars.fecha_hasta or request.now.date()
    moneda_filtro = request.vars.moneda or 'TODAS'
    
    query = (db.movimientos_remesas.fecha_movimiento >= fecha_desde) &             (db.movimientos_remesas.fecha_movimiento <= fecha_hasta)
    
    if moneda_filtro != 'TODAS':
        query &= (db.remesas_diarias.moneda == moneda_filtro)
    
    movimientos = db(query).select(
        db.movimientos_remesas.ALL,
        db.remesas_diarias.moneda,
        db.remesas_diarias.fecha,
        left=db.remesas_diarias.on(
            db.movimientos_remesas.remesa_id == db.remesas_diarias.id
        ),
        orderby=~db.movimientos_remesas.fecha_movimiento,
        limitby=(0, 100)
    )
    
    return dict(
        movimientos=movimientos,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        moneda_filtro=moneda_filtro
    )

def calcular_estadisticas_mes(moneda, fecha_desde, fecha_hasta):
    """Calcular estadísticas del mes para una moneda"""
    
    remesas_mes = db(
        (db.remesas_diarias.fecha >= fecha_desde) &
        (db.remesas_diarias.fecha <= fecha_hasta) &
        (db.remesas_diarias.moneda == moneda)
    ).select()
    
    total_recibido = sum([float(r.monto_recibido) for r in remesas_mes])
    total_vendido = sum([float(r.monto_vendido) for r in remesas_mes])
    
    return {
        'total_recibido': total_recibido,
        'total_vendido': total_vendido,
        'disponible': total_recibido - total_vendido,
        'dias_con_remesas': len(remesas_mes),
        'promedio_diario': total_recibido / len(remesas_mes) if remesas_mes else 0
    }

@auth.requires_membership('administrador')
def ajustar_remesa():
    """Realizar ajuste manual en remesa"""
    
    remesa_id = request.vars.remesa_id
    if not remesa_id:
        session.flash = 'Remesa no especificada'
        redirect(URL('index'))
    
    remesa = db.remesas_diarias[remesa_id]
    if not remesa:
        session.flash = 'Remesa no encontrada'
        redirect(URL('index'))
    
    form = FORM(
        DIV(
            LABEL('Tipo de Ajuste:'),
            SELECT('INCREMENTO', 'DECREMENTO', _name='tipo_ajuste', _class='form-control'),
            _class='form-group'
        ),
        DIV(
            LABEL('Monto:'),
            INPUT(_name='monto', _type='number', _step='0.01', _class='form-control', requires=IS_NOT_EMPTY()),
            _class='form-group'
        ),
        DIV(
            LABEL('Motivo:'),
            TEXTAREA(_name='motivo', _class='form-control', _rows=3, requires=IS_NOT_EMPTY()),
            _class='form-group'
        ),
        INPUT(_type='submit', _value='Realizar Ajuste', _class='btn btn-warning')
    )
    
    if form.process().accepted:
        tipo = form.vars.tipo_ajuste
        monto = Decimal(str(form.vars.monto))
        motivo = form.vars.motivo
        
        if tipo == 'INCREMENTO':
            registrar_movimiento_remesa(
                remesa_id=remesa_id,
                tipo_movimiento='AJUSTE',
                monto=-monto,  # Negativo para incrementar
                descripcion=f"Ajuste manual (incremento): {motivo}"
            )
        else:
            registrar_movimiento_remesa(
                remesa_id=remesa_id,
                tipo_movimiento='AJUSTE',
                monto=monto,
                descripcion=f"Ajuste manual (decremento): {motivo}"
            )
        
        session.flash = 'Ajuste realizado exitosamente'
        redirect(URL('index'))
    
    return dict(form=form, remesa=remesa)


@auth.requires_membership('administrador')
def configurar_limite_simple():
    """
    Configurar límite de forma simple - solo el monto máximo
    El sistema calcula automáticamente vendido y disponible
    """
    try:
        if request.vars.moneda and request.vars.limite_diario:
            moneda = request.vars.moneda
            limite_diario = float(request.vars.limite_diario)
            fecha = request.now.date()
            
            # Validar que existe remesa
            remesa = db(
                (db.remesas_diarias.fecha == fecha) &
                (db.remesas_diarias.moneda == moneda) &
                (db.remesas_diarias.activa == True)
            ).select().first()
            
            if not remesa:
                response.flash = f"❌ No hay remesa de {moneda} para hoy. Registra una remesa primero."
                redirect(URL('configurar_limites_simple'))
            
            # Validar que el límite no exceda la remesa
            if limite_diario > float(remesa.monto_disponible):
                response.flash = f"❌ El límite no puede exceder la remesa disponible (${remesa.monto_disponible:,.2f})"
                redirect(URL('configurar_limites_simple'))
            
            # *** DESACTIVAR TODOS LOS LÍMITES ANTERIORES DE ESTA MONEDA ***
            db(
                (db.limites_venta.fecha == fecha) &
                (db.limites_venta.moneda == moneda)
            ).update(activo=False)
            
            # *** CREAR NUEVO LÍMITE LIMPIO ***
            db.limites_venta.insert(
                fecha=fecha,
                moneda=moneda,
                limite_diario=limite_diario,
                monto_vendido=0.00,
                monto_disponible=limite_diario,
                porcentaje_utilizado=0.0,
                activo=True,
                alerta_80_enviada=False,
                alerta_95_enviada=False
            )
            
            response.flash = f"✅ Límite de {moneda} configurado: ${limite_diario:,.2f}"
            
            db.commit()
        
        redirect(URL('configurar_limites_simple'))
        
    except Exception as e:
        logger.error(f"Error configurando límite simple: {str(e)}")
        response.flash = f"❌ Error: {str(e)}"
        redirect(URL('configurar_limites_simple'))

@auth.requires_membership('administrador')
def configurar_limites_simple():
    """Vista simple para configurar límites"""
    return dict()
