# -*- coding: utf-8 -*-
"""
Tareas del Scheduler - Sistema de Divisas Bancario
Configuración de tareas automáticas para actualización de tasas
"""

import logging
import datetime

# Configurar logging específico para el scheduler
scheduler_logger = logging.getLogger("web2py.app.divisas.scheduler")

def actualizar_tasas_automatico():
    """
    Tarea del scheduler para actualizar tasas automáticamente
    Se ejecuta cada hora durante horario bancario
    Requisitos: 1.5
    """
    try:
        scheduler_logger.info("Iniciando actualización automática de tasas")
        
        # Verificar si estamos en horario bancario (8 AM - 6 PM, Lunes a Viernes)
        ahora = datetime.datetime.now()
        es_horario_bancario = (
            ahora.weekday() < 5 and  # Lunes a Viernes (0-4)
            8 <= ahora.hour < 18     # 8 AM a 6 PM
        )
        
        if not es_horario_bancario:
            scheduler_logger.info("Fuera de horario bancario, saltando actualización")
            return "Fuera de horario bancario"
        
        # Importar el controlador API para usar sus funciones
        from applications.divisas.controllers.api import obtener_tasas_bcv, guardar_tasas_db, obtener_ultimas_tasas_db
        
        # Intentar obtener tasas del BCV
        tasas_bcv = obtener_tasas_bcv()
        
        if tasas_bcv:
            # Guardar las nuevas tasas
            resultado = guardar_tasas_db(tasas_bcv)
            
            if resultado['success']:
                mensaje = f"Tasas actualizadas automáticamente: USD={tasas_bcv['usd_ves']}, EUR={tasas_bcv['eur_ves']}"
                scheduler_logger.info(mensaje)
                
                # Registrar en log de actualizaciones
                registrar_log_actualizacion(True, tasas_bcv, "Actualización exitosa desde BCV")
                
                return mensaje
            else:
                error_msg = f"Error guardando tasas: {resultado['error']}"
                scheduler_logger.error(error_msg)
                
                # Registrar error en log
                registrar_log_actualizacion(False, tasas_bcv, error_msg)
                
                return error_msg
        else:
            # No se pudieron obtener tasas del BCV
            tasas_respaldo = obtener_ultimas_tasas_db()
            mensaje = "No se pudieron obtener tasas del BCV, manteniendo tasas de respaldo"
            scheduler_logger.warning(mensaje)
            
            # Registrar en log de actualizaciones
            registrar_log_actualizacion(False, tasas_respaldo, "Error conectando con BCV")
            
            return mensaje
            
    except Exception as e:
        error_msg = f"Error en actualización automática: {str(e)}"
        scheduler_logger.error(error_msg)
        
        # Registrar error crítico
        registrar_log_actualizacion(False, None, error_msg)
        
        return error_msg

def registrar_log_actualizacion(exitoso, tasas_data, mensaje):
    """
    Registra el resultado de una actualización de tasas en la configuración
    Requisitos: 1.5
    """
    try:
        # Crear entrada de log en la tabla de configuración
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if exitoso and tasas_data:
            log_entry = {
                'timestamp': timestamp,
                'exitoso': True,
                'usd_ves': str(tasas_data.get('usd_ves', 'N/A')),
                'eur_ves': str(tasas_data.get('eur_ves', 'N/A')),
                'fuente': tasas_data.get('fuente', 'N/A'),
                'mensaje': mensaje
            }
        else:
            log_entry = {
                'timestamp': timestamp,
                'exitoso': False,
                'usd_ves': 'N/A',
                'eur_ves': 'N/A',
                'fuente': 'N/A',
                'mensaje': mensaje
            }
        
        # Convertir a string JSON para almacenar
        import json
        log_json = json.dumps(log_entry)
        
        # Buscar si existe entrada de log de hoy
        hoy = datetime.date.today().strftime("%Y-%m-%d")
        clave_log = f"log_actualizaciones_{hoy}"
        
        log_existente = db(db.configuracion.clave == clave_log).select().first()
        
        if log_existente:
            # Agregar al log existente
            try:
                logs_existentes = json.loads(log_existente.valor)
                if not isinstance(logs_existentes, list):
                    logs_existentes = [logs_existentes]
            except:
                logs_existentes = []
            
            logs_existentes.append(log_entry)
            
            # Mantener solo los últimos 24 registros del día
            if len(logs_existentes) > 24:
                logs_existentes = logs_existentes[-24:]
            
            db(db.configuracion.clave == clave_log).update(
                valor=json.dumps(logs_existentes),
                fecha_actualizacion=datetime.datetime.now()
            )
        else:
            # Crear nueva entrada de log
            db.configuracion.insert(
                clave=clave_log,
                valor=json.dumps([log_entry]),
                descripcion=f"Log de actualizaciones de tasas para {hoy}"
            )
        
        db.commit()
        scheduler_logger.info(f"Log de actualización registrado: {mensaje}")
        
    except Exception as e:
        scheduler_logger.error(f"Error registrando log de actualización: {str(e)}")

def limpiar_logs_antiguos():
    """
    Tarea para limpiar logs de actualizaciones antiguos (más de 30 días)
    Se ejecuta diariamente a medianoche
    """
    try:
        scheduler_logger.info("Iniciando limpieza de logs antiguos")
        
        # Calcular fecha límite (30 días atrás)
        fecha_limite = datetime.date.today() - datetime.timedelta(days=30)
        fecha_limite_str = fecha_limite.strftime("%Y-%m-%d")
        
        # Buscar logs antiguos
        logs_antiguos = db(
            (db.configuracion.clave.like('log_actualizaciones_%')) &
            (db.configuracion.clave < f"log_actualizaciones_{fecha_limite_str}")
        ).select()
        
        contador = 0
        for log in logs_antiguos:
            db(db.configuracion.id == log.id).delete()
            contador += 1
        
        db.commit()
        
        mensaje = f"Limpieza completada: {contador} logs antiguos eliminados"
        scheduler_logger.info(mensaje)
        
        return mensaje
        
    except Exception as e:
        error_msg = f"Error en limpieza de logs: {str(e)}"
        scheduler_logger.error(error_msg)
        return error_msg

def verificar_estado_sistema():
    """
    Tarea para verificar el estado general del sistema de tasas
    Se ejecuta cada 6 horas
    """
    try:
        scheduler_logger.info("Verificando estado del sistema")
        
        # Verificar si hay tasas activas
        tasa_activa = db(db.tasas_cambio.activa == True).select().first()
        
        if not tasa_activa:
            scheduler_logger.warning("No hay tasas activas en el sistema")
            return "Advertencia: No hay tasas activas"
        
        # Verificar antigüedad de las tasas
        ahora = datetime.datetime.now()
        fecha_tasa = datetime.datetime.combine(tasa_activa.fecha, tasa_activa.hora)
        diferencia = ahora - fecha_tasa
        
        if diferencia.total_seconds() > 7200:  # Más de 2 horas
            scheduler_logger.warning(f"Las tasas tienen más de 2 horas de antigüedad: {diferencia}")
            return f"Advertencia: Tasas antiguas ({diferencia})"
        
        # Verificar que las tasas estén en rangos razonables
        if not (1 <= float(tasa_activa.usd_ves) <= 100):
            scheduler_logger.warning(f"Tasa USD fuera de rango razonable: {tasa_activa.usd_ves}")
            return f"Advertencia: Tasa USD sospechosa ({tasa_activa.usd_ves})"
        
        if not (1 <= float(tasa_activa.eur_ves) <= 100):
            scheduler_logger.warning(f"Tasa EUR fuera de rango razonable: {tasa_activa.eur_ves}")
            return f"Advertencia: Tasa EUR sospechosa ({tasa_activa.eur_ves})"
        
        scheduler_logger.info("Estado del sistema OK")
        return "Sistema OK"
        
    except Exception as e:
        error_msg = f"Error verificando estado del sistema: {str(e)}"
        scheduler_logger.error(error_msg)
        return error_msg

# -------------------------------------------------------------------------
# Configuración de tareas del scheduler
# -------------------------------------------------------------------------

if configuration.get("scheduler.enabled"):
    try:
        # Tarea 1: Actualización automática de tasas cada hora en horario bancario
        scheduler.queue_task(
            'actualizar_tasas_automatico',
            period=3600,  # Cada hora (3600 segundos)
            timeout=300,  # 5 minutos de timeout
            repeats=0,    # Repetir indefinidamente
            retry_failed=2,  # Reintentar 2 veces si falla
            start_time=datetime.datetime.now() + datetime.timedelta(minutes=5)  # Empezar en 5 minutos
        )
        
        # Tarea 2: Limpieza de logs antiguos diariamente a las 2 AM
        scheduler.queue_task(
            'limpiar_logs_antiguos',
            period=86400,  # Cada día (86400 segundos)
            timeout=120,   # 2 minutos de timeout
            repeats=0,     # Repetir indefinidamente
            retry_failed=1,
            start_time=datetime.datetime.now().replace(hour=2, minute=0, second=0, microsecond=0)
        )
        
        # Tarea 3: Verificación del estado del sistema cada 6 horas
        scheduler.queue_task(
            'verificar_estado_sistema',
            period=21600,  # Cada 6 horas (21600 segundos)
            timeout=60,    # 1 minuto de timeout
            repeats=0,     # Repetir indefinidamente
            retry_failed=1,
            start_time=datetime.datetime.now() + datetime.timedelta(minutes=10)
        )
        
        scheduler_logger.info("Tareas del scheduler configuradas exitosamente")
        
    except Exception as e:
        scheduler_logger.error(f"Error configurando tareas del scheduler: {str(e)}")