# -*- coding: utf-8 -*-
"""
Controlador de Remesas y Límites Diarios
Gestión de liquidez y control de ventas
"""

import logging
import uuid
from decimal import Decimal
from datetime import datetime, timedelta

logger = logging.getLogger("web2py.app.divisas")

# =========================================================================
# FUNCIONES AUXILIARES
# =========================================================================

def generar_comprobante_unico(prefijo='TXN'):
    """
    Genera un número de comprobante único
    Formato: PREFIJO-YYYYMMDD-HHMMSS-UUID4
    """
    try:
        fecha_hora = datetime.now()
        fecha_str = fecha_hora.strftime("%Y%m%d")
        hora_str = fecha_hora.strftime("%H%M%S")
        uuid_corto = str(uuid.uuid4())[:8].upper()
        
        comprobante = f"{prefijo}-{fecha_str}-{hora_str}-{uuid_corto}"
        
        # Verificar que no exista (muy improbable, pero por seguridad)
        existe = db(db.transacciones.numero_comprobante == comprobante).count()
        if existe > 0:
            # Agregar timestamp adicional si existe
            timestamp = str(int(fecha_hora.timestamp()))[-4:]
            comprobante = f"{prefijo}-{fecha_str}-{hora_str}-{uuid_corto}-{timestamp}"
        
        return comprobante
        
    except Exception as e:
        logger.error(f"Error generando comprobante único: {str(e)}")
        return f"{prefijo}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

def obtener_disponibilidad_moneda(moneda, fecha=None):
    """
    Obtiene la disponibilidad actual de una moneda SUMANDO todas las remesas activas del día
    Integrado con sistema de cuentas por moneda
    Requirement: 7.4
    Retorna: dict con monto_disponible, limite_diario, porcentaje_usado
    """
    if not fecha:
        fecha = request.now.date()
    
    # Obtener TODAS las remesas activas del día para esta moneda
    # Nota: activa se guarda como 'T' en SQLite, no como True
    remesas = db((db.remesas_diarias.fecha == fecha) & 
                 (db.remesas_diarias.moneda == moneda) &
                 (db.remesas_diarias.activa == 'T')).select()
    
    # SUMAR todos los montos de todas las remesas
    total_recibido = sum([float(r.monto_recibido) for r in remesas]) if remesas else 0
    total_disponible = sum([float(r.monto_disponible) for r in remesas]) if remesas else 0
    total_vendido = sum([float(r.monto_vendido) for r in remesas]) if remesas else 0
    
    # Obtener límite del día
    limite = db((db.limites_venta.fecha == fecha) & 
                (db.limites_venta.moneda == moneda) &
                (db.limites_venta.activo == True)).select().first()
    
    # Calcular total en cuentas de clientes (solo para moneda USD)
    total_en_cuentas = 0
    if moneda == 'USD':
        cuentas_usd = db(
            (db.cuentas.moneda == 'USD') &
            (db.cuentas.estado == 'activa')
        ).select()
        total_en_cuentas = sum([float(c.saldo) for c in cuentas_usd]) if cuentas_usd else 0
    
    resultado = {
        'moneda': moneda,
        'fecha': fecha,
        'remesa_disponible': total_disponible,
        'remesa_total': total_recibido,
        'remesa_vendido': total_vendido,
        'total_en_cuentas': total_en_cuentas,
        'limite_diario': float(limite.limite_diario) if limite else 0,
        'limite_vendido': float(limite.monto_vendido) if limite else 0,
        'limite_disponible': float(limite.monto_disponible) if limite else 0,
        'porcentaje_limite': float(limite.porcentaje_utilizado) if limite else 0,
        'puede_vender': True
    }
    
    # Determinar si se puede vender
    if total_disponible <= 0:
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
    
    # Obtener remesas del día AGRUPADAS por moneda
    remesas_raw = db(
        (db.remesas_diarias.fecha == fecha_hoy) &
        (db.remesas_diarias.activa == 'T')
    ).select(orderby=db.remesas_diarias.moneda)
    
    # Agrupar y sumar remesas por moneda
    remesas_agrupadas = {}
    for remesa in remesas_raw:
        moneda = remesa.moneda
        if moneda not in remesas_agrupadas:
            remesas_agrupadas[moneda] = {
                'moneda': moneda,
                'monto_recibido': 0,
                'monto_disponible': 0,
                'monto_vendido': 0,
                'fuente_remesa': [],
                'fecha': remesa.fecha
            }
        remesas_agrupadas[moneda]['monto_recibido'] += float(remesa.monto_recibido)
        remesas_agrupadas[moneda]['monto_disponible'] += float(remesa.monto_disponible)
        remesas_agrupadas[moneda]['monto_vendido'] += float(remesa.monto_vendido)
        if remesa.fuente_remesa:
            remesas_agrupadas[moneda]['fuente_remesa'].append(remesa.fuente_remesa)
    
    # Convertir a lista para la vista
    remesas_hoy = [remesas_agrupadas[m] for m in sorted(remesas_agrupadas.keys())]
    
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
    """
    Registrar nueva remesa diaria - Versión SIMPLE sin lógica de suma
    Integrado con sistema de cuentas por moneda
    Requirements: 7.1, 7.2
    """
    
    # Ocultar campos calculados
    db.remesas_diarias.monto_disponible.readable = False
    db.remesas_diarias.monto_disponible.writable = False
    db.remesas_diarias.monto_vendido.readable = False
    db.remesas_diarias.monto_vendido.writable = False
    db.remesas_diarias.monto_reservado.readable = False
    db.remesas_diarias.monto_reservado.writable = False
    db.remesas_diarias.usuario_registro.readable = False
    db.remesas_diarias.usuario_registro.writable = False
    db.remesas_diarias.fecha_registro.readable = False
    db.remesas_diarias.fecha_registro.writable = False
    db.remesas_diarias.activa.readable = False
    db.remesas_diarias.activa.writable = False
    
    form = SQLFORM(db.remesas_diarias)
    
    if form.process().accepted:
        # Obtener el ID y monto de la remesa recién creada
        remesa_id = form.vars.id
        monto_recibido = form.vars.monto_recibido
        moneda = form.vars.moneda
        
        # Leer el registro recién creado
        remesa = db.remesas_diarias[remesa_id]
        
        # Actualizar SOLO si monto_disponible no es correcto
        if remesa.monto_disponible != monto_recibido:
            remesa.update_record(
                monto_disponible=monto_recibido,
                monto_vendido=0,
                monto_reservado=0,
                usuario_registro=auth.user_id,
                fecha_registro=request.now,
                activa='T'
            )
        
        logger.info(f"Remesa registrada: {moneda} ${float(monto_recibido):,.2f} - ID: {remesa_id}")
        
        session.flash = f'✅ Remesa de {moneda} por ${float(monto_recibido):,.2f} registrada'
        redirect(URL('index'))
    
    return dict(form=form)

@auth.requires_membership('administrador')
def recibir_remesa_cliente():
    """
    Recibir remesa para un cliente específico
    Acredita el monto en la cuenta USD del cliente
    Requirements: 7.1, 7.2, 7.3
    """
    try:
        # Obtener parámetros
        cliente_id = request.vars.cliente_id
        monto_usd = request.vars.monto_usd
        referencia = request.vars.referencia or ''
        observaciones = request.vars.observaciones or ''
        
        if not cliente_id or not monto_usd:
            session.flash = '❌ Faltan parámetros requeridos'
            redirect(URL('index'))
        
        monto_usd = Decimal(str(monto_usd))
        
        if monto_usd <= 0:
            session.flash = '❌ El monto debe ser mayor a cero'
            redirect(URL('index'))
        
        # Obtener cliente
        cliente = db.clientes[cliente_id]
        if not cliente:
            session.flash = '❌ Cliente no encontrado'
            redirect(URL('index'))
        
        # Buscar cuenta USD del cliente
        cuenta_usd = db(
            (db.cuentas.cliente_id == cliente_id) &
            (db.cuentas.moneda == 'USD') &
            (db.cuentas.estado == 'activa')
        ).select().first()
        
        # Si no existe, crear cuenta USD automáticamente
        if not cuenta_usd:
            from models.db import generar_numero_cuenta_por_moneda
            numero_cuenta = generar_numero_cuenta_por_moneda('USD')
            
            cuenta_usd_id = db.cuentas.insert(
                cliente_id=cliente_id,
                numero_cuenta=numero_cuenta,
                tipo_cuenta='corriente',
                moneda='USD',
                saldo=Decimal('0.0'),
                estado='activa',
                fecha_creacion=request.now
            )
            cuenta_usd = db.cuentas[cuenta_usd_id]
            logger.info(f"Cuenta USD creada automáticamente para cliente {cliente_id}: {numero_cuenta}")
        
        # Acreditar monto en cuenta USD
        nuevo_saldo = cuenta_usd.saldo + monto_usd
        cuenta_usd.update_record(
            saldo=nuevo_saldo,
            fecha_actualizacion=request.now
        )
        
        # Registrar transacción de remesa
        comprobante = generar_comprobante_unico('REM')
        
        db.transacciones.insert(
            cuenta_destino_id=cuenta_usd.id,
            tipo_operacion='remesa',
            moneda_destino='USD',
            monto_destino=monto_usd,
            comprobante=comprobante,
            estado='completada',
            fecha_transaccion=request.now
        )
        
        # Registrar en log de auditoría
        db.logs_auditoria.insert(
            usuario_id=auth.user_id,
            accion='RECEPCION_REMESA',
            tabla='cuentas',
            registro_id=cuenta_usd.id,
            detalles=f"Remesa recibida: ${float(monto_usd):,.2f} USD - Cliente: {cliente.nombre} {cliente.apellido} - Ref: {referencia}",
            ip_address=request.client
        )
        
        logger.info(f"Remesa recibida - Cliente: {cliente_id}, Monto: ${float(monto_usd):,.2f} USD, Cuenta: {cuenta_usd.numero_cuenta}")
        
        session.flash = f'✅ Remesa de ${float(monto_usd):,.2f} USD acreditada en cuenta {cuenta_usd.numero_cuenta}'
        redirect(URL('index'))
        
    except Exception as e:
        logger.error(f"Error recibiendo remesa: {str(e)}")
        session.flash = f'❌ Error: {str(e)}'
        redirect(URL('index'))

@auth.requires_membership('administrador')
def configurar_limites():
    """Configurar límites de venta diarios - Vista simplificada"""
    # Redirigir a la vista simple que ya existe
    redirect(URL('configurar_limites_simple'))

@auth.requires_membership('administrador')
def historial_movimientos():
    """Ver historial de movimientos de remesas"""
    import datetime
    
    # Obtener parámetros de filtro
    fecha_desde = request.vars.fecha_desde or (datetime.date.today() - datetime.timedelta(days=30))
    fecha_hasta = request.vars.fecha_hasta or datetime.date.today()
    tipo_filtro = request.vars.tipo or 'TODOS'
    
    # Construir query base
    query = (db.movimientos_remesas.id > 0)
    
    # Aplicar filtros de fecha si están presentes
    if fecha_desde:
        if isinstance(fecha_desde, str):
            fecha_desde = datetime.datetime.strptime(fecha_desde, '%Y-%m-%d').date()
        query &= (db.movimientos_remesas.fecha_movimiento >= fecha_desde)
    
    if fecha_hasta:
        if isinstance(fecha_hasta, str):
            fecha_hasta = datetime.datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
        # Incluir todo el día hasta
        fecha_hasta_fin = datetime.datetime.combine(fecha_hasta, datetime.time(23, 59, 59))
        query &= (db.movimientos_remesas.fecha_movimiento <= fecha_hasta_fin)
    
    # Filtrar por tipo si no es TODOS
    if tipo_filtro and tipo_filtro != 'TODOS':
        query &= (db.movimientos_remesas.tipo_movimiento == tipo_filtro)
    
    # Consultar movimientos con join a remesas_diarias
    movimientos = db(query).select(
        db.movimientos_remesas.ALL,
        db.remesas_diarias.moneda,
        left=db.remesas_diarias.on(db.movimientos_remesas.remesa_id == db.remesas_diarias.id),
        orderby=~db.movimientos_remesas.fecha_movimiento,
        limitby=(0, 100)
    )
    
    return dict(
        movimientos=movimientos,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        tipo_filtro=tipo_filtro
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
        logger.info(f"configurar_limite_simple llamado. request.vars: {request.vars}")
        
        if request.vars.moneda and request.vars.limite_diario:
            moneda = request.vars.moneda
            limite_diario = float(request.vars.limite_diario)
            fecha = request.now.date()
            
            logger.info(f"Configurando límite: {moneda} = ${limite_diario} para {fecha}")
            
            # Validar que existen remesas y sumar el total disponible
            remesas = db(
                (db.remesas_diarias.fecha == fecha) &
                (db.remesas_diarias.moneda == moneda) &
                (db.remesas_diarias.activa == 'T')
            ).select()
            
            if not remesas:
                response.flash = f"❌ No hay remesa de {moneda} para hoy. Registra una remesa primero."
                redirect(URL('configurar_limites_simple'))
            
            # Sumar el total disponible de todas las remesas
            total_disponible = sum([float(r.monto_disponible) for r in remesas])
            
            # Validar que el límite no exceda el total disponible
            if limite_diario > total_disponible:
                response.flash = f"❌ El límite no puede exceder la remesa disponible (${total_disponible:,.2f})"
                redirect(URL('configurar_limites_simple'))
            
            # *** DESACTIVAR TODOS LOS LÍMITES ANTERIORES DE ESTA MONEDA ***
            db(
                (db.limites_venta.fecha == fecha) &
                (db.limites_venta.moneda == moneda)
            ).update(activo='F')
            
            # *** CREAR NUEVO LÍMITE LIMPIO ***
            db.limites_venta.insert(
                fecha=fecha,
                moneda=moneda,
                limite_diario=limite_diario,
                monto_vendido=0.00,
                monto_disponible=limite_diario,
                porcentaje_utilizado=0.0,
                activo='T',
                alerta_80_enviada='F',
                alerta_95_enviada='F'
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
