# -*- coding: utf-8 -*-
# Sistema de Divisas Bancario - Configuración de Menú

# ----------------------------------------------------------------------------------------------------------------------
# Configuración del menú principal del sistema
# ----------------------------------------------------------------------------------------------------------------------

# Inicializar menú vacío
response.menu = []

# Menú para usuarios no autenticados
if not auth.is_logged_in():
    response.menu = [
        ('Inicio', False, URL('default', 'index'), []),
        ('Iniciar Sesión', False, URL('default', 'user/login'), []),
        ('Registrarse', False, URL('default', 'user/register'), [])
    ]
else:
    # Menú base para usuarios autenticados
    response.menu = [
        ('Dashboard', False, URL('default', 'dashboard'), [])
    ]
    
    # Verificar si el usuario es cliente
    cliente = db(db.clientes.user_id == auth.user.id).select().first() if auth.user else None
    
    # Menú de divisas para clientes Y administradores/operadores
    if cliente or auth.has_membership('administrador') or auth.has_membership('operador'):
        response.menu.extend([
            ('Divisas', False, '#', [
                ('Comprar Divisas', False, URL('divisas', 'comprar')),
                ('Vender Divisas', False, URL('divisas', 'vender')),
                ('Historial de Transacciones', False, URL('divisas', 'historial_transacciones')),
                ('Tasas Actuales', False, URL('api', 'index'))
            ])
        ])
    
    if cliente:
        # Menú específico para clientes
        response.menu.extend([
            ('Mis Cuentas', False, '#', [
                ('Consultar Saldos', False, URL('cuentas', 'consultar')),
                ('Movimientos', False, URL('cuentas', 'movimientos')),
                ('Crear Nueva Cuenta', False, URL('cuentas', 'crear'))
            ]),
            ('Mi Perfil', False, '#', [
                ('Datos Personales', False, URL('default', 'user/profile')),
                ('Información Bancaria', False, URL('clientes', 'perfil')),
                ('Cambiar Contraseña', False, URL('default', 'user/change_password'))
            ])
        ])
    
    # Menú adicional para administradores y operadores
    if auth.has_membership('administrador') or auth.has_membership('operador'):
        response.menu.extend([
            ('Gestión', False, '#', [
                ('Clientes', False, URL('clientes', 'listar')),
                ('Todas las Cuentas', False, URL('cuentas', 'listar_todas')),
                ('Transacciones del Sistema', False, URL('reportes', 'transacciones'))
            ]),
            ('Reportes', False, '#', [
                ('Reportes Administrativos', False, URL('reportes', 'reportes_administrativos')),
                ('Historial del Sistema', False, URL('reportes', 'historial_transacciones')),
                ('Exportar Datos', False, URL('reportes', 'exportar'))
            ]),
            ('Sistema', False, '#', [
                ('Tasas BCV', False, URL('api', 'index')),
                ('Configuración', False, URL('appadmin', 'index')),
                ('Logs del Sistema', False, URL('admin', 'default', 'errors/' + request.application))
            ])
        ])
    
    # Menú exclusivo para administradores
    if auth.has_membership('administrador'):
        response.menu.extend([
            ('Administración', False, '#', [
                ('Panel de Control', False, URL('admin', 'index')),
                ('Logs de Auditoría', False, URL('admin', 'logs_auditoria')),
                ('Gestionar Usuarios', False, URL('admin', 'gestionar_usuarios')),
                ('Estadísticas', False, URL('admin', 'estadisticas_auditoria')),
                ('Configuración Sistema', False, URL('admin', 'configuracion'))
            ])
        ])
    
    # Agregar opción de cerrar sesión
    response.menu.append(('Cerrar Sesión', False, URL('default', 'user/logout'), []))

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        (T('My Sites'), False, URL('admin', 'default', 'site')),
        (T('This App'), False, '#', [
            (T('Design'), False, URL('admin', 'default', 'design/%s' % _app)),
            (T('Controller'), False,
             URL(
                 'admin', 'default', 'edit/%s/controllers/%s.py' % (_app, request.controller))),
            (T('View'), False,
             URL(
                 'admin', 'default', 'edit/%s/views/%s' % (_app, response.view))),
            (T('DB Model'), False,
             URL(
                 'admin', 'default', 'edit/%s/models/db.py' % _app)),
            (T('Menu Model'), False,
             URL(
                 'admin', 'default', 'edit/%s/models/menu.py' % _app)),
            (T('Config.ini'), False,
             URL(
                 'admin', 'default', 'edit/%s/private/appconfig.ini' % _app)),
            (T('Layout'), False,
             URL(
                 'admin', 'default', 'edit/%s/views/layout.html' % _app)),
            (T('Stylesheet'), False,
             URL(
                 'admin', 'default', 'edit/%s/static/css/web2py-bootstrap3.css' % _app)),
            (T('Database'), False, URL(_app, 'appadmin', 'index')),
            (T('Errors'), False, URL(
                'admin', 'default', 'errors/' + _app)),
            (T('About'), False, URL(
                'admin', 'default', 'about/' + _app)),
        ]),
        ('web2py.com', False, '#', [
            (T('Download'), False,
             'http://www.web2py.com/examples/default/download'),
            (T('Support'), False,
             'http://www.web2py.com/examples/default/support'),
            (T('Demo'), False, 'http://web2py.com/demo_admin'),
            (T('Quick Examples'), False,
             'http://web2py.com/examples/default/examples'),
            (T('FAQ'), False, 'http://web2py.com/AlterEgo'),
            (T('Videos'), False,
             'http://www.web2py.com/examples/default/videos/'),
            (T('Free Applications'),
             False, 'http://web2py.com/appliances'),
            (T('Plugins'), False, 'http://web2py.com/plugins'),
            (T('Recipes'), False, 'http://web2pyslices.com/'),
        ]),
        (T('Documentation'), False, '#', [
            (T('Online book'), False, 'http://www.web2py.com/book'),
            (T('Preface'), False,
             'http://www.web2py.com/book/default/chapter/00'),
            (T('Introduction'), False,
             'http://www.web2py.com/book/default/chapter/01'),
            (T('Python'), False,
             'http://www.web2py.com/book/default/chapter/02'),
            (T('Overview'), False,
             'http://www.web2py.com/book/default/chapter/03'),
            (T('The Core'), False,
             'http://www.web2py.com/book/default/chapter/04'),
            (T('The Views'), False,
             'http://www.web2py.com/book/default/chapter/05'),
            (T('Database'), False,
             'http://www.web2py.com/book/default/chapter/06'),
            (T('Forms and Validators'), False,
             'http://www.web2py.com/book/default/chapter/07'),
            (T('Email and SMS'), False,
             'http://www.web2py.com/book/default/chapter/08'),
            (T('Access Control'), False,
             'http://www.web2py.com/book/default/chapter/09'),
            (T('Services'), False,
             'http://www.web2py.com/book/default/chapter/10'),
            (T('Ajax Recipes'), False,
             'http://www.web2py.com/book/default/chapter/11'),
            (T('Components and Plugins'), False,
             'http://www.web2py.com/book/default/chapter/12'),
            (T('Deployment Recipes'), False,
             'http://www.web2py.com/book/default/chapter/13'),
            (T('Other Recipes'), False,
             'http://www.web2py.com/book/default/chapter/14'),
            (T('Helping web2py'), False,
             'http://www.web2py.com/book/default/chapter/15'),
            (T("Buy web2py's book"), False,
             'http://stores.lulu.com/web2py'),
        ]),
        (T('Community'), False, None, [
            (T('Groups'), False,
             'http://www.web2py.com/examples/default/usergroups'),
            (T('Twitter'), False, 'http://twitter.com/web2py'),
            (T('Live Chat'), False,
             'http://webchat.freenode.net/?channels=web2py'),
        ]),
    ]

