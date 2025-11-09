#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para agregar el módulo de Remesas y Límites Diarios
Basado en mejores prácticas bancarias
"""

def generar_modelo_remesas():
    """Generar código para agregar al models/db.py"""
    
    modelo = """
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
    format='%(fecha)s - %(moneda)s'
)

# Validaciones
db.remesas_diarias.moneda.requires = IS_IN_SET(['USD', 'EUR', 'USDT'], 
                                                error_message='Moneda debe ser USD, EUR o USDT')
db.remesas_diarias.monto_recibido.requires = IS_DECIMAL_IN_RANGE(0, 999999999.99, 
                                                                  error_message='Monto inválido')
db.remesas_diarias.fecha.requires = IS_DATE(format='%Y-%m-%d')

# Índices para optimizar consultas
db.remesas_diarias._after_insert.append(lambda f, id: actualizar_disponibilidad_remesa(id))

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
    format='%(fecha)s - %(moneda)s'
)

# Validaciones
db.limites_venta.moneda.requires = IS_IN_SET(['USD', 'EUR', 'USDT'])
db.limites_venta.limite_diario.requires = IS_DECIMAL_IN_RANGE(0, 999999999.99)

# Índice único por fecha y moneda
db.limites_venta._after_insert.append(lambda f, id: verificar_limite_unico(f, id))

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
    format='%(tipo_movimiento)s - %(monto)s'
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
    format='%(tipo_alerta)s - %(moneda)s'
)

# =========================================================================
# FUNCIONES AUXILIARES PARA REMESAS
# =========================================================================

def actualizar_disponibilidad_remesa(remesa_id):
    \"\"\"Actualiza la disponibilidad de una remesa después de inserción\"\"\"
    remesa = db.remesas_diarias[remesa_id]
    if remesa:
        remesa.update_record(monto_disponible=remesa.monto_recibido)

def verificar_limite_unico(fields, id):
    \"\"\"Verifica que no exista otro límite activo para la misma fecha y moneda\"\"\"
    fecha = fields.get('fecha')
    moneda = fields.get('moneda')
    
    # Desactivar otros límites para la misma fecha y moneda
    db((db.limites_venta.fecha == fecha) & 
       (db.limites_venta.moneda == moneda) & 
       (db.limites_venta.id != id)).update(activo=False)

def obtener_disponibilidad_moneda(moneda, fecha=None):
    \"\"\"
    Obtiene la disponibilidad actual de una moneda
    Retorna: dict con monto_disponible, limite_diario, porcentaje_usado
    \"\"\"
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
    \"\"\"
    Registra un movimiento en el historial de remesas
    \"\"\"
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

def verificar_y_enviar_alertas(moneda, porcentaje_utilizado):
    \"\"\"
    Verifica si se deben enviar alertas por límites alcanzados
    \"\"\"
    fecha = request.now.date()
    limite = db((db.limites_venta.fecha == fecha) & 
                (db.limites_venta.moneda == moneda) &
                (db.limites_venta.activo == True)).select().first()
    
    if not limite:
        return
    
    # Alerta 80%
    if porcentaje_utilizado >= 80 and not limite.alerta_80_enviada:
        enviar_alerta_limite(moneda, 80, porcentaje_utilizado)
        limite.update_record(alerta_80_enviada=True)
    
    # Alerta 95%
    if porcentaje_utilizado >= 95 and not limite.alerta_95_enviada:
        enviar_alerta_limite(moneda, 95, porcentaje_utilizado)
        limite.update_record(alerta_95_enviada=True)

def enviar_alerta_limite(moneda, umbral, porcentaje_actual):
    \"\"\"
    Envía alerta cuando se alcanza un umbral de límite
    \"\"\"
    # Aquí se implementaría el envío de email o notificación
    logger.warning(f"ALERTA: Límite de {moneda} al {porcentaje_actual:.2f}% (umbral {umbral}%)")
"""
    
    return modelo

def generar_controlador_remesas():
    """Generar controlador de remesas"""
    
    controlador = """# -*- coding: utf-8 -*-
\"\"\"
Controlador de Remesas y Límites Diarios
Gestión de liquidez y control de ventas
\"\"\"

import logging
from decimal import Decimal
from datetime import datetime, timedelta

logger = logging.getLogger("web2py.app.divisas")

@auth.requires_membership('administrador')
def index():
    \"\"\"Dashboard de remesas y límites\"\"\"
    
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
    \"\"\"Registrar nueva remesa diaria\"\"\"
    
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
    \"\"\"Configurar límites de venta diarios\"\"\"
    
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
    \"\"\"Ver historial de movimientos de remesas\"\"\"
    
    # Filtros
    fecha_desde = request.vars.fecha_desde or (request.now.date() - timedelta(days=7))
    fecha_hasta = request.vars.fecha_hasta or request.now.date()
    moneda_filtro = request.vars.moneda or 'TODAS'
    
    query = (db.movimientos_remesas.fecha_movimiento >= fecha_desde) & \
            (db.movimientos_remesas.fecha_movimiento <= fecha_hasta)
    
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
    \"\"\"Calcular estadísticas del mes para una moneda\"\"\"
    
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
    \"\"\"Realizar ajuste manual en remesa\"\"\"
    
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
"""
    
    return controlador

if __name__ == "__main__":
    print("🏦 GENERANDO MÓDULO DE REMESAS Y LÍMITES DIARIOS")
    print("="*60)
    
    print("\n📝 Generando modelo de base de datos...")
    modelo = generar_modelo_remesas()
    
    with open("modelo_remesas.txt", 'w', encoding='utf-8') as f:
        f.write(modelo)
    print("✅ Modelo generado: modelo_remesas.txt")
    
    print("\n📝 Generando controlador...")
    controlador = generar_controlador_remesas()
    
    with open("controllers/remesas.py", 'w', encoding='utf-8') as f:
        f.write(controlador)
    print("✅ Controlador generado: controllers/remesas.py")
    
    print("\n✅ MÓDULO GENERADO EXITOSAMENTE")
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Agregar el contenido de modelo_remesas.txt al final de models/db.py")
    print("2. El controlador ya está en controllers/remesas.py")
    print("3. Crear las vistas en views/remesas/")
    print("4. Agregar al menú de navegación")
