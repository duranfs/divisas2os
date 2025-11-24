# -*- coding: utf-8 -*-
"""
Módulo para generar breadcrumbs del sistema de divisas bancario
Versión: 1.1
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
        {'titulo': 'Inicio', 'url': URL('default', 'dashboard'), 'activo': False}
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
        'listar': 'Gestión de Clientes',
        'listar_todas': 'Gestión de Cuentas',
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
    # Excepciones: no agregar breadcrumb intermedio en ciertos casos
    funciones_sin_controlador = {
        'divisas': ['historial_transacciones', 'comprar', 'vender'],
        'clientes': ['listar'],
        'cuentas': ['listar_todas']
    }
    
    agregar_controlador = True
    if request.controller in funciones_sin_controlador:
        if request.function in funciones_sin_controlador[request.controller]:
            agregar_controlador = False
    
    if request.controller != 'default' and agregar_controlador:
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