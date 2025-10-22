# -*- coding: utf-8 -*-
"""
Configuración de Manejo de Errores Personalizado
Sistema de Divisas Bancario
"""

import os
import sys

# Import error handler with try/except to handle import issues
try:
    from modules.error_handler import error_handler, log_error, log_info, log_warning
except ImportError:
    # Fallback: create dummy functions if import fails
    def log_error(error, context=None, user_id=None):
        import logging
        logging.error(f"Error: {error}, Context: {context}")
    
    def log_info(message, context=None, user_id=None):
        import logging
        logging.info(f"Info: {message}, Context: {context}")
    
    def log_warning(message, context=None, user_id=None):
        import logging
        logging.warning(f"Warning: {message}, Context: {context}")
    
    # Create dummy error_handler object
    class DummyErrorHandler:
        def get_error_statistics(self, days=7):
            return None
    
    error_handler = DummyErrorHandler()

# -------------------------------------------------------------------------
# Configuración Global de Manejo de Errores
# -------------------------------------------------------------------------

def configure_error_handling():
    """Configura el manejo global de errores para web2py"""
    
    # Configurar páginas de error personalizadas
    if hasattr(response, 'view'):
        # Mapear códigos de error a vistas personalizadas
        error_views = {
            400: 'error_400.html',
            401: 'error_401.html', 
            403: 'error_403.html',
            404: 'error_404.html',
            500: 'error_500.html',
            503: 'error_503.html'
        }
        
        # Configurar vistas de error
        for code, view in error_views.items():
            if os.path.exists(os.path.join(request.folder, 'views', view)):
                response.files.append(URL('static', 'css/error-pages.css'))

def custom_error_handler(code, message, traceback_info=None):
    """
    Manejador personalizado de errores HTTP
    
    Args:
        code: Código de error HTTP
        message: Mensaje de error
        traceback_info: Información de traceback si está disponible
    """
    
    try:
        # Registrar el error
        error_context = {
            'http_code': code,
            'message': message,
            'url': request.env.request_uri if hasattr(request, 'env') else 'unknown',
            'method': request.env.request_method if hasattr(request, 'env') else 'unknown',
            'user_agent': request.env.http_user_agent if hasattr(request, 'env') else 'unknown',
            'ip_address': request.env.remote_addr if hasattr(request, 'env') else 'unknown'
        }
        
        if traceback_info:
            error_context['traceback'] = traceback_info
        
        # Log del error
        log_error(
            error=f"HTTP {code}: {message}",
            context=error_context,
            user_id=auth.user_id if hasattr(auth, 'user_id') and auth.user_id else None
        )
        
        # Determinar vista de error apropiada
        error_view = f'error_{code}.html'
        if not os.path.exists(os.path.join(request.folder, 'views', error_view)):
            error_view = 'error_500.html'  # Vista por defecto
        
        # Configurar respuesta de error
        response.status = code
        response.view = error_view
        
        # Datos adicionales para la vista
        error_data = {
            'error_code': code,
            'error_message': message,
            'timestamp': request.now,
            'request_info': {
                'url': request.env.request_uri if hasattr(request, 'env') else 'N/A',
                'method': request.env.request_method if hasattr(request, 'env') else 'N/A',
                'ip': request.env.remote_addr if hasattr(request, 'env') else 'N/A'
            }
        }
        
        return error_data
        
    except Exception as e:
        # Error manejando el error - usar logging básico
        import logging
        logging.error(f"Error en custom_error_handler: {str(e)}")
        
        # Retornar datos mínimos
        return {
            'error_code': code,
            'error_message': message,
            'timestamp': request.now if hasattr(request, 'now') else None
        }

def setup_web2py_error_handling():
    """Configura el manejo de errores específico de web2py"""
    
    try:
        # Hook para errores HTTP
        def http_error_handler(code, message):
            return custom_error_handler(code, message)
        
        # Hook para errores de aplicación
        def application_error_handler(exception):
            try:
                # Registrar excepción
                log_error(
                    error=exception,
                    context={
                        'type': 'application_error',
                        'controller': request.controller if hasattr(request, 'controller') else 'unknown',
                        'function': request.function if hasattr(request, 'function') else 'unknown'
                    }
                )
                
                # Retornar vista de error 500
                return custom_error_handler(500, str(exception))
                
            except Exception as e:
                import logging
                logging.error(f"Error en application_error_handler: {str(e)}")
                return None
        
        # Configurar handlers en web2py si están disponibles
        if hasattr(response, 'error_handler'):
            response.error_handler = http_error_handler
            
    except Exception as e:
        import logging
        logging.error(f"Error configurando manejo de errores web2py: {str(e)}")

# -------------------------------------------------------------------------
# Decoradores para Manejo de Errores
# -------------------------------------------------------------------------

def handle_controller_errors(func):
    """
    Decorador para manejar errores en controladores
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTP as e:
            # Errores HTTP - dejar que web2py los maneje
            raise
        except Exception as e:
            # Registrar error de aplicación
            log_error(
                error=e,
                context={
                    'controller_function': func.__name__,
                    'args': str(args),
                    'kwargs': str(kwargs)
                }
            )
            
            # Mostrar página de error 500
            raise HTTP(500, "Error interno del servidor")
    
    return wrapper

def handle_database_errors(func):
    """
    Decorador específico para errores de base de datos
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Verificar si es error de BD
            error_str = str(e).lower()
            if any(keyword in error_str for keyword in ['database', 'sql', 'constraint', 'foreign key']):
                log_error(
                    error=e,
                    context={
                        'type': 'database_error',
                        'function': func.__name__
                    }
                )
                
                # Mensaje amigable para usuario
                session.flash = "Error en la base de datos. Por favor, intente nuevamente."
                redirect(URL('default', 'index'))
            else:
                # Re-lanzar si no es error de BD
                raise
    
    return wrapper

def handle_api_errors(func):
    """
    Decorador para errores en APIs externas
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Registrar error de API
            log_error(
                error=e,
                context={
                    'type': 'api_error',
                    'function': func.__name__
                }
            )
            
            # Retornar respuesta de error JSON para APIs
            if request.extension == 'json':
                return response.json({
                    'success': False,
                    'error': 'Error en servicio externo',
                    'code': 'API_ERROR'
                })
            else:
                session.flash = "Error conectando con servicio externo"
                redirect(URL('default', 'index'))
    
    return wrapper

# -------------------------------------------------------------------------
# Funciones de Utilidad para Errores
# -------------------------------------------------------------------------

def log_user_action_error(action, error, user_id=None):
    """
    Registra errores específicos de acciones de usuario
    """
    if not user_id:
        user_id = auth.user_id if hasattr(auth, 'user_id') else None
    
    log_error(
        error=error,
        context={
            'type': 'user_action_error',
            'action': action,
            'user_id': user_id
        },
        user_id=user_id
    )

def log_security_error(error_type, details, user_id=None):
    """
    Registra errores de seguridad
    """
    if not user_id:
        user_id = auth.user_id if hasattr(auth, 'user_id') else None
    
    log_error(
        error=f"Security Error: {error_type}",
        context={
            'type': 'security_error',
            'error_type': error_type,
            'details': details,
            'ip_address': request.env.remote_addr if hasattr(request, 'env') else 'unknown'
        },
        user_id=user_id
    )

def log_transaction_error(transaction_type, error, account_id=None, amount=None):
    """
    Registra errores específicos de transacciones
    """
    log_error(
        error=error,
        context={
            'type': 'transaction_error',
            'transaction_type': transaction_type,
            'account_id': account_id,
            'amount': amount
        }
    )

def create_error_report(error_id=None, days=7):
    """
    Crea un reporte de errores para administradores
    """
    try:
        from datetime import datetime, timedelta
        
        # Obtener estadísticas de errores
        stats = error_handler.get_error_statistics(days=days)
        
        if not stats:
            return None
        
        # Crear reporte
        report = {
            'period': f"Últimos {days} días",
            'generated_at': datetime.now().isoformat(),
            'statistics': stats,
            'recommendations': []
        }
        
        # Agregar recomendaciones basadas en estadísticas
        if stats['unresolved_count'] > 10:
            report['recommendations'].append(
                "Alto número de errores sin resolver. Revisar logs de sistema."
            )
        
        # Verificar errores críticos
        critical_errors = [error for error, count in stats['error_counts'] 
                          if error in ['DatabaseError', 'SecurityError', 'AuthenticationError']]
        
        if critical_errors:
            report['recommendations'].append(
                f"Errores críticos detectados: {', '.join(critical_errors)}. Revisar inmediatamente."
            )
        
        return report
        
    except Exception as e:
        log_error(e, context={'function': 'create_error_report'})
        return None

# -------------------------------------------------------------------------
# Inicialización del Sistema de Errores
# -------------------------------------------------------------------------

# Configurar manejo de errores al cargar el modelo
try:
    configure_error_handling()
    setup_web2py_error_handling()
    
    # Log de inicialización exitosa
    log_info("Sistema de manejo de errores inicializado correctamente")
    
except Exception as e:
    # Error crítico en inicialización
    import logging
    logging.error(f"Error crítico inicializando sistema de errores: {str(e)}")

# -------------------------------------------------------------------------
# Variables globales para uso en controladores
# -------------------------------------------------------------------------

# Exportar decoradores y funciones para uso en controladores
__all__ = [
    'handle_controller_errors',
    'handle_database_errors', 
    'handle_api_errors',
    'log_user_action_error',
    'log_security_error',
    'log_transaction_error',
    'create_error_report',
    'custom_error_handler'
]