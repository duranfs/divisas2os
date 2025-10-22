# -*- coding: utf-8 -*-
"""
Módulo para generar breadcrumbs del sistema de divisas bancario
"""

def generar_breadcrumbs(request):
    """
    Genera breadcrumbs basados en el controlador y función actual
    
    Args:
        request: Objeto request de web2py
        
    Returns:
        list: Lista de diccionarios con información de breadcrumbs
    """
    from gluon import URL
    
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
        'listar_todas': 'Todas las Cuentas',
        'registrar': 'Registro',
        'perfil': 'Perfil',
        'crear': 'Crear Nueva Cuenta',
        'consultar': 'Consultar Saldos',
        'movimientos': 'Movimientos',
        'comprar': 'Comprar Divisas',
        'vender': 'Vender Divisas',
        'historial_transacciones': 'Historial de Transacciones',
        'reportes_administrativos': 'Reportes Administrativos',
        'exportar': 'Exportar Datos',
        'detalle': 'Detalle',
        'gestionar': 'Gestionar',
        'comprobante': 'Comprobante',
        'widget_tasas': 'Widget de Tasas',
        'historial_grafico': 'Gráfico Histórico'
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
    if request.function not in ['index', 'dashboard']:
        titulo_funcion = funciones.get(request.function, request.function.replace('_', ' ').title())
        breadcrumbs.append({
            'titulo': titulo_funcion,
            'url': None,
            'activo': True
        })
    
    return breadcrumbs

def set_breadcrumbs(response, request):
    """
    Establece los breadcrumbs en el objeto response
    
    Args:
        response: Objeto response de web2py
        request: Objeto request de web2py
    """
    response.breadcrumbs = generar_breadcrumbs(request)