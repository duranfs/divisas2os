# -*- coding: utf-8 -*-
"""
Controlador de Divisas - Sistema de Divisas Bancario
Maneja las operaciones de compra y venta de divisas
"""

import logging
import datetime
import uuid
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json

# Configurar logging
logger = logging.getLogger("web2py.app.divisas")

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

def index():
    """
    Página principal del módulo de divisas
    Muestra las tasas actuales y opciones de transacción
    """
    try:
        # Obtener tasas actuales
        tasas = obtener_tasas_actuales()
        
        # Obtener cuentas del cliente actual si está autenticado
        cuentas_cliente = []
        if auth.user:
            cliente = db(db.clientes.user_id == auth.user.id).select().first()
            if cliente:
                cuentas_cliente = db(
                    (db.cuentas.cliente_id == cliente.id) & 
                    (db.cuentas.estado == 'activa')
                ).select()
        
        return dict(
            tasas=tasas,
            cuentas=cuentas_cliente,
            mensaje="Sistema de Divisas - Compra y Venta"
        )
        
    except Exception as e:
        logger.error(f"Error en index de divisas: {str(e)}")
        response.flash = f"Error cargando módulo de divisas: {str(e)}"
        return dict(
            tasas=None,
            cuentas=[],
            mensaje="Error en el sistema"
        )

@auth.requires_login()
def comprar():
    """
    Función de compra de divisas ultra-simplificada
    """
    try:
        # Procesamiento de compra
        if request.vars.confirmar_compra:
            try:
                logger.info(f"Procesando compra REAL para usuario: {auth.user.email}")
                
                # Obtener datos del formulario
                cuenta_id = request.vars.cuenta_id
                moneda_destino = request.vars.moneda_destino
                cantidad_divisa = request.vars.cantidad_divisa
                
                # Validación básica
                if not cuenta_id or not moneda_destino or not cantidad_divisa:
                    response.flash = "❌ Faltan datos requeridos"
                else:
                    # PROCESAR COMPRA REAL - no simular
                    logger.info(f"Llamando a procesar_compra_divisa() con datos: cuenta_id={cuenta_id}, moneda_destino={moneda_destino}, cantidad_divisa={cantidad_divisa}")
                    
                    resultado = procesar_compra_divisa()
                    logger.info(f"Resultado de procesar_compra_divisa(): {resultado}")
                    
                    if resultado.get('success'):
                        comprobante = resultado.get('comprobante')
                        session.ultimo_comprobante = comprobante
                        response.flash = f"✅ Compra realizada exitosamente! Comprobante: {comprobante}"
                        
                        # Usar raise HTTP en lugar de redirect para evitar el error 303
                        raise HTTP(303, "See Other", Location=URL('divisas', 'compra_exitosa', vars={'comprobante': comprobante}))
                    else:
                        error_msg = resultado.get('error', 'Error desconocido')
                        logger.error(f"Error en compra: {error_msg}")
                        response.flash = f"❌ Error en la compra: {error_msg}"
                    
            except HTTP:
                # Re-raise HTTP exceptions (redirects)
                raise
            except Exception as e_proc:
                logger.error(f"Error procesando compra: {str(e_proc)}")
                response.flash = f"❌ Error procesando la compra: {str(e_proc)}"
        
        # Obtener datos para mostrar el formulario
        cliente = db(db.clientes.user_id == auth.user.id).select().first()
        
        # Si no hay cliente, crear uno básico para administradores
        if not cliente and auth.has_membership('administrador'):
            cliente = db(db.clientes.id > 0).select().first()
        
        # Obtener cuentas
        if cliente:
            cuentas = db((db.cuentas.cliente_id == cliente.id) & (db.cuentas.estado == 'activa')).select()
        else:
            cuentas = []
        
        # Tasas básicas
        tasas = {'usd_ves': 36.50, 'eur_ves': 40.25}
        
        return dict(
            cuentas=cuentas,
            tasas=tasas,
            cliente=cliente
        )
        
    except HTTP:
        # Re-raise HTTP exceptions (redirects)
        raise
    except Exception as e:
        logger.error(f"Error general en comprar: {str(e)}")
        response.flash = f"Error: {str(e)}"
        return dict(cuentas=[], tasas={'usd_ves': 36.50, 'eur_ves': 40.25}, cliente=None)

@auth.requires_login()
# @requiere_permiso('create', 'transacciones')  # Temporalmente deshabilitado para testing
def vender():
    """
    Función de venta de divisas
    Requisitos: 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 5.4
    """
    try:
        # Crear datos de prueba si es administrador y no hay datos
        if auth.has_membership('administrador') and not db(db.clientes.id > 0).select().first():
            crear_datos_prueba_admin()
        # Verificar que el usuario tenga un perfil de cliente o sea administrador
        cliente = db(db.clientes.user_id == auth.user.id).select().first()
        
        # Si es administrador y no tiene perfil de cliente, crear uno temporal o permitir transacciones
        if not cliente and (auth.has_membership('administrador') or auth.has_membership('operador')):
            # Para administradores, buscar cualquier cliente existente para usar sus cuentas
            cliente = db(db.clientes.id > 0).select().first()
            if not cliente:
                response.flash = "No hay clientes registrados en el sistema para realizar transacciones de prueba"
                redirect(URL('clientes', 'registrar'))
        elif not cliente:
            response.flash = "Debe completar su registro como cliente para realizar transacciones"
            redirect(URL('clientes', 'registrar'))
        
        # Obtener cuentas activas del cliente
        cuentas = db(
            (db.cuentas.cliente_id == cliente.id) & 
            (db.cuentas.estado == 'activa')
        ).select()
        
        if not cuentas:
            response.flash = "Debe tener al menos una cuenta activa para realizar transacciones"
            redirect(URL('cuentas', 'crear'))
        
        # Obtener tasas actuales
        tasas = obtener_tasas_actuales()
        
        # Debug: verificar si se está enviando el formulario
        if request.vars.confirmar_venta:
            logger.info(f"Procesando venta para usuario: {auth.user.email}")
            # Procesar la venta
            resultado = procesar_venta_divisa()
            if resultado['success']:
                comprobante = resultado.get('comprobante', 'N/A')
                transaccion_id = resultado.get('transaccion_id')
                
                logger.info(f"Venta exitosa - Transacción ID: {transaccion_id}, Comprobante: {comprobante}")
                session.ultimo_comprobante = comprobante
                
                # Redirigir a la página de comprobante usando raise HTTP
                # El ID va como args, no como vars
                raise HTTP(303, "See Other", Location=URL('divisas', 'comprobante', args=[transaccion_id]))
            else:
                response.flash = f"❌ Error en la venta: {resultado['error']}"
        else:
            logger.info(f"Mostrando formulario de venta para usuario: {auth.user.email}")
        
        return dict(
            cuentas=cuentas,
            tasas=tasas,
            cliente=cliente
        )
    
    except HTTP:
        # Re-raise HTTP exceptions (redirects)
        raise
    except Exception as e:
        logger.error(f"Error en venta de divisas: {str(e)}")
        response.flash = f"Error procesando venta: {str(e)}"
        redirect(URL('divisas', 'index'))

def procesar_compra_divisa():
    """
    Procesa una transacción de compra de divisas
    Implementa validación de fondos y generación de comprobantes únicos
    """
    try:
        # Obtener parámetros de la transacción
        cuenta_id = request.vars.cuenta_id
        moneda_destino = request.vars.moneda_destino  # USD o EUR
        
        # Nuevo: obtener cantidad de divisa y calcular monto en VES
        # IMPORTANTE: Guardar la tasa que se usará para todo el cálculo
        tasa_a_usar = None
        
        if request.vars.cantidad_divisa:
            cantidad_divisa = Decimal(str(request.vars.cantidad_divisa))
            # Obtener tasas para transacciones (con compra/venta)
            tasas = obtener_tasas_para_transacciones()
            if not tasas or moneda_destino not in tasas:
                return {'success': False, 'error': f'No se pudo obtener la tasa para {moneda_destino}'}
            
            tasa_compra = Decimal(str(tasas[moneda_destino]['compra']))
            tasa_a_usar = tasa_compra  # Guardar para usar después
            monto_origen = cantidad_divisa * tasa_compra  # Calcular VES necesarios
        else:
            # Compatibilidad con método anterior
            monto_origen = Decimal(str(request.vars.monto_origen))  # Monto en VES
        
        # Validaciones básicas
        if not cuenta_id or not moneda_destino or not monto_origen:
            return {'success': False, 'error': 'Faltan parámetros requeridos'}
        
        if moneda_destino not in ['USD', 'EUR', 'USDT']:
            return {'success': False, 'error': 'Moneda destino debe ser USD, EUR o USDT'}
        
        if monto_origen <= 0:
            return {'success': False, 'error': 'El monto debe ser mayor a cero'}
        
        # Verificar que la cuenta pertenece al usuario actual o es administrador
        cliente = db(db.clientes.user_id == auth.user.id).select().first()
        
        if not cliente:
            # Si es administrador, permitir usar cualquier cuenta
            if auth.has_membership('administrador') or auth.has_membership('operador'):
                cuenta = db(
                    (db.cuentas.id == cuenta_id) & 
                    (db.cuentas.estado == 'activa')
                ).select().first()
                if cuenta:
                    # Obtener el cliente dueño de la cuenta
                    cliente = db(db.clientes.id == cuenta.cliente_id).select().first()
                if not cuenta or not cliente:
                    return {'success': False, 'error': 'Cuenta no válida o cliente no encontrado'}
            else:
                return {'success': False, 'error': 'Usuario no tiene perfil de cliente'}
        else:
            # Cliente normal - verificar que la cuenta le pertenece
            cuenta = db(
                (db.cuentas.id == cuenta_id) & 
                (db.cuentas.cliente_id == cliente.id) &
                (db.cuentas.estado == 'activa')
            ).select().first()
            if not cuenta:
                return {'success': False, 'error': 'Cuenta no válida o inactiva'}
        
        # Verificar fondos suficientes en VES
        if cuenta.saldo_ves < monto_origen:
            return {'success': False, 'error': f'Fondos insuficientes. Saldo disponible: {cuenta.saldo_ves} VES'}
        
        # Obtener tasa de cambio actual
        # Si ya tenemos una tasa (porque el usuario especificó cantidad_divisa), usarla
        if tasa_a_usar is not None:
            tasa_aplicada = tasa_a_usar
        else:
            # Si no, obtener la tasa actual (método antiguo)
            tasas = obtener_tasas_actuales()
            if not tasas:
                return {'success': False, 'error': 'No se pudieron obtener las tasas de cambio'}
            
            if moneda_destino == 'USD':
                tasa_aplicada = tasas['usd_ves']
            elif moneda_destino == 'EUR':
                tasa_aplicada = tasas['eur_ves']
            elif moneda_destino == 'USDT':
                tasa_aplicada = tasas['usdt_ves']
            else:
                return {'success': False, 'error': f'Moneda destino no soportada: {moneda_destino}'}
        
        # Calcular monto destino
        monto_destino = monto_origen / Decimal(str(tasa_aplicada))
        monto_destino = monto_destino.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # *** VALIDAR LÍMITES DE VENTA ANTES DE PROCESAR ***
        validacion = validar_limite_venta(moneda_destino, float(monto_destino))
        
        if not validacion['puede_vender']:
            logger.warning(f"Venta rechazada por límites: {validacion['razon']}")
            return {
                'success': False, 
                'error': f"Venta rechazada: {validacion['razon']}"
            }
        
        logger.info(f"Validación de límites OK - Disponible: ${validacion['limite_disponible']:,.2f}")
        
        # Calcular comisión
        comision = calcular_comision(monto_origen, 'compra')
        monto_total_debitado = monto_origen + comision
        
        # Verificar fondos incluyendo comisión
        if cuenta.saldo_ves < monto_total_debitado:
            return {'success': False, 'error': f'Fondos insuficientes incluyendo comisión. Total requerido: {monto_total_debitado} VES'}
        
        # Generar número de comprobante único
        numero_comprobante = generar_comprobante_unico('COMP')
        
        # En web2py las transacciones se manejan automáticamente
        try:
            # Registrar la transacción
            transaccion_id = db.transacciones.insert(
                cuenta_id=cuenta_id,
                tipo_operacion='compra',
                moneda_origen='VES',
                moneda_destino=moneda_destino,
                monto_origen=monto_origen,
                monto_destino=monto_destino,
                tasa_aplicada=Decimal(str(tasa_aplicada)),
                comision=comision,
                numero_comprobante=numero_comprobante,
                estado='completada',
                fecha_transaccion=datetime.datetime.now(),
                observaciones=f'Compra de {moneda_destino} - Tasa: {tasa_aplicada}'
            )
            
            # Actualizar saldos de la cuenta
            nuevo_saldo_ves = cuenta.saldo_ves - monto_total_debitado
            
            if moneda_destino == 'USD':
                nuevo_saldo_usd = cuenta.saldo_usd + monto_destino
                db(db.cuentas.id == cuenta_id).update(
                    saldo_ves=nuevo_saldo_ves,
                    saldo_usd=nuevo_saldo_usd
                )
            elif moneda_destino == 'EUR':
                nuevo_saldo_eur = cuenta.saldo_eur + monto_destino
                db(db.cuentas.id == cuenta_id).update(
                    saldo_ves=nuevo_saldo_ves,
                    saldo_eur=nuevo_saldo_eur
                )
            elif moneda_destino == 'USDT':
                saldo_usdt_actual = cuenta.saldo_usdt if cuenta.saldo_usdt is not None else Decimal('0.0')
                nuevo_saldo_usdt = saldo_usdt_actual + monto_destino
                db(db.cuentas.id == cuenta_id).update(
                    saldo_ves=nuevo_saldo_ves,
                    saldo_usdt=nuevo_saldo_usdt
                )
            
            # Registrar en historial de movimientos (log adicional para auditoría)
            registrar_movimiento_historial(
                cuenta_id=cuenta_id,
                tipo_movimiento='debito',
                moneda='VES',
                monto=monto_total_debitado,
                descripcion=f'Compra de {moneda_destino} - Comprobante: {numero_comprobante}',
                transaccion_id=transaccion_id
            )
            
            registrar_movimiento_historial(
                cuenta_id=cuenta_id,
                tipo_movimiento='credito',
                moneda=moneda_destino,
                monto=monto_destino,
                descripcion=f'Compra de {moneda_destino} - Comprobante: {numero_comprobante}',
                transaccion_id=transaccion_id
            )
            
            # Las transacciones se confirman automáticamente en web2py
            
            # Registrar en log de auditoría
            log_transaccion(
                tipo_operacion='compra',
                cuenta_id=cuenta_id,
                monto_origen=monto_origen,
                moneda_origen='VES',
                monto_destino=monto_destino,
                moneda_destino=moneda_destino,
                tasa_aplicada=tasa_aplicada,
                numero_comprobante=numero_comprobante,
                resultado='exitoso'
            )
            
            logger.info(f"Compra exitosa - Usuario: {auth.user.email}, Comprobante: {numero_comprobante}, Monto: {monto_origen} VES -> {monto_destino} {moneda_destino}")
            
            # *** ACTUALIZAR LÍMITES Y REMESAS ***
            resultado_limite = procesar_venta_con_limites(
                moneda=moneda_destino,
                monto_venta=float(monto_destino),
                transaccion_id=transaccion_id
            )
            
            if resultado_limite['success']:
                logger.info(f"Límites actualizados: {resultado_limite['mensaje']}")
            else:
                logger.warning(f"Error actualizando límites: {resultado_limite['mensaje']}")
            
            # Convertir transaccion_id para el return
            try:
                if hasattr(transaccion_id, 'id'):
                    transaccion_id_return = transaccion_id.id
                elif hasattr(transaccion_id, '_id'):
                    transaccion_id_return = transaccion_id._id
                else:
                    transaccion_id_return = transaccion_id
                transaccion_id_return = int(str(transaccion_id_return).strip()) if transaccion_id_return else None
            except:
                transaccion_id_return = None
            
            return {
                'success': True,
                'transaccion_id': transaccion_id_return,
                'comprobante': numero_comprobante,
                'monto_origen': float(monto_origen),
                'monto_destino': float(monto_destino),
                'comision': float(comision),
                'tasa_aplicada': float(tasa_aplicada)
            }
            
        except Exception as e:
            # En web2py, los rollbacks se manejan automáticamente en caso de error
            
            # Registrar error en log de auditoría
            log_transaccion(
                tipo_operacion='compra',
                cuenta_id=cuenta_id,
                monto_origen=monto_origen,
                moneda_origen='VES',
                monto_destino=0,
                moneda_destino=moneda_destino,
                tasa_aplicada=0,
                numero_comprobante='',
                resultado='fallido',
                mensaje_error=str(e)
            )
            
            logger.error(f"Error en transacción de compra: {str(e)}")
            return {'success': False, 'error': f'Error procesando transacción: {str(e)}'}
        
    except Exception as e:
        logger.error(f"Error en procesar_compra_divisa: {str(e)}")
        
        # Registrar error general en log de auditoría
        log_auditoria(
            accion='transaccion_compra',
            modulo='divisas',
            resultado='fallido',
            mensaje_error=str(e)
        )
        
        return {'success': False, 'error': str(e)}

def procesar_venta_divisa():
    """
    Procesa una transacción de venta de divisas
    """
    try:
        # Obtener parámetros de la transacción
        cuenta_id = request.vars.cuenta_id
        moneda_origen = request.vars.moneda_origen  # USD o EUR
        
        # Nuevo: obtener cantidad de divisa a vender
        if request.vars.cantidad_divisa:
            monto_origen = Decimal(str(request.vars.cantidad_divisa))  # Cantidad de divisa a vender
        else:
            # Compatibilidad con método anterior
            monto_origen = Decimal(str(request.vars.monto_origen))  # Monto en divisa extranjera
        
        # Validaciones básicas
        if not cuenta_id or not moneda_origen or not monto_origen:
            return {'success': False, 'error': 'Faltan parámetros requeridos'}
        
        if moneda_origen not in ['USD', 'EUR', 'USDT']:
            return {'success': False, 'error': 'Moneda origen debe ser USD, EUR o USDT'}
        
        if monto_origen <= 0:
            return {'success': False, 'error': 'El monto debe ser mayor a cero'}
        
        # Verificar que la cuenta pertenece al usuario actual o es administrador
        cliente = db(db.clientes.user_id == auth.user.id).select().first()
        
        if not cliente:
            # Si es administrador, permitir usar cualquier cuenta
            if auth.has_membership('administrador') or auth.has_membership('operador'):
                cuenta = db(
                    (db.cuentas.id == cuenta_id) & 
                    (db.cuentas.estado == 'activa')
                ).select().first()
                if cuenta:
                    # Obtener el cliente dueño de la cuenta
                    cliente = db(db.clientes.id == cuenta.cliente_id).select().first()
                if not cuenta or not cliente:
                    return {'success': False, 'error': 'Cuenta no válida o cliente no encontrado'}
            else:
                return {'success': False, 'error': 'Usuario no tiene perfil de cliente'}
        else:
            # Cliente normal - verificar que la cuenta le pertenece
            cuenta = db(
                (db.cuentas.id == cuenta_id) & 
                (db.cuentas.cliente_id == cliente.id) &
                (db.cuentas.estado == 'activa')
            ).select().first()
            if not cuenta:
                return {'success': False, 'error': 'Cuenta no válida o inactiva'}
        
        if not cuenta:
            return {'success': False, 'error': 'Cuenta no válida o inactiva'}
        
        # Verificar fondos suficientes en la divisa origen
        if moneda_origen == 'USD':
            saldo_disponible = cuenta.saldo_usd
        elif moneda_origen == 'EUR':
            saldo_disponible = cuenta.saldo_eur
        elif moneda_origen == 'USDT':
            saldo_disponible = cuenta.saldo_usdt if cuenta.saldo_usdt is not None else Decimal('0.0')
        else:
            return {'success': False, 'error': f'Moneda origen no soportada: {moneda_origen}'}
        if saldo_disponible < monto_origen:
            return {'success': False, 'error': f'Fondos insuficientes. Saldo disponible: {saldo_disponible} {moneda_origen}'}
        
        # Obtener tasa de cambio actual
        tasas = obtener_tasas_actuales()
        if not tasas:
            return {'success': False, 'error': 'No se pudieron obtener las tasas de cambio'}
        
        if moneda_origen == 'USD':
            tasa_aplicada = tasas['usd_ves']
        elif moneda_origen == 'EUR':
            tasa_aplicada = tasas['eur_ves']
        elif moneda_origen == 'USDT':
            tasa_aplicada = tasas['usdt_ves']
        else:
            return {'success': False, 'error': f'Moneda origen no soportada: {moneda_origen}'}
        
        # Calcular monto destino en VES
        monto_destino = monto_origen * Decimal(str(tasa_aplicada))
        monto_destino = monto_destino.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Calcular comisión (se descuenta del monto en VES)
        comision = calcular_comision(monto_destino, 'venta')
        monto_neto_ves = monto_destino - comision
        
        # Generar número de comprobante único
        numero_comprobante = generar_comprobante_unico('VENT')
        
        # En web2py las transacciones se manejan automáticamente
        try:
            # Registrar la transacción
            transaccion_id = db.transacciones.insert(
                cuenta_id=cuenta_id,
                tipo_operacion='venta',
                moneda_origen=moneda_origen,
                moneda_destino='VES',
                monto_origen=monto_origen,
                monto_destino=monto_neto_ves,
                tasa_aplicada=Decimal(str(tasa_aplicada)),
                comision=comision,
                numero_comprobante=numero_comprobante,
                estado='completada',
                fecha_transaccion=datetime.datetime.now(),
                observaciones=f'Venta de {moneda_origen} - Tasa: {tasa_aplicada}'
            )
            
            # Debug: Imprimir información sobre transaccion_id
            logger.info(f"Tipo de transaccion_id: {type(transaccion_id)}")
            logger.info(f"Valor de transaccion_id: {transaccion_id}")
            
            # Intentar obtener el ID numérico
            try:
                if hasattr(transaccion_id, 'id'):
                    transaccion_id = transaccion_id.id
                elif hasattr(transaccion_id, '_id'):
                    transaccion_id = transaccion_id._id
                transaccion_id = int(str(transaccion_id).strip())
                logger.info(f"ID convertido: {transaccion_id}")
            except Exception as e:
                logger.error(f"Error convirtiendo ID: {str(e)}")
            
            # Actualizar saldos de la cuenta
            nuevo_saldo_ves = cuenta.saldo_ves + monto_neto_ves
            
            if moneda_origen == 'USD':
                nuevo_saldo_usd = cuenta.saldo_usd - monto_origen
                db(db.cuentas.id == cuenta_id).update(
                    saldo_ves=nuevo_saldo_ves,
                    saldo_usd=nuevo_saldo_usd
                )
            elif moneda_origen == 'EUR':
                nuevo_saldo_eur = cuenta.saldo_eur - monto_origen
                db(db.cuentas.id == cuenta_id).update(
                    saldo_ves=nuevo_saldo_ves,
                    saldo_eur=nuevo_saldo_eur
                )
            elif moneda_origen == 'USDT':
                saldo_usdt_actual = cuenta.saldo_usdt if cuenta.saldo_usdt is not None else Decimal('0.0')
                nuevo_saldo_usdt = saldo_usdt_actual - monto_origen
                db(db.cuentas.id == cuenta_id).update(
                    saldo_ves=nuevo_saldo_ves,
                    saldo_usdt=nuevo_saldo_usdt
                )
            
            # Registrar en historial de movimientos (log adicional para auditoría)
            registrar_movimiento_historial(
                cuenta_id=cuenta_id,
                tipo_movimiento='debito',
                moneda=moneda_origen,
                monto=monto_origen,
                descripcion=f'Venta de {moneda_origen} - Comprobante: {numero_comprobante}',
                transaccion_id=transaccion_id
            )
            
            registrar_movimiento_historial(
                cuenta_id=cuenta_id,
                tipo_movimiento='credito',
                moneda='VES',
                monto=monto_neto_ves,
                descripcion=f'Venta de {moneda_origen} - Comprobante: {numero_comprobante}',
                transaccion_id=transaccion_id
            )
            
            # Las transacciones se confirman automáticamente en web2py
            
            # Registrar en log de auditoría
            log_transaccion(
                tipo_operacion='venta',
                cuenta_id=cuenta_id,
                monto_origen=monto_origen,
                moneda_origen=moneda_origen,
                monto_destino=monto_neto_ves,
                moneda_destino='VES',
                tasa_aplicada=tasa_aplicada,
                numero_comprobante=numero_comprobante,
                resultado='exitoso'
            )
            
            logger.info(f"Venta exitosa - Usuario: {auth.user.email}, Comprobante: {numero_comprobante}, Monto: {monto_origen} {moneda_origen} -> {monto_neto_ves} VES")
            
            # Convertir transaccion_id para el return
            try:
                if hasattr(transaccion_id, 'id'):
                    transaccion_id_return = transaccion_id.id
                elif hasattr(transaccion_id, '_id'):
                    transaccion_id_return = transaccion_id._id
                else:
                    transaccion_id_return = transaccion_id
                transaccion_id_return = int(str(transaccion_id_return).strip()) if transaccion_id_return else None
            except:
                transaccion_id_return = None
            
            return {
                'success': True,
                'transaccion_id': transaccion_id_return,
                'comprobante': numero_comprobante,
                'monto_origen': float(monto_origen),
                'monto_destino': float(monto_neto_ves),
                'comision': float(comision),
                'tasa_aplicada': float(tasa_aplicada)
            }
            
        except Exception as e:
            # En web2py, los rollbacks se manejan automáticamente en caso de error
            
            # Registrar error en log de auditoría
            log_transaccion(
                tipo_operacion='venta',
                cuenta_id=cuenta_id,
                monto_origen=monto_origen,
                moneda_origen=moneda_origen,
                monto_destino=0,
                moneda_destino='VES',
                tasa_aplicada=0,
                numero_comprobante='',
                resultado='fallido',
                mensaje_error=str(e)
            )
            
            logger.error(f"Error en transacción de venta: {str(e)}")
            return {'success': False, 'error': f'Error procesando transacción: {str(e)}'}
        
    except Exception as e:
        logger.error(f"Error en procesar_venta_divisa: {str(e)}")
        
        # Registrar error general en log de auditoría
        log_auditoria(
            accion='transaccion_venta',
            modulo='divisas',
            resultado='fallido',
            mensaje_error=str(e)
        )
        
        return {'success': False, 'error': str(e)}

def generar_comprobante_unico(prefijo='TXN'):
    """
    Genera un número de comprobante único
    Formato: PREFIJO-YYYYMMDD-HHMMSS-UUID4
    """
    try:
        fecha_hora = datetime.datetime.now()
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
        # Fallback simple
        return f"{prefijo}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:8].upper()}"

def calcular_comision(monto, tipo_operacion):
    """
    Calcula la comisión para una operación
    """
    try:
        # Obtener configuración de comisiones
        if tipo_operacion == 'compra':
            config_comision = db(db.configuracion.clave == 'comision_compra').select().first()
        else:
            config_comision = db(db.configuracion.clave == 'comision_venta').select().first()
        
        if config_comision:
            porcentaje_comision = Decimal(config_comision.valor)
        else:
            # Comisión por defecto del 0.5%
            porcentaje_comision = Decimal('0.005')
        
        comision = monto * porcentaje_comision
        return comision.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
    except Exception as e:
        logger.error(f"Error calculando comisión: {str(e)}")
        # Comisión por defecto
        return (Decimal(str(monto)) * Decimal('0.005')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def crear_datos_prueba_admin():
    """Crea datos de prueba para administradores"""
    try:
        # Crear cliente de prueba
        cliente_id = db.clientes.insert(
            user_id=auth.user.id,
            cedula='V-12345678',
            fecha_registro=datetime.datetime.now()
        )
        
        # Generar número de cuenta único
        import random
        numero_cuenta = "2001" + "".join([str(random.randint(0, 9)) for _ in range(16)])
        
        # Crear cuenta de prueba con saldos
        db.cuentas.insert(
            cliente_id=cliente_id,
            numero_cuenta=numero_cuenta,
            tipo_cuenta='corriente',
            saldo_ves=1000000.00,  # 1 millón de bolívares
            saldo_usd=1000.00,     # 1000 USD
            saldo_eur=1000.00,     # 1000 EUR
            estado='activa',
            fecha_creacion=datetime.datetime.now()
        )
        
        # Crear tasas de prueba si no existen
        if not db(db.tasas_cambio.activa == True).select().first():
            db.tasas_cambio.insert(
                fecha=datetime.date.today(),
                hora=datetime.datetime.now().time(),
                usd_ves=36.50,
                eur_ves=40.25,
                fuente='BCV',
                activa=True
            )
        
        # Las transacciones se confirman automáticamente en web2py
        return db(db.clientes.id == cliente_id).select().first()
        
    except Exception as e:
        # En web2py, los rollbacks se manejan automáticamente en caso de error
        logger.error(f"Error creando datos de prueba: {str(e)}")
        return None

def obtener_tasas_actuales():
    """
    Obtiene las tasas de cambio actuales desde la base de datos
    """
    try:
        # Buscar la tasa activa más reciente
        tasa_activa = db(db.tasas_cambio.activa == True).select().first()
        
        if tasa_activa:
            return {
                'usd_ves': float(tasa_activa.usd_ves),
                'eur_ves': float(tasa_activa.eur_ves),
                'usdt_ves': float(tasa_activa.usdt_ves) if tasa_activa.usdt_ves else float(tasa_activa.usd_ves),
                'fecha': tasa_activa.fecha,
                'hora': tasa_activa.hora,
                'fuente': tasa_activa.fuente
            }
        else:
            # Si no hay tasa activa, buscar la más reciente
            tasa_reciente = db().select(
                db.tasas_cambio.ALL,
                orderby=~db.tasas_cambio.fecha|~db.tasas_cambio.hora,
                limitby=(0, 1)
            ).first()
            
            if tasa_reciente:
                return {
                    'usd_ves': float(tasa_reciente.usd_ves),
                    'eur_ves': float(tasa_reciente.eur_ves),
                    'usdt_ves': float(tasa_reciente.usdt_ves) if tasa_reciente.usdt_ves else float(tasa_reciente.usd_ves),
                    'fecha': tasa_reciente.fecha,
                    'hora': tasa_reciente.hora,
                    'fuente': f"{tasa_reciente.fuente} (Histórica)"
                }
            else:
                logger.warning("No hay tasas disponibles en la base de datos")
                return None
                
    except Exception as e:
        logger.error(f"Error obteniendo tasas actuales: {str(e)}")
        return None

def obtener_tasas_para_transacciones():
    """
    Obtiene las tasas de cambio en formato para transacciones (con compra/venta)
    """
    try:
        tasas_base = obtener_tasas_actuales()
        if not tasas_base:
            # Crear tasas por defecto si no hay en BD
            logger.warning("No hay tasas en BD, usando valores por defecto")
            return {
                'USD': {
                    'compra': 36.50,
                    'venta': 36.80
                },
                'EUR': {
                    'compra': 40.25,
                    'venta': 40.60
                },
                'USDT': {
                    'compra': 36.50,
                    'venta': 36.80
                }
            }
        
        # Convertir tasas base a formato con compra/venta
        # Para compra: cliente compra divisa (paga más)
        # Para venta: cliente vende divisa (recibe menos)
        margen = 0.008  # 0.8% de margen
        
        usd_base = tasas_base['usd_ves']
        eur_base = tasas_base['eur_ves']
        usdt_base = tasas_base['usdt_ves']
        
        return {
            'USD': {
                'compra': usd_base * (1 + margen),  # Cliente paga más para comprar
                'venta': usd_base * (1 - margen)    # Cliente recibe menos al vender
            },
            'EUR': {
                'compra': eur_base * (1 + margen),
                'venta': eur_base * (1 - margen)
            },
            'USDT': {
                'compra': usdt_base * (1 + margen),
                'venta': usdt_base * (1 - margen)
            },
            'usd': {  # También en minúsculas para compatibilidad
                'compra': usd_base * (1 + margen),
                'venta': usd_base * (1 - margen)
            },
            'eur': {
                'compra': eur_base * (1 + margen),
                'venta': eur_base * (1 - margen)
            },
            'usdt': {
                'compra': usdt_base * (1 + margen),
                'venta': usdt_base * (1 - margen)
            }
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo tasas para transacciones: {str(e)}")
        # Devolver tasas por defecto en caso de error
        return {
            'USD': {
                'compra': 36.50,
                'venta': 36.80
            },
            'EUR': {
                'compra': 40.25,
                'venta': 40.60
            },
            'USDT': {
                'compra': 36.50,  # Usar misma tasa que USD por defecto
                'venta': 36.80
            },
            'usd': {
                'compra': 36.50,
                'venta': 36.80
            },
            'eur': {
                'compra': 40.25,
                'venta': 40.60
            },
            'usdt': {
                'compra': 36.50,
                'venta': 36.80
            }
        }

@auth.requires_login()
def comprobante():
    """
    Muestra el comprobante de una transacción
    """
    try:
        if not request.args(0):
            response.flash = "ID de transacción requerido"
            redirect(URL('divisas', 'index'))
        
        transaccion_id = request.args(0)
        
        # Obtener la transacción primero
        transaccion = db(db.transacciones.id == transaccion_id).select().first()
        
        if not transaccion:
            response.flash = "Transacción no encontrada"
            redirect(URL('divisas', 'index'))
        
        # Obtener la cuenta de la transacción
        cuenta = db(db.cuentas.id == transaccion.cuenta_id).select().first()
        
        if not cuenta:
            response.flash = "Cuenta no encontrada"
            redirect(URL('divisas', 'index'))
        
        # Obtener el cliente dueño de la cuenta (no el usuario actual)
        cliente = db(db.clientes.id == cuenta.cliente_id).select().first()
        
        if not cliente:
            response.flash = "Cliente no encontrado"
            redirect(URL('divisas', 'index'))
        
        # Verificar permisos: debe ser el dueño de la cuenta o administrador
        es_admin = auth.has_membership('administrador') or auth.has_membership('operador')
        cliente_actual = db(db.clientes.user_id == auth.user.id).select().first()
        es_propietario = cliente_actual and cliente_actual.id == cliente.id
        
        if not (es_propietario or es_admin):
            response.flash = "Acceso no autorizado a esta transacción"
            redirect(URL('divisas', 'index'))
        
        # Obtener el usuario asociado al cliente
        usuario_cliente = db(db.auth_user.id == cliente.user_id).select().first()
        
        return dict(
            transaccion=transaccion,
            cuenta=cuenta,
            cliente=cliente,
            usuario_cliente=usuario_cliente
        )
        
    except Exception as e:
        logger.error(f"Error mostrando comprobante: {str(e)}")
        response.flash = f"Error: {str(e)}"
        redirect(URL('divisas', 'index'))

def calcular_cambio():
    """
    Función AJAX para calcular cambios en tiempo real
    Requisitos: 4.1, 5.1
    """
    try:
        monto = request.vars.monto
        moneda_origen = request.vars.moneda_origen
        moneda_destino = request.vars.moneda_destino
        tipo_operacion = request.vars.tipo_operacion  # 'compra' o 'venta'
        
        if not all([monto, moneda_origen, moneda_destino, tipo_operacion]):
            return response.json({'error': 'Faltan parámetros'})
        
        try:
            monto_decimal = Decimal(str(monto))
            if monto_decimal <= 0:
                return response.json({'error': 'El monto debe ser mayor a cero'})
        except (InvalidOperation, ValueError):
            return response.json({'error': 'Monto inválido'})
        
        # Obtener tasas actuales
        tasas = obtener_tasas_actuales()
        if not tasas:
            return response.json({'error': 'No se pudieron obtener las tasas'})
        
        # Calcular conversión según el tipo de operación
        if tipo_operacion == 'compra':
            # Compra: VES -> USD/EUR
            if moneda_origen != 'VES' or moneda_destino not in ['USD', 'EUR', 'USDT']:
                return response.json({'error': 'Para compra: origen debe ser VES, destino USD, EUR o USDT'})
            
            tasa = tasas['usd_ves'] if moneda_destino == 'USD' else tasas['eur_ves']
            monto_convertido = monto_decimal / Decimal(str(tasa))
            comision = calcular_comision(monto_decimal, 'compra')
            total_debitado = monto_decimal + comision
            
        else:  # venta
            # Venta: USD/EUR -> VES
            if moneda_origen not in ['USD', 'EUR', 'USDT'] or moneda_destino != 'VES':
                return response.json({'error': 'Para venta: origen debe ser USD, EUR o USDT, destino VES'})
            
            tasa = tasas['usd_ves'] if moneda_origen == 'USD' else tasas['eur_ves']
            monto_bruto = monto_decimal * Decimal(str(tasa))
            comision = calcular_comision(monto_bruto, 'venta')
            monto_convertido = monto_bruto - comision
            total_debitado = monto_decimal
        
        return response.json({
            'success': True,
            'monto_convertido': float(monto_convertido.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'comision': float(comision),
            'total_debitado': float(total_debitado),
            'tasa_aplicada': float(tasa),
            'fecha_tasa': str(tasas['fecha']),
            'hora_tasa': str(tasas['hora'])
        })
        
    except Exception as e:
        logger.error(f"Error en calcular_cambio: {str(e)}")
        return response.json({'error': str(e)})

@auth.requires_login()
def validar_fondos():
    """
    Función AJAX para validar fondos disponibles
    """
    try:
        cuenta_id = request.vars.cuenta_id
        monto = request.vars.monto
        moneda = request.vars.moneda
        
        if not all([cuenta_id, monto, moneda]):
            return response.json({'error': 'Faltan parámetros'})
        
        try:
            monto_decimal = Decimal(str(monto))
            if monto_decimal <= 0:
                return response.json({'error': 'El monto debe ser mayor a cero'})
        except (InvalidOperation, ValueError):
            return response.json({'error': 'Monto inválido'})
        
        # Verificar que la cuenta pertenece al usuario actual
        cliente = db(db.clientes.user_id == auth.user.id).select().first()
        if not cliente:
            return response.json({'error': 'Usuario no autorizado'})
        
        cuenta = db(
            (db.cuentas.id == cuenta_id) & 
            (db.cuentas.cliente_id == cliente.id) &
            (db.cuentas.estado == 'activa')
        ).select().first()
        
        if not cuenta:
            return response.json({'error': 'Cuenta no válida'})
        
        # Obtener saldo según la moneda
        if moneda == 'VES':
            saldo_disponible = cuenta.saldo_ves
        elif moneda == 'USD':
            saldo_disponible = cuenta.saldo_usd
        elif moneda == 'EUR':
            saldo_disponible = cuenta.saldo_eur
        else:
            return response.json({'error': 'Moneda no válida'})
        
        fondos_suficientes = saldo_disponible >= monto_decimal
        
        return response.json({
            'success': True,
            'fondos_suficientes': fondos_suficientes,
            'saldo_disponible': float(saldo_disponible),
            'monto_solicitado': float(monto_decimal),
            'diferencia': float(saldo_disponible - monto_decimal)
        })
        
    except Exception as e:
        logger.error(f"Error en validar_fondos: {str(e)}")
        return response.json({'error': str(e)})

@auth.requires_login()
def historial_transacciones():
    """
    Muestra el historial de transacciones del cliente o administrador
    """
    try:
        # Obtener roles del usuario
        user_roles = get_user_roles()
        
        # Si es administrador u operador, puede ver todas las transacciones
        if 'administrador' in user_roles or 'operador' in user_roles:
            cliente = None  # Los administradores no necesitan perfil de cliente
        else:
            # Para clientes, verificar que tengan perfil
            cliente = db(db.clientes.user_id == auth.user.id).select().first()
            if not cliente:
                response.flash = "Debe completar su registro como cliente"
                redirect(URL('clientes', 'registrar'))
        
        # Obtener parámetros de filtro
        fecha_desde = request.vars.fecha_desde
        fecha_hasta = request.vars.fecha_hasta
        tipo_operacion = request.vars.tipo_operacion
        moneda = request.vars.moneda
        
        # Construir query base
        if cliente:
            # Para clientes: solo sus transacciones
            query = (db.transacciones.cuenta_id == db.cuentas.id) & (db.cuentas.cliente_id == cliente.id)
        else:
            # Para administradores: todas las transacciones
            query = (db.transacciones.cuenta_id == db.cuentas.id)
        
        # Aplicar filtros
        if fecha_desde:
            query &= db.transacciones.fecha_transaccion >= fecha_desde
        if fecha_hasta:
            query &= db.transacciones.fecha_transaccion <= fecha_hasta + ' 23:59:59'
        if tipo_operacion and tipo_operacion != 'todos':
            query &= db.transacciones.tipo_operacion == tipo_operacion
        if moneda and moneda != 'todas':
            query &= ((db.transacciones.moneda_origen == moneda) | (db.transacciones.moneda_destino == moneda))
        
        # Obtener transacciones con información de cuenta y cliente
        transacciones = db(query).select(
            db.transacciones.ALL,
            db.cuentas.numero_cuenta,
            db.clientes.cedula,
            db.auth_user.first_name,
            db.auth_user.last_name,
            left=[
                db.cuentas.on(db.transacciones.cuenta_id == db.cuentas.id),
                db.clientes.on(db.cuentas.cliente_id == db.clientes.id),
                db.auth_user.on(db.clientes.user_id == db.auth_user.id)
            ],
            orderby=~db.transacciones.fecha_transaccion,
            limitby=(0, 50)  # Limitar a 50 registros
        )
        
        return dict(
            transacciones=transacciones,
            cliente=cliente,
            filtros={
                'fecha_desde': fecha_desde,
                'fecha_hasta': fecha_hasta,
                'tipo_operacion': tipo_operacion,
                'moneda': moneda
            }
        )
        
    except Exception as e:
        logger.error(f"Error en historial_transacciones: {str(e)}")
        response.flash = f"Error: {str(e)}"
        redirect(URL('divisas', 'index'))

def tasas_actuales():
    """
    Función pública para consultar tasas actuales (para widgets)
    """
    try:
        tasas = obtener_tasas_actuales()
        if tasas:
            return response.json({
                'success': True,
                'tasas': tasas
            })
        else:
            return response.json({
                'success': False,
                'error': 'No se pudieron obtener las tasas'
            })
    except Exception as e:
        logger.error(f"Error en tasas_actuales: {str(e)}")
        return response.json({
            'success': False,
            'error': str(e)
        })

def registrar_movimiento_historial(cuenta_id, tipo_movimiento, moneda, monto, descripcion, transaccion_id=None):
    """
    Registra un movimiento en el historial para auditoría con seguimiento de saldos
    Requisitos: 4.5, 5.5
    """
    try:
        # Convertir transaccion_id a entero si es posible
        if transaccion_id is not None:
            try:
                if hasattr(transaccion_id, 'id'):
                    transaccion_id = transaccion_id.id
                elif hasattr(transaccion_id, '_id'):
                    transaccion_id = transaccion_id._id
                transaccion_id = int(str(transaccion_id).strip())
                logger.info(f"ID de transacción convertido: {transaccion_id}")
            except Exception as e:
                logger.error(f"Error convirtiendo ID de transacción: {str(e)}")
                transaccion_id = None
        
        # Obtener cuenta actual
        cuenta = db(db.cuentas.id == cuenta_id).select().first()
        if not cuenta:
            logger.error(f"Cuenta {cuenta_id} no encontrada para registrar movimiento")
            return
        
        # Obtener saldo anterior según la moneda
        if moneda == 'VES':
            saldo_anterior = cuenta.saldo_ves
        elif moneda == 'USD':
            saldo_anterior = cuenta.saldo_usd
        elif moneda == 'EUR':
            saldo_anterior = cuenta.saldo_eur
        else:
            logger.error(f"Moneda {moneda} no válida para movimiento")
            return
        
        # Calcular saldo nuevo
        if tipo_movimiento == 'credito':
            saldo_nuevo = saldo_anterior + Decimal(str(monto))
        else:  # debito
            saldo_nuevo = saldo_anterior - Decimal(str(monto))
        
        # Registrar movimiento
        db.movimientos_cuenta.insert(
            cuenta_id=cuenta_id,
            tipo_movimiento=tipo_movimiento,
            moneda=moneda,
            monto=Decimal(str(monto)),
            saldo_anterior=saldo_anterior,
            saldo_nuevo=saldo_nuevo,
            descripcion=descripcion,
            transaccion_relacionada=transaccion_id,
            fecha_movimiento=datetime.datetime.now(),
            usuario_id=auth.user.id if auth.user else None
        )
        
        # Log adicional para auditoría
        logger.info(f"Movimiento registrado - Cuenta: {cuenta_id}, Tipo: {tipo_movimiento}, Moneda: {moneda}, Monto: {monto}, Saldo: {saldo_anterior} -> {saldo_nuevo}")
        
    except Exception as e:
        logger.error(f"Error registrando movimiento en historial: {str(e)}")
        # No fallar la transacción principal por un error de logging

def obtener_saldos_actualizados(cuenta_id):
    """
    Obtiene los saldos actualizados de una cuenta después de una transacción
    """
    try:
        cuenta = db(db.cuentas.id == cuenta_id).select().first()
        if cuenta:
            return {
                'saldo_ves': float(cuenta.saldo_ves),
                'saldo_usd': float(cuenta.saldo_usd),
                'saldo_eur': float(cuenta.saldo_eur)
            }
        return None
    except Exception as e:
        logger.error(f"Error obteniendo saldos actualizados: {str(e)}")
        return None

def validar_integridad_saldos(cuenta_id):
    """
    Valida que los saldos de una cuenta sean consistentes
    """
    try:
        cuenta = db(db.cuentas.id == cuenta_id).select().first()
        if not cuenta:
            return {'valido': False, 'error': 'Cuenta no encontrada'}
        
        # Verificar que los saldos no sean negativos
        if cuenta.saldo_ves < 0 or cuenta.saldo_usd < 0 or cuenta.saldo_eur < 0:
            logger.error(f"Saldos negativos detectados en cuenta {cuenta_id}: VES={cuenta.saldo_ves}, USD={cuenta.saldo_usd}, EUR={cuenta.saldo_eur}")
            return {'valido': False, 'error': 'Saldos negativos detectados'}
        
        return {'valido': True}
        
    except Exception as e:
        logger.error(f"Error validando integridad de saldos: {str(e)}")
        return {'valido': False, 'error': str(e)}

def generar_reporte_transacciones_diario():
    """
    Genera un reporte diario de transacciones para auditoría
    """
    try:
        fecha_hoy = datetime.date.today()
        
        # Obtener transacciones del día
        transacciones_hoy = db(
            db.transacciones.fecha_transaccion >= fecha_hoy
        ).select()
        
        if not transacciones_hoy:
            return {'success': True, 'mensaje': 'No hay transacciones para reportar hoy'}
        
        # Calcular estadísticas
        total_compras = sum([float(t.monto_origen) for t in transacciones_hoy if t.tipo_operacion == 'compra'])
        total_ventas = sum([float(t.monto_origen) for t in transacciones_hoy if t.tipo_operacion == 'venta'])
        total_comisiones = sum([float(t.comision) for t in transacciones_hoy])
        
        reporte = {
            'fecha': str(fecha_hoy),
            'total_transacciones': len(transacciones_hoy),
            'total_compras': float(total_compras),
            'total_ventas': float(total_ventas),
            'total_comisiones': float(total_comisiones),
            'transacciones': [
                {
                    'id': t.id,
                    'comprobante': t.numero_comprobante,
                    'tipo': t.tipo_operacion,
                    'monto_origen': float(t.monto_origen),
                    'moneda_origen': t.moneda_origen,
                    'monto_destino': float(t.monto_destino),
                    'moneda_destino': t.moneda_destino,
                    'tasa': float(t.tasa_aplicada),
                    'comision': float(t.comision),
                    'fecha': str(t.fecha_transaccion)
                } for t in transacciones_hoy
            ]
        }
        
        # Guardar reporte en configuración para acceso posterior
        import json
        clave_reporte = f"reporte_diario_{fecha_hoy.strftime('%Y%m%d')}"
        
        # Verificar si ya existe el reporte
        reporte_existente = db(db.configuracion.clave == clave_reporte).select().first()
        if reporte_existente:
            db(db.configuracion.clave == clave_reporte).update(
                valor=json.dumps(reporte),
                fecha_actualizacion=datetime.datetime.now()
            )
        else:
            db.configuracion.insert(
                clave=clave_reporte,
                valor=json.dumps(reporte),
                descripcion=f'Reporte diario de transacciones del {fecha_hoy}',
                fecha_actualizacion=datetime.datetime.now()
            )
        
        logger.info(f"Reporte diario generado: {len(transacciones_hoy)} transacciones, comisiones: {total_comisiones}")
        
        return {
            'success': True,
            'reporte': reporte,
            'mensaje': f'Reporte generado con {len(transacciones_hoy)} transacciones'
        }
        
    except Exception as e:
        logger.error(f"Error generando reporte diario: {str(e)}")
        return {'success': False, 'error': str(e)}

@auth.requires_login()
def movimientos_detallados():
    """
    Consulta movimientos detallados de una cuenta específica
    """
    try:
        cuenta_id = request.vars.cuenta_id
        if not cuenta_id:
            return dict(error="ID de cuenta requerido")
        
        # Verificar que la cuenta pertenece al usuario actual
        cliente = db(db.clientes.user_id == auth.user.id).select().first()
        if not cliente:
            return dict(error="Usuario no autorizado")
        
        cuenta = db(
            (db.cuentas.id == cuenta_id) & 
            (db.cuentas.cliente_id == cliente.id)
        ).select().first()
        
        if not cuenta:
            return dict(error="Cuenta no encontrada o no autorizada")
        
        # Obtener movimientos de la cuenta
        movimientos = db(
            db.movimientos_cuenta.cuenta_id == cuenta_id
        ).select(
            orderby=~db.movimientos_cuenta.fecha_movimiento,
            limitby=(0, 100)  # Últimos 100 movimientos
        )
        
        return dict(
            cuenta=cuenta,
            movimientos=movimientos,
            cliente=cliente
        )
        
    except Exception as e:
        logger.error(f"Error consultando movimientos detallados: {str(e)}")
        return dict(error=str(e))

def obtener_estadisticas_transacciones():
    """
    Obtiene estadísticas generales de transacciones para el dashboard administrativo
    """
    try:
        # Estadísticas del día actual
        fecha_hoy = datetime.date.today()
        
        transacciones_hoy = db(
            db.transacciones.fecha_transaccion >= fecha_hoy
        ).count()
        
        # Estadísticas del mes actual
        primer_dia_mes = fecha_hoy.replace(day=1)
        
        transacciones_mes = db(
            db.transacciones.fecha_transaccion >= primer_dia_mes
        ).count()
        
        # Volumen total en VES del mes
        compras_mes = db(
            (db.transacciones.fecha_transaccion >= primer_dia_mes) &
            (db.transacciones.tipo_operacion == 'compra')
        ).select()
        
        ventas_mes = db(
            (db.transacciones.fecha_transaccion >= primer_dia_mes) &
            (db.transacciones.tipo_operacion == 'venta')
        ).select()
        
        volumen_compras = sum([float(t.monto_origen) for t in compras_mes])
        volumen_ventas = sum([float(t.monto_destino) for t in ventas_mes])
        comisiones_mes = sum([float(t.comision) for t in compras_mes + ventas_mes])
        
        return {
            'transacciones_hoy': transacciones_hoy,
            'transacciones_mes': transacciones_mes,
            'volumen_compras_mes': volumen_compras,
            'volumen_ventas_mes': volumen_ventas,
            'comisiones_mes': comisiones_mes,
            'fecha_consulta': str(datetime.datetime.now())
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {str(e)}")
        return {
            'error': str(e),
            'transacciones_hoy': 0,
            'transacciones_mes': 0,
            'volumen_compras_mes': 0,
            'volumen_ventas_mes': 0,
            'comisiones_mes': 0
        }

def prueba_calculadora():
    """
    Página de prueba para la calculadora de divisas
    """
    return dict(
        mensaje="Página de prueba de la calculadora de divisas"
    )

def test_calculadora_asincrona():
    """
    Página de prueba para verificar la calculadora asíncrona
    """
    return dict(mensaje="Prueba de calculadora asíncrona")

def test_calculadora_simple():
    """
    Página de prueba simple para la calculadora
    """
    return dict(mensaje="Prueba simple de calculadora")

def arreglar_calculadoras():
    """
    Página de diagnóstico para arreglar las calculadoras
    """
    return dict(mensaje="Diagnóstico de calculadoras")

def debug_compra():
    """
    Función de debug para probar el flujo de compra
    """
    try:
        # Simular datos de compra
        request.vars.confirmar_compra = "1"
        request.vars.cuenta_id = "1"
        request.vars.moneda_destino = "USD"
        request.vars.cantidad_divisa = "100"
        
        logger.info("=== DEBUG COMPRA ===")
        logger.info(f"Datos simulados: {dict(request.vars)}")
        
        resultado = procesar_compra_divisa()
        logger.info(f"Resultado: {resultado}")
        
        if resultado.get('success'):
            return dict(
                mensaje="Compra exitosa",
                resultado=resultado,
                redirect_url=URL('divisas', 'historial_transacciones')
            )
        else:
            return dict(
                mensaje="Error en compra",
                resultado=resultado,
                redirect_url=URL('divisas', 'index')
            )
            
    except Exception as e:
        logger.error(f"Error en debug_compra: {str(e)}")
        return dict(
            mensaje=f"Error: {str(e)}",
            resultado=None,
            redirect_url=URL('divisas', 'index')
        )

def compra_exitosa():
    """
    Página de confirmación de compra exitosa
    """
    comprobante = request.vars.comprobante or session.get('ultimo_comprobante', 'N/A')
    return dict(comprobante=comprobante)

def comprar_simple():
    """
    Función simplificada de compra sin redirects problemáticos
    """
    try:
        # Procesamiento de compra
        if request.vars.confirmar_compra:
            logger.info(f"Procesando compra REAL (simple) para usuario: {auth.user.email}")
            
            # Obtener datos del formulario
            cuenta_id = request.vars.cuenta_id
            moneda_destino = request.vars.moneda_destino
            cantidad_divisa = request.vars.cantidad_divisa
            
            # Validación básica
            if not cuenta_id or not moneda_destino or not cantidad_divisa:
                response.flash = "❌ Faltan datos requeridos"
            else:
                # PROCESAR COMPRA REAL - no simular
                logger.info(f"Llamando a procesar_compra_divisa() con datos: cuenta_id={cuenta_id}, moneda_destino={moneda_destino}, cantidad_divisa={cantidad_divisa}")
                
                resultado = procesar_compra_divisa()
                logger.info(f"Resultado de procesar_compra_divisa(): {resultado}")
                
                if resultado.get('success'):
                    comprobante = resultado.get('comprobante')
                    session.flash = f"✅ Compra realizada exitosamente! Comprobante: {comprobante}"
                    session.ultimo_comprobante = comprobante
                    
                    # Redirect directo
                    redirect(URL('divisas', 'compra_exitosa', vars={'comprobante': comprobante}))
                else:
                    error_msg = resultado.get('error', 'Error desconocido')
                    logger.error(f"Error en compra simple: {error_msg}")
                    response.flash = f"❌ Error en la compra: {error_msg}"
        
        # Obtener datos para mostrar el formulario
        cliente = db(db.clientes.user_id == auth.user.id).select().first()
        if cliente:
            cuentas = db((db.cuentas.cliente_id == cliente.id) & (db.cuentas.estado == 'activa')).select()
        else:
            cuentas = []
        
        tasas = {'usd_ves': 36.50, 'eur_ves': 40.25}
        
        return dict(
            cuentas=cuentas,
            tasas=tasas,
            cliente=cliente
        )
        
    except Exception as e:
        logger.error(f"Error en comprar_simple: {str(e)}")
        response.flash = f"Error: {str(e)}"
        return dict(cuentas=[], tasas={'usd_ves': 36.50, 'eur_ves': 40.25}, cliente=None)