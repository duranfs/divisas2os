# -*- coding: utf-8 -*-
"""
Sistema de Manejo de Errores Personalizado
Sistema de Divisas Bancario
"""

import logging
import traceback
import json
import os
from datetime import datetime
from gluon import current

class ErrorHandler:
    """Manejador centralizado de errores del sistema"""
    
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        """Configura el sistema de logging"""
        # Crear directorio de logs si no existe
        log_dir = os.path.join(current.request.folder, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configurar logger principal
        self.logger = logging.getLogger('sistema_divisas')
        self.logger.setLevel(logging.DEBUG)
        
        # Evitar duplicar handlers
        if not self.logger.handlers:
            # Handler para errores generales
            error_handler = logging.FileHandler(
                os.path.join(log_dir, 'errors.log'),
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)
            
            # Handler para información general
            info_handler = logging.FileHandler(
                os.path.join(log_dir, 'info.log'),
                encoding='utf-8'
            )
            info_handler.setLevel(logging.INFO)
            
            # Handler para debug
            debug_handler = logging.FileHandler(
                os.path.join(log_dir, 'debug.log'),
                encoding='utf-8'
            )
            debug_handler.setLevel(logging.DEBUG)
            
            # Formato de logs
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            error_handler.setFormatter(formatter)
            info_handler.setFormatter(formatter)
            debug_handler.setFormatter(formatter)
            
            self.logger.addHandler(error_handler)
            self.logger.addHandler(info_handler)
            self.logger.addHandler(debug_handler)
    
    def log_error(self, error, context=None, user_id=None, request_info=None):
        """
        Registra un error en el sistema
        
        Args:
            error: Excepción o mensaje de error
            context: Contexto adicional del error
            user_id: ID del usuario que experimentó el error
            request_info: Información de la petición HTTP
        """
        try:
            # Obtener información del error
            if isinstance(error, Exception):
                error_message = str(error)
                error_type = type(error).__name__
                error_traceback = traceback.format_exc()
            else:
                error_message = str(error)
                error_type = 'CustomError'
                error_traceback = None
            
            # Obtener información de la petición si no se proporciona
            if not request_info and hasattr(current, 'request'):
                request_info = {
                    'url': current.request.env.request_uri,
                    'method': current.request.env.request_method,
                    'ip': current.request.env.remote_addr,
                    'user_agent': current.request.env.http_user_agent,
                    'controller': current.request.controller,
                    'function': current.request.function
                }
            
            # Obtener información del usuario si no se proporciona
            if not user_id and hasattr(current, 'auth') and current.auth.user:
                user_id = current.auth.user.id
            
            # Crear registro de error
            error_record = {
                'timestamp': datetime.now().isoformat(),
                'error_type': error_type,
                'error_message': error_message,
                'error_traceback': error_traceback,
                'user_id': user_id,
                'context': context,
                'request_info': request_info
            }
            
            # Log en archivo
            self.logger.error(json.dumps(error_record, indent=2, ensure_ascii=False))
            
            # Guardar en base de datos si está disponible
            self._save_error_to_db(error_record)
            
            # Notificar a administradores si es crítico
            if self._is_critical_error(error_type):
                self._notify_administrators(error_record)
            
            return error_record
            
        except Exception as e:
            # Error logging el error - usar logging básico
            logging.error(f"Error en ErrorHandler.log_error: {str(e)}")
            return None
    
    def _save_error_to_db(self, error_record):
        """Guarda el error en la base de datos"""
        try:
            if hasattr(current, 'db') and current.db:
                # Crear tabla de errores si no existe
                if 'system_errors' not in current.db.tables:
                    current.db.define_table('system_errors',
                        current.db.Field('timestamp', 'datetime'),
                        current.db.Field('error_type', 'string', length=100),
                        current.db.Field('error_message', 'text'),
                        current.db.Field('error_traceback', 'text'),
                        current.db.Field('user_id', 'reference auth_user'),
                        current.db.Field('context', 'json'),
                        current.db.Field('request_info', 'json'),
                        current.db.Field('resolved', 'boolean', default=False),
                        current.db.Field('resolution_notes', 'text')
                    )
                
                # Insertar error
                current.db.system_errors.insert(
                    timestamp=datetime.now(),
                    error_type=error_record['error_type'],
                    error_message=error_record['error_message'],
                    error_traceback=error_record['error_traceback'],
                    user_id=error_record['user_id'],
                    context=error_record['context'],
                    request_info=error_record['request_info']
                )
                current.db.commit()
                
        except Exception as e:
            logging.error(f"Error guardando en BD: {str(e)}")
    
    def _is_critical_error(self, error_type):
        """Determina si un error es crítico"""
        critical_errors = [
            'DatabaseError', 'ConnectionError', 'SecurityError',
            'AuthenticationError', 'DataIntegrityError'
        ]
        return error_type in critical_errors
    
    def _notify_administrators(self, error_record):
        """Notifica a los administradores sobre errores críticos"""
        try:
            if hasattr(current, 'mail') and current.mail:
                # Obtener emails de administradores
                admin_emails = self._get_admin_emails()
                
                if admin_emails:
                    subject = f"Error Crítico - Sistema de Divisas - {error_record['error_type']}"
                    
                    body = f"""
                    Se ha producido un error crítico en el Sistema de Divisas:
                    
                    Tipo de Error: {error_record['error_type']}
                    Mensaje: {error_record['error_message']}
                    Fecha/Hora: {error_record['timestamp']}
                    Usuario: {error_record['user_id'] or 'Anónimo'}
                    URL: {error_record['request_info'].get('url', 'N/A') if error_record['request_info'] else 'N/A'}
                    
                    Por favor, revise el sistema lo antes posible.
                    """
                    
                    current.mail.send(
                        to=admin_emails,
                        subject=subject,
                        message=body
                    )
                    
        except Exception as e:
            logging.error(f"Error enviando notificación: {str(e)}")
    
    def _get_admin_emails(self):
        """Obtiene los emails de los administradores"""
        try:
            if hasattr(current, 'db') and current.db:
                # Buscar usuarios con rol de administrador
                admin_group = current.db(current.db.auth_group.role == 'administrador').select().first()
                if admin_group:
                    admin_users = current.db(
                        (current.db.auth_membership.group_id == admin_group.id) &
                        (current.db.auth_membership.user_id == current.db.auth_user.id)
                    ).select(current.db.auth_user.email)
                    
                    return [user.email for user in admin_users if user.email]
            
            return []
            
        except Exception:
            return []
    
    def log_info(self, message, context=None, user_id=None):
        """Registra información general"""
        try:
            info_record = {
                'timestamp': datetime.now().isoformat(),
                'message': message,
                'context': context,
                'user_id': user_id
            }
            
            self.logger.info(json.dumps(info_record, ensure_ascii=False))
            
        except Exception as e:
            logging.error(f"Error en log_info: {str(e)}")
    
    def log_warning(self, message, context=None, user_id=None):
        """Registra advertencias"""
        try:
            warning_record = {
                'timestamp': datetime.now().isoformat(),
                'message': message,
                'context': context,
                'user_id': user_id
            }
            
            self.logger.warning(json.dumps(warning_record, ensure_ascii=False))
            
        except Exception as e:
            logging.error(f"Error en log_warning: {str(e)}")
    
    def log_debug(self, message, context=None):
        """Registra información de debug"""
        try:
            debug_record = {
                'timestamp': datetime.now().isoformat(),
                'message': message,
                'context': context
            }
            
            self.logger.debug(json.dumps(debug_record, ensure_ascii=False))
            
        except Exception as e:
            logging.error(f"Error en log_debug: {str(e)}")
    
    def get_error_statistics(self, days=7):
        """Obtiene estadísticas de errores"""
        try:
            if hasattr(current, 'db') and current.db and 'system_errors' in current.db.tables:
                from datetime import timedelta
                
                start_date = datetime.now() - timedelta(days=days)
                
                # Contar errores por tipo
                error_counts = current.db(
                    current.db.system_errors.timestamp >= start_date
                ).select(
                    current.db.system_errors.error_type,
                    current.db.system_errors.id.count(),
                    groupby=current.db.system_errors.error_type
                )
                
                # Errores no resueltos
                unresolved_count = current.db(
                    (current.db.system_errors.timestamp >= start_date) &
                    (current.db.system_errors.resolved == False)
                ).count()
                
                # Errores por día
                daily_counts = current.db(
                    current.db.system_errors.timestamp >= start_date
                ).select(
                    current.db.system_errors.timestamp.date(),
                    current.db.system_errors.id.count(),
                    groupby=current.db.system_errors.timestamp.date()
                )
                
                return {
                    'error_counts': [(row.system_errors.error_type, row._extra[current.db.system_errors.id.count()]) for row in error_counts],
                    'unresolved_count': unresolved_count,
                    'daily_counts': [(row._extra[current.db.system_errors.timestamp.date()], row._extra[current.db.system_errors.id.count()]) for row in daily_counts],
                    'period_days': days
                }
            
            return None
            
        except Exception as e:
            logging.error(f"Error obteniendo estadísticas: {str(e)}")
            return None

# Instancia global del manejador de errores
error_handler = ErrorHandler()

# Funciones de conveniencia
def log_error(error, context=None, user_id=None, request_info=None):
    """Función de conveniencia para registrar errores"""
    return error_handler.log_error(error, context, user_id, request_info)

def log_info(message, context=None, user_id=None):
    """Función de conveniencia para registrar información"""
    return error_handler.log_info(message, context, user_id)

def log_warning(message, context=None, user_id=None):
    """Función de conveniencia para registrar advertencias"""
    return error_handler.log_warning(message, context, user_id)

def log_debug(message, context=None):
    """Función de conveniencia para registrar debug"""
    return error_handler.log_debug(message, context)

def get_error_statistics(days=7):
    """Función de conveniencia para obtener estadísticas"""
    return error_handler.get_error_statistics(days)

# Decorador para manejo automático de errores
def handle_errors(func):
    """Decorador que maneja automáticamente los errores de una función"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Registrar el error
            log_error(e, context={
                'function': func.__name__,
                'args': str(args),
                'kwargs': str(kwargs)
            })
            
            # Re-lanzar la excepción para que sea manejada por web2py
            raise
    
    return wrapper

# Función para configurar manejo global de errores en web2py
def setup_global_error_handling():
    """Configura el manejo global de errores para web2py"""
    try:
        if hasattr(current, 'response'):
            # Configurar páginas de error personalizadas
            current.response.view = 'error_500.html'
            
        # Registrar handler para errores no capturados
        import sys
        
        def exception_handler(exc_type, exc_value, exc_traceback):
            if exc_type != KeyboardInterrupt:
                log_error(exc_value, context={
                    'exc_type': exc_type.__name__,
                    'traceback': traceback.format_exception(exc_type, exc_value, exc_traceback)
                })
        
        sys.excepthook = exception_handler
        
    except Exception as e:
        logging.error(f"Error configurando manejo global: {str(e)}")