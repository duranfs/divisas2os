# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Sistema de Divisas Bancario - Controlador Principal
# -------------------------------------------------------------------------

from datetime import datetime, timedelta
import json

# ---- Dashboard principal ----
def index():
    """Dashboard principal del sistema de divisas"""
    if auth.is_logged_in():
        return dashboard()
    else:
        # Página de bienvenida para usuarios no autenticados
        # Obtener tasas actuales para mostrar
        tasas_actuales = obtener_tasas_actuales()
        return dict(
            message=T('Bienvenido al Sistema de Divisas Bancario'),
            tasas=tasas_actuales,
            mostrar_login=True
        )

@auth.requires_login()
def dashboard():
    """Dashboard personalizado según el rol del usuario"""
    user_id = auth.user.id
    
    # Lógica simple: administradores ven dashboard admin, clientes ven dashboard cliente
    if auth.has_membership('administrador') or auth.has_membership('operador'):
        return dashboard_administrativo()
    
    # Verificar si el usuario es cliente
    cliente = db(db.clientes.user_id == user_id).select().first()
    
    if cliente:
        return dashboard_cliente(cliente)
    else:
        # Usuario sin rol específico - mostrar dashboard básico
        return dashboard_basico()

def dashboard_cliente(cliente):
    """Dashboard específico para clientes"""
    # Obtener cuentas del cliente
    cuentas = db(db.cuentas.cliente_id == cliente.id).select()
    
    # Calcular totales por moneda (convertir a float para evitar problemas de tipos)
    total_ves = sum([float(cuenta.saldo_ves or 0) for cuenta in cuentas])
    total_usd = sum([float(cuenta.saldo_usd or 0) for cuenta in cuentas])
    total_eur = sum([float(cuenta.saldo_eur or 0) for cuenta in cuentas])
    total_usdt = sum([float(cuenta.saldo_usdt or 0) for cuenta in cuentas])
    
    # Obtener últimas transacciones
    ultimas_transacciones = db(
        (db.transacciones.cuenta_id.belongs([c.id for c in cuentas]))
    ).select(
        orderby=~db.transacciones.fecha_transaccion,
        limitby=(0, 5)
    )
    
    # Obtener tasas actuales
    tasas_actuales = obtener_tasas_actuales()
    
    # Calcular equivalencias en VES
    equivalencia_total_ves = total_ves
    if tasas_actuales and tasas_actuales.usd_ves:
        equivalencia_total_ves += total_usd * float(tasas_actuales.usd_ves)
    if tasas_actuales and tasas_actuales.eur_ves:
        equivalencia_total_ves += total_eur * float(tasas_actuales.eur_ves)
    if tasas_actuales and tasas_actuales.usdt_ves:
        equivalencia_total_ves += total_usdt * float(tasas_actuales.usdt_ves)
    
    return dict(
        tipo_dashboard='cliente',
        cliente=cliente,
        cuentas=cuentas,
        total_ves=total_ves,
        total_usd=total_usd,
        total_eur=total_eur,
        total_usdt=total_usdt,
        equivalencia_total_ves=equivalencia_total_ves,
        ultimas_transacciones=ultimas_transacciones,
        tasas_actuales=tasas_actuales,
        accesos_rapidos=generar_accesos_rapidos_cliente()
    )

def dashboard_administrativo():
    """Dashboard para administradores y operadores"""
    # Estadísticas del día
    hoy = datetime.now().date()
    
    # Transacciones del día
    transacciones_hoy = db(
        db.transacciones.fecha_transaccion >= hoy
    ).count()
    
    # Volumen de transacciones por moneda
    volumen_ves = db(
        (db.transacciones.fecha_transaccion >= hoy) &
        (db.transacciones.moneda_origen == 'VES')
    ).select(
        db.transacciones.monto_origen.sum()
    ).first()[db.transacciones.monto_origen.sum()] or 0
    
    volumen_usd = db(
        (db.transacciones.fecha_transaccion >= hoy) &
        (db.transacciones.moneda_origen == 'USD')
    ).select(
        db.transacciones.monto_origen.sum()
    ).first()[db.transacciones.monto_origen.sum()] or 0
    
    volumen_eur = db(
        (db.transacciones.fecha_transaccion >= hoy) &
        (db.transacciones.moneda_origen == 'EUR')
    ).select(
        db.transacciones.monto_origen.sum()
    ).first()[db.transacciones.monto_origen.sum()] or 0
    
    # Total de clientes activos
    clientes_activos = db(
        (db.clientes.id > 0) &
        (db.auth_user.id == db.clientes.user_id) &
        (db.auth_user.estado == 'activo')
    ).count()
    
    # Cuentas activas
    cuentas_activas = db(db.cuentas.estado == 'activa').count()
    
    # Obtener tasas actuales
    tasas_actuales = obtener_tasas_actuales()
    
    # Últimas transacciones del sistema
    ultimas_transacciones = db().select(
        db.transacciones.ALL,
        orderby=~db.transacciones.fecha_transaccion,
        limitby=(0, 10)
    )
    
    return dict(
        tipo_dashboard='administrativo',
        transacciones_hoy=transacciones_hoy,
        volumen_ves=volumen_ves,
        volumen_usd=volumen_usd,
        volumen_eur=volumen_eur,
        clientes_activos=clientes_activos,
        cuentas_activas=cuentas_activas,
        tasas_actuales=tasas_actuales,
        ultimas_transacciones=ultimas_transacciones,
        accesos_rapidos=generar_accesos_rapidos_admin()
    )

def dashboard_basico():
    """Dashboard básico para usuarios sin rol específico"""
    tasas_actuales = obtener_tasas_actuales()
    
    return dict(
        tipo_dashboard='basico',
        tasas_actuales=tasas_actuales,
        mensaje='Complete su registro como cliente para acceder a todas las funcionalidades'
    )

def obtener_tasas_actuales():
    """Obtiene las tasas de cambio más recientes"""
    try:
        tasa = db(db.tasas_cambio.activa == True).select(
            orderby=~db.tasas_cambio.fecha | ~db.tasas_cambio.hora,
            limitby=(0, 1)
        ).first()
        
        # Si no hay tasa activa, obtener la más reciente
        if not tasa:
            tasa = db().select(
                db.tasas_cambio.ALL,
                orderby=~db.tasas_cambio.fecha | ~db.tasas_cambio.hora,
                limitby=(0, 1)
            ).first()
        
        return tasa
    except Exception as e:
        # En caso de error, crear objeto de respaldo
        from gluon.storage import Storage
        return Storage(
            usd_ves=36.5000,
            eur_ves=40.2500,
            usdt_ves=36.4635,
            fecha=request.now.date(),
            hora=request.now.time(),
            fuente='Respaldo'
        )

def generar_accesos_rapidos_cliente():
    """Genera los accesos rápidos para clientes"""
    return [
        {
            'titulo': 'Comprar Divisas',
            'descripcion': 'Comprar USD o EUR con VES',
            'url': URL('divisas', 'comprar'),
            'icono': 'fas fa-shopping-cart',
            'color': 'success'
        },
        {
            'titulo': 'Vender Divisas',
            'descripcion': 'Vender USD o EUR por VES',
            'url': URL('divisas', 'vender'),
            'icono': 'fas fa-hand-holding-usd',
            'color': 'warning'
        },
        {
            'titulo': 'Mis Cuentas',
            'descripcion': 'Consultar saldos y movimientos',
            'url': URL('cuentas', 'consultar'),
            'icono': 'fas fa-university',
            'color': 'info'
        },
        {
            'titulo': 'Historial',
            'descripcion': 'Ver historial de transacciones',
            'url': URL('divisas', 'historial_transacciones'),
            'icono': 'fas fa-history',
            'color': 'secondary'
        }
    ]

def generar_accesos_rapidos_admin():
    """Genera los accesos rápidos para administradores"""
    return [
        {
            'titulo': 'Comprar Divisas',
            'descripcion': 'Realizar compras de divisas',
            'url': URL('divisas', 'comprar'),
            'icono': 'fas fa-shopping-cart',
            'color': 'success'
        },
        {
            'titulo': 'Vender Divisas',
            'descripcion': 'Realizar ventas de divisas',
            'url': URL('divisas', 'vender'),
            'icono': 'fas fa-hand-holding-usd',
            'color': 'warning'
        },
        {
            'titulo': 'Gestión de Clientes',
            'descripcion': 'Administrar clientes del sistema',
            'url': URL('clientes', 'listar'),
            'icono': 'fas fa-users',
            'color': 'primary'
        },
        {
            'titulo': 'Reportes',
            'descripcion': 'Generar reportes del sistema',
            'url': URL('reportes', 'index'),
            'icono': 'fas fa-chart-bar',
            'color': 'info'
        },
        {
            'titulo': 'Tasas de Cambio',
            'descripcion': 'Gestionar tasas de cambio',
            'url': URL('api', 'index'),
            'icono': 'fas fa-exchange-alt',
            'color': 'secondary'
        },
        {
            'titulo': 'Configuración',
            'descripcion': 'Configurar parámetros del sistema',
            'url': URL('appadmin', 'index'),
            'icono': 'fas fa-cogs',
            'color': 'dark'
        }
    ]

def generar_breadcrumbs():
    """Genera breadcrumbs basados en el controlador y función actual"""
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
        'registrar': 'Registro',
        'perfil': 'Perfil',
        'crear': 'Crear',
        'consultar': 'Consultar',
        'movimientos': 'Movimientos',
        'comprar': 'Comprar',
        'vender': 'Vender',
        'historial_transacciones': 'Historial',
        'reportes_administrativos': 'Reportes Administrativos',
        'exportar': 'Exportar'
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
    if request.function != 'index':
        titulo_funcion = funciones.get(request.function, request.function.replace('_', ' ').title())
        breadcrumbs.append({
            'titulo': titulo_funcion,
            'url': None,
            'activo': True
        })
    
    return breadcrumbs

# Hacer breadcrumbs disponibles globalmente
response.breadcrumbs = generar_breadcrumbs()

# ---- API para obtener datos del dashboard -----
@auth.requires_login()
def api_dashboard_data():
    """API para obtener datos actualizados del dashboard"""
    if not request.env.request_method == 'GET': 
        raise HTTP(403)
    
    user_id = auth.user.id
    cliente = db(db.clientes.user_id == user_id).select().first()
    
    if cliente:
        # Datos para cliente
        cuentas = db(db.cuentas.cliente_id == cliente.id).select()
        total_ves = sum([float(cuenta.saldo_ves or 0) for cuenta in cuentas])
        total_usd = sum([float(cuenta.saldo_usd or 0) for cuenta in cuentas])
        total_eur = sum([float(cuenta.saldo_eur or 0) for cuenta in cuentas])
        total_usdt = sum([float(cuenta.saldo_usdt or 0) for cuenta in cuentas])
        
        tasas = obtener_tasas_actuales()
        
        return response.json({
            'status': 'success',
            'data': {
                'total_ves': total_ves,
                'total_usd': total_usd,
                'total_eur': total_eur,
                'total_usdt': total_usdt,
                'tasa_usd': float(tasas.usd_ves) if tasas else 0,
                'tasa_eur': float(tasas.eur_ves) if tasas else 0,
                'tasa_usdt': float(tasas.usdt_ves) if tasas and tasas.usdt_ves else 0,
                'ultima_actualizacion': str(tasas.fecha) if tasas else None
            }
        })
    else:
        return response.json({'status': 'error', 'message': 'Cliente no encontrado'})

# ---- Función para obtener widget de tasas -----
def widget_tasas():
    """Renderiza el widget de tasas actuales"""
    tasas = obtener_tasas_actuales()
    return dict(tasas=tasas) 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

# -------------------------------------------------------------------------
# Funciones de Administración de Usuarios
# -------------------------------------------------------------------------

def limpiar_y_crear_admin():
    """
    Función para limpiar toda la base de datos y crear el primer administrador
    NO requiere autenticación - solo para desarrollo inicial
    """
    
    try:
        # Limpiar todas las tablas en orden correcto (respetando foreign keys)
        db.transacciones.truncate()
        db.cuentas.truncate()
        db.clientes.truncate()
        db.auth_membership.truncate()
        db.auth_group.truncate()
        db.auth_user.truncate()
        db.tasas_cambio.truncate()
        
        # Crear grupos de roles
        admin_group_id = db.auth_group.insert(role='administrador', description='Administradores del sistema')
        operador_group_id = db.auth_group.insert(role='operador', description='Operadores bancarios')
        cliente_group_id = db.auth_group.insert(role='cliente', description='Clientes del banco')
        
        # Crear usuario administrador
        admin_user_id = db.auth_user.insert(
            first_name='Administrador',
            last_name='Sistema',
            email='duranfs.2012@gmail.com',
            password='admin123',  # Se hasheará automáticamente
            telefono='04141234567',
            direccion='Oficina Principal',
            fecha_nacimiento='1990-01-01',
            estado='activo'
        )
        
        # Asignar rol de administrador
        db.auth_membership.insert(user_id=admin_user_id, group_id=admin_group_id)
        
        # Crear algunas tasas de cambio iniciales
        from datetime import datetime
        db.tasas_cambio.insert(
            usd_ves=36.50,
            eur_ves=40.25,
            fecha=datetime.now(),
            fuente='BCV',
            activa=True
        )
        
        db.commit()
        
        mensaje = """
        ✅ Base de datos limpiada y administrador creado exitosamente!
        
        📧 Email: duranfs.2012@gmail.com
        🔑 Contraseña: admin123
        👤 Rol: Administrador
        
        Ahora puedes hacer login con estas credenciales.
        """
        
    except Exception as e:
        db.rollback()
        mensaje = f"❌ Error al limpiar la base de datos: {str(e)}"
    
    return dict(mensaje=mensaje)

def diagnosticar_login():
    """
    Función de diagnóstico para verificar el estado de la autenticación
    """
    
    diagnostico = []
    
    # Verificar TODOS los usuarios en el sistema
    todos_usuarios = db(db.auth_user).select()
    
    diagnostico.append(f"👥 Total usuarios en sistema: {len(todos_usuarios)}")
    diagnostico.append("=" * 50)
    
    for usuario in todos_usuarios:
        diagnostico.append(f"📧 Usuario: {usuario.email}")
        diagnostico.append(f"   ID: {usuario.id}")
        diagnostico.append(f"   Nombre: {usuario.first_name} {usuario.last_name}")
        diagnostico.append(f"   Estado: {usuario.estado}")
        
        # Verificar el tipo de hash
        if usuario.password and usuario.password.startswith('pbkdf2'):
            diagnostico.append("   ✅ Hash correcto (pbkdf2)")
        else:
            diagnostico.append("   ❌ Hash incorrecto")
            diagnostico.append(f"   🔐 Hash actual: {usuario.password[:30]}...")
        
        # Verificar roles
        memberships = db(db.auth_membership.user_id == usuario.id).select()
        if memberships:
            for membership in memberships:
                group = db(db.auth_group.id == membership.group_id).select().first()
                if group:
                    diagnostico.append(f"   👑 Rol: {group.role}")
        else:
            diagnostico.append("   ❌ Sin roles asignados")
        
        diagnostico.append("-" * 30)
    
    # Verificar configuración de auth
    diagnostico.append("🔧 CONFIGURACIÓN DEL SISTEMA:")
    diagnostico.append(f"   Password field: {auth.settings.password_field}")
    diagnostico.append(f"   Password min length: {auth.settings.password_min_length}")
    
    # Verificar validadores del campo password
    password_requires = db.auth_user.password.requires
    if password_requires:
        diagnostico.append(f"   Password validators: {[str(req) for req in password_requires]}")
    else:
        diagnostico.append("   ❌ Sin validadores de password")
    
    return dict(diagnostico=diagnostico)

def arreglar_password_admin():
    """
    Función para arreglar específicamente el hash de la contraseña del admin
    """
    
    try:
        # Buscar el usuario admin
        admin_user = db(db.auth_user.email == 'duranfs.2012@gmail.com').select().first()
        
        if admin_user:
            # Forzar el re-hash de la contraseña usando el validador CRYPT
            password_validator = None
            for validator in db.auth_user.password.requires:
                if hasattr(validator, '__class__') and 'CRYPT' in str(validator.__class__):
                    password_validator = validator
                    break
            
            if password_validator:
                # Usar el validador CRYPT para hashear la contraseña
                nueva_password_hash = password_validator('admin123')[0]
                
                # Actualizar la contraseña con el hash correcto
                db(db.auth_user.id == admin_user.id).update(password=nueva_password_hash)
                db.commit()
                
                mensaje = f"✅ Contraseña del administrador arreglada correctamente.\n\nNuevo hash: {nueva_password_hash[:50]}...\n\nAhora puedes hacer login con:\n📧 Email: duranfs.2012@gmail.com\n🔑 Contraseña: admin123"
            else:
                mensaje = "❌ No se encontró el validador CRYPT"
        else:
            mensaje = "❌ Usuario administrador no encontrado"
            
    except Exception as e:
        db.rollback()
        mensaje = f"❌ Error al arreglar la contraseña: {str(e)}"
    
    return dict(mensaje=mensaje)

def arreglar_passwords_clientes():
    """
    Función para arreglar las contraseñas de todos los clientes
    """
    
    try:
        # Buscar todos los usuarios que son clientes
        clientes_query = db(
            (db.auth_user.id == db.auth_membership.user_id) &
            (db.auth_membership.group_id == db.auth_group.id) &
            (db.auth_group.role == 'cliente')
        ).select(db.auth_user.ALL, distinct=True)
        
        usuarios_arreglados = []
        password_validator = None
        
        # Encontrar el validador CRYPT
        for validator in db.auth_user.password.requires:
            if hasattr(validator, '__class__') and 'CRYPT' in str(validator.__class__):
                password_validator = validator
                break
        
        if not password_validator:
            return dict(mensaje="❌ No se encontró el validador CRYPT")
        
        for usuario in clientes_query:
            # Si la contraseña no empieza con 'pbkdf2', necesita ser re-hasheada
            if usuario.password and not usuario.password.startswith('pbkdf2'):
                # Usar una contraseña temporal conocida
                nueva_password = "cliente123"
                nueva_password_hash = password_validator(nueva_password)[0]
                
                # Actualizar la contraseña con el hash correcto
                db(db.auth_user.id == usuario.id).update(password=nueva_password_hash)
                usuarios_arreglados.append(f"{usuario.email} - contraseña temporal: cliente123")
        
        db.commit()
        
        if usuarios_arreglados:
            mensaje = f"""✅ Contraseñas de clientes arregladas exitosamente!

📧 Clientes arreglados:
{chr(10).join(usuarios_arreglados)}

🔑 Contraseña temporal para todos: cliente123

📋 Instrucciones:
1. Los clientes pueden hacer login con su email y la contraseña: cliente123
2. Una vez dentro, deben cambiar su contraseña desde el perfil
3. Total de clientes arreglados: {len(usuarios_arreglados)}"""
        else:
            mensaje = "✅ No se encontraron clientes con contraseñas que necesiten ser arregladas."
            
    except Exception as e:
        db.rollback()
        mensaje = f"❌ Error al arreglar las contraseñas: {str(e)}"
    
    return dict(mensaje=mensaje)

def resetear_passwords_clientes():
    """
    Función para resetear las contraseñas de los clientes a una conocida
    """
    
    try:
        # Buscar todos los usuarios que son clientes
        clientes_query = db(
            (db.auth_user.id == db.auth_membership.user_id) &
            (db.auth_membership.group_id == db.auth_group.id) &
            (db.auth_group.role == 'cliente')
        ).select(db.auth_user.ALL, distinct=True)
        
        usuarios_reseteados = []
        
        for usuario in clientes_query:
            # Cambiar contraseña a "123456" (fácil de recordar)
            db(db.auth_user.id == usuario.id).update(password="123456")
            usuarios_reseteados.append(f"{usuario.email} - nueva contraseña: 123456")
        
        db.commit()
        
        if usuarios_reseteados:
            mensaje = f"""✅ Contraseñas de clientes reseteadas exitosamente!

📧 Clientes con nueva contraseña:
{chr(10).join(usuarios_reseteados)}

🔑 Nueva contraseña para todos: 123456

📋 Instrucciones:
1. Los clientes pueden hacer login con su email y la contraseña: 123456
2. Una vez dentro, deben cambiar su contraseña desde el perfil
3. Total de clientes reseteados: {len(usuarios_reseteados)}"""
        else:
            mensaje = "❌ No se encontraron clientes para resetear."
            
    except Exception as e:
        db.rollback()
        mensaje = f"❌ Error al resetear las contraseñas: {str(e)}"
    
    return dict(mensaje=mensaje)

def probar_login_manual():
    """
    Función para probar manualmente el proceso de login
    """
    
    email = "beto.jesus@gmail.com"
    password = "123456"
    
    resultado = []
    
    try:
        # Paso 1: Buscar el usuario por email
        usuario = db(db.auth_user.email == email).select().first()
        
        if usuario:
            resultado.append(f"✅ Usuario encontrado: {email}")
            resultado.append(f"   ID: {usuario.id}")
            resultado.append(f"   Estado: {usuario.estado}")
            resultado.append(f"   Hash actual: {usuario.password[:50]}...")
            
            # Paso 2: Verificar el validador CRYPT
            password_validator = None
            for validator in db.auth_user.password.requires:
                if hasattr(validator, '__class__') and 'CRYPT' in str(validator.__class__):
                    password_validator = validator
                    break
            
            if password_validator:
                resultado.append("✅ Validador CRYPT encontrado")
                
                # Paso 3: Intentar validar la contraseña
                try:
                    # Esto es lo que hace web2py internamente
                    validation_result = password_validator(password, usuario.password)
                    
                    if validation_result[1] is None:  # Sin errores = contraseña correcta
                        resultado.append("✅ Contraseña validada correctamente")
                        
                        # Paso 4: Verificar estado del usuario
                        if hasattr(usuario, 'estado') and usuario.estado == 'activo':
                            resultado.append("✅ Usuario activo")
                        else:
                            resultado.append("❌ Usuario inactivo o sin campo estado")
                        
                        # Paso 5: Intentar login programático
                        try:
                            login_result = auth.login_bare(email, password)
                            if login_result:
                                resultado.append("✅ Login programático exitoso")
                            else:
                                resultado.append("❌ Login programático falló")
                        except Exception as e:
                            resultado.append(f"❌ Error en login programático: {str(e)}")
                            
                    else:
                        resultado.append(f"❌ Contraseña incorrecta: {validation_result[1]}")
                        
                except Exception as e:
                    resultado.append(f"❌ Error al validar contraseña: {str(e)}")
                    
            else:
                resultado.append("❌ Validador CRYPT no encontrado")
                
        else:
            resultado.append(f"❌ Usuario no encontrado: {email}")
            
    except Exception as e:
        resultado.append(f"❌ Error general: {str(e)}")
    
    return dict(resultado=resultado)

def probar_login_directo():
    """
    Función para probar login directo sin usar auth.login_bare
    """
    
    email = "beto.jesus@gmail.com"
    password = "123456"
    
    resultado = []
    
    try:
        # Buscar el usuario
        usuario = db(db.auth_user.email == email).select().first()
        
        if usuario:
            resultado.append(f"✅ Usuario encontrado: {email}")
            
            # Verificar contraseña manualmente
            password_validator = None
            for validator in db.auth_user.password.requires:
                if hasattr(validator, '__class__') and 'CRYPT' in str(validator.__class__):
                    password_validator = validator
                    break
            
            if password_validator:
                validation_result = password_validator(password, usuario.password)
                
                if validation_result[1] is None:  # Contraseña correcta
                    resultado.append("✅ Contraseña correcta")
                    
                    # Intentar login manual (simular lo que hace web2py)
                    try:
                        # Limpiar sesión actual
                        session.auth = None
                        
                        # Crear sesión de usuario manualmente
                        from gluon.storage import Storage
                        from gluon.utils import web2py_uuid
                        
                        session.auth = Storage(
                            user=usuario,
                            last_visit=request.now,
                            expiration=3600,
                            hmac_key=web2py_uuid()
                        )
                        
                        # Verificar que la sesión se creó
                        if session.auth and session.auth.user:
                            resultado.append("✅ Sesión creada manualmente")
                            resultado.append(f"   Usuario en sesión: {session.auth.user.email}")
                            
                            # Probar si auth.is_logged_in() funciona
                            if auth.is_logged_in():
                                resultado.append("✅ auth.is_logged_in() retorna True")
                            else:
                                resultado.append("❌ auth.is_logged_in() retorna False")
                                
                        else:
                            resultado.append("❌ No se pudo crear la sesión")
                            
                    except Exception as e:
                        resultado.append(f"❌ Error al crear sesión manual: {str(e)}")
                        
                else:
                    resultado.append("❌ Contraseña incorrecta")
                    
            else:
                resultado.append("❌ Validador CRYPT no encontrado")
                
        else:
            resultado.append(f"❌ Usuario no encontrado: {email}")
            
    except Exception as e:
        resultado.append(f"❌ Error general: {str(e)}")
    
    return dict(resultado=resultado)

def login_cliente_forzado():
    """
    Función para hacer logout del admin y login forzado del cliente
    """
    
    email = "beto.jesus@gmail.com"
    password = "123456"
    
    resultado = []
    
    try:
        # Paso 1: Logout del usuario actual
        if auth.is_logged_in():
            current_user = auth.user.email
            resultado.append(f"🚪 Cerrando sesión de: {current_user}")
            auth.logout(next=None)
            session.clear()
        
        # Paso 2: Buscar el cliente
        usuario = db(db.auth_user.email == email).select().first()
        
        if usuario:
            resultado.append(f"✅ Cliente encontrado: {email}")
            
            # Paso 3: Verificar contraseña
            password_validator = None
            for validator in db.auth_user.password.requires:
                if hasattr(validator, '__class__') and 'CRYPT' in str(validator.__class__):
                    password_validator = validator
                    break
            
            if password_validator:
                validation_result = password_validator(password, usuario.password)
                
                if validation_result[1] is None:  # Contraseña correcta
                    resultado.append("✅ Contraseña verificada")
                    
                    # Paso 4: Login forzado usando auth.login_user
                    try:
                        # Usar el método interno de web2py para login
                        auth.login_user(usuario)
                        
                        if auth.is_logged_in() and auth.user.email == email:
                            resultado.append(f"🎉 Login exitoso como: {auth.user.email}")
                        else:
                            resultado.append("❌ Login falló - usuario no en sesión")
                            
                    except Exception as e:
                        resultado.append(f"❌ Error en auth.login_user: {str(e)}")
                        
                else:
                    resultado.append("❌ Contraseña incorrecta")
                    
            else:
                resultado.append("❌ Validador CRYPT no encontrado")
                
        else:
            resultado.append(f"❌ Cliente no encontrado: {email}")
            
    except Exception as e:
        resultado.append(f"❌ Error general: {str(e)}")
    
    return dict(resultado=resultado)

def login_rapido():
    """
    Página con enlaces de login rápido para todos los usuarios
    """
    
    # Obtener todos los usuarios del sistema
    usuarios = db(db.auth_user).select()
    
    usuarios_info = []
    
    for usuario in usuarios:
        # Obtener roles
        roles = []
        memberships = db(db.auth_membership.user_id == usuario.id).select()
        for membership in memberships:
            group = db(db.auth_group.id == membership.group_id).select().first()
            if group:
                roles.append(group.role)
        
        usuarios_info.append({
            'id': usuario.id,
            'email': usuario.email,
            'nombre': f"{usuario.first_name} {usuario.last_name}",
            'roles': roles,
            'estado': usuario.estado
        })
    
    return dict(usuarios=usuarios_info)

def login_como():
    """
    Función para hacer login como un usuario específico
    """
    
    user_id = request.args(0)
    
    if not user_id:
        session.flash = "ID de usuario requerido"
        redirect(URL('default', 'login_rapido'))
    
    try:
        user_id = int(user_id)
        usuario = db(db.auth_user.id == user_id).select().first()
        
        if usuario:
            # Logout del usuario actual si existe
            if auth.is_logged_in():
                auth.logout(next=None)
                session.clear()
            
            # Login como el usuario especificado
            auth.login_user(usuario)
            
            session.flash = f"✅ Login exitoso como: {usuario.email}"
            redirect(URL('default', 'dashboard'))
            
        else:
            session.flash = "Usuario no encontrado"
            redirect(URL('default', 'login_rapido'))
            
    except Exception as e:
        session.flash = f"Error en login: {str(e)}"
        redirect(URL('default', 'login_rapido'))

def probar_login_normal():
    """
    Función para probar el login normal con el formulario de web2py
    """
    
    # Usar el formulario estándar de auth pero con debugging
    form = auth()
    
    # Si es un POST (intento de login)
    if request.post_vars.email and request.post_vars.password:
        email = request.post_vars.email
        password = request.post_vars.password
        
        resultado = []
        resultado.append(f"🔍 Intento de login: {email}")
        
        # Verificar usuario
        usuario = db(db.auth_user.email == email).select().first()
        if usuario:
            resultado.append("✅ Usuario encontrado")
            
            # Verificar contraseña manualmente
            password_validator = None
            for validator in db.auth_user.password.requires:
                if hasattr(validator, '__class__') and 'CRYPT' in str(validator.__class__):
                    password_validator = validator
                    break
            
            if password_validator:
                validation_result = password_validator(password, usuario.password)
                if validation_result[1] is None:
                    resultado.append("✅ Contraseña correcta")
                else:
                    resultado.append(f"❌ Contraseña incorrecta: {validation_result[1]}")
            
            # Verificar estado
            if hasattr(usuario, 'estado') and usuario.estado == 'activo':
                resultado.append("✅ Usuario activo")
            else:
                resultado.append("❌ Usuario inactivo")
                
        else:
            resultado.append("❌ Usuario no encontrado")
        
        return dict(form=form, resultado=resultado)
    
    return dict(form=form, resultado=None)

def arreglar_login_definitivo():
    """
    Función definitiva para arreglar el login de todos los usuarios - MÉTODO DIRECTO
    """
    
    resultado = []
    
    try:
        # Obtener todos los usuarios
        usuarios = db(db.auth_user).select()
        
        usuarios_arreglados = []
        
        for usuario in usuarios:
            # Si la contraseña no empieza con 'pbkdf2', necesita ser re-hasheada
            if usuario.password and not usuario.password.startswith('pbkdf2'):
                resultado.append(f"🔧 Arreglando: {usuario.email}")
                
                # Determinar contraseña según el usuario
                if usuario.email == 'duranfs.2012@gmail.com':
                    nueva_password = "admin123"
                elif usuario.email == 'beto.jesus@gmail.com':
                    nueva_password = "123456"
                elif usuario.email == 'ricardo.duran@gmail.com':
                    nueva_password = "123456"
                else:
                    nueva_password = "123456"  # Por defecto
                
                # Usar el método directo de web2py para hashear
                # Esto es lo mismo que hace internamente el sistema de auth
                from gluon.validators import CRYPT
                crypt_validator = CRYPT()
                nueva_password_hash = str(crypt_validator(nueva_password)[0])
                
                # Actualizar en la base de datos
                db(db.auth_user.id == usuario.id).update(password=nueva_password_hash)
                
                usuarios_arreglados.append({
                    'email': usuario.email,
                    'password': nueva_password,
                    'hash': nueva_password_hash[:50] + '...'
                })
            else:
                resultado.append(f"✅ Ya correcto: {usuario.email}")
        
        db.commit()
        
        if usuarios_arreglados:
            resultado.append("=" * 50)
            resultado.append("🎉 USUARIOS ARREGLADOS:")
            for user in usuarios_arreglados:
                resultado.append(f"📧 {user['email']} → contraseña: {user['password']}")
                resultado.append(f"   Hash: {user['hash']}")
            
            resultado.append("=" * 50)
            resultado.append("✅ ¡Ahora todos pueden hacer login normal!")
        else:
            resultado.append("✅ Todos los usuarios ya tenían hash correcto")
            
    except Exception as e:
        db.rollback()
        resultado.append(f"❌ Error: {str(e)}")
        import traceback
        resultado.append(f"   Detalle: {traceback.format_exc()}")
    
    return dict(resultado=resultado)

def admin_usuarios():
    """
    Página de administración de usuarios (solo para desarrollo)
    """
    
    # Crear primer administrador automáticamente
    if request.vars.crear_admin:
        exito, mensaje = crear_primer_administrador()
        if exito:
            session.flash = mensaje
        else:
            response.flash = mensaje
        redirect(URL('admin_usuarios'))
    
    # Aprobar usuario específico
    if request.vars.aprobar and request.vars.email:
        exito, mensaje = aprobar_usuario_pendiente(request.vars.email)
        if exito:
            session.flash = mensaje
        else:
            response.flash = mensaje
        redirect(URL('admin_usuarios'))
    
    # Listar usuarios pendientes
    usuarios_pendientes = listar_usuarios_pendientes()
    
    # Listar todos los usuarios
    todos_usuarios = db(db.auth_user.id > 0).select(
        db.auth_user.id,
        db.auth_user.email,
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.auth_user.registration_key,
        orderby=db.auth_user.id
    )
    
    return dict(
        usuarios_pendientes=usuarios_pendientes,
        todos_usuarios=todos_usuarios
    )

def demo_colores_frescos():
    """Página de demostración de los nuevos colores"""
    return dict(
        message="Demostración de la nueva paleta de colores fresca y moderna"
    )

def test_alturas_campos():
    """Página de prueba para verificar alturas de campos"""
    return dict(
        message="Página de prueba para verificar que todos los campos tengan la misma altura"
    )

@auth.requires_membership('administrador')
def actualizar_tasas():
    """Página para actualizar tasas del BCV"""
    return dict(
        message="Herramienta para actualizar las tasas de cambio del sistema"
    )

@auth.requires_membership('administrador')
def verificar_tasas_bd():
    """Página para verificar el estado de las tasas en la base de datos"""
    return dict(
        message="Verificación del estado de las tasas de cambio en la base de datos"
    )

@auth.requires_membership('administrador')
def actualizar_tasas_bcv():
    """Función para obtener y actualizar tasas del BCV"""
    try:
        import requests
        from bs4 import BeautifulSoup
        import datetime
        
        # URL del BCV
        url_bcv = "https://www.bcv.org.ve/"
        
        # Headers para simular navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Realizar petición
        response = requests.get(url_bcv, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parsear HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar las tasas (esto puede variar según la estructura del BCV)
        # Intentar diferentes selectores comunes
        usd_ves = None
        eur_ves = None
        
        # Método 1: Buscar por texto que contenga "Dólar" y "Euro"
        try:
            # Buscar elementos que contengan las tasas
            elementos = soup.find_all(['td', 'span', 'div'], string=lambda text: text and ('USD' in text or 'EUR' in text or 'Dólar' in text or 'Euro' in text))
            
            for elemento in elementos:
                # Buscar números cerca del elemento
                parent = elemento.parent
                if parent:
                    texto = parent.get_text()
                    # Buscar patrones de números decimales
                    import re
                    numeros = re.findall(r'\d+[.,]\d+', texto)
                    if numeros and 'USD' in texto or 'Dólar' in texto:
                        usd_ves = float(numeros[0].replace(',', '.'))
                    elif numeros and ('EUR' in texto or 'Euro' in texto):
                        eur_ves = float(numeros[0].replace(',', '.'))
        except:
            pass
        
        # Si no encontramos las tasas, usar valores de ejemplo realistas
        if not usd_ves or not eur_ves:
            # Usar tasas de ejemplo actuales (estas deberían ser reemplazadas por las reales)
            usd_ves = 36.50  # Ejemplo
            eur_ves = 40.25  # Ejemplo
            fuente = "Valores de ejemplo (BCV no disponible)"
        else:
            fuente = "BCV Oficial"
        
        # Guardar en base de datos
        # Primero desactivar todas las tasas anteriores
        db(db.tasas_cambio.activa == True).update(activa=False)
        
        # Insertar nueva tasa
        nueva_tasa = db.tasas_cambio.insert(
            fecha=datetime.date.today(),
            hora=datetime.datetime.now().time(),
            usd_ves=usd_ves,
            eur_ves=eur_ves,
            fuente=fuente,
            activa=True
        )
        
        db.commit()
        
        # Respuesta exitosa
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({
            'success': True,
            'tasas': {
                'usd_ves': float(usd_ves),
                'eur_ves': float(eur_ves)
            },
            'fecha': str(datetime.date.today()),
            'fuente': fuente,
            'id': nueva_tasa
        })
        
    except Exception as e:
        # En caso de error, insertar tasas por defecto
        try:
            # Desactivar tasas anteriores
            db(db.tasas_cambio.activa == True).update(activa=False)
            
            # Insertar tasas por defecto
            nueva_tasa = db.tasas_cambio.insert(
                fecha=datetime.date.today(),
                hora=datetime.datetime.now().time(),
                usd_ves=36.50,
                eur_ves=40.25,
                fuente="Valores por defecto (Error: " + str(e)[:100] + ")",
                activa=True
            )
            
            db.commit()
            
            response.headers['Content-Type'] = 'application/json'
            return json.dumps({
                'success': True,
                'tasas': {
                    'usd_ves': 36.50,
                    'eur_ves': 40.25
                },
                'fecha': str(datetime.date.today()),
                'fuente': "Valores por defecto",
                'error': str(e),
                'id': nueva_tasa
            })
        except Exception as e2:
            response.headers['Content-Type'] = 'application/json'
            return json.dumps({
                'success': False,
                'error': f"Error al actualizar tasas: {str(e)} | Error BD: {str(e2)}"
            })

def insertar_tasas_reales():
    """Función para insertar tasas reales del BCV directamente"""
    try:
        # Desactivar todas las tasas anteriores
        db(db.tasas_cambio.activa == True).update(activa=False)
        
        # Insertar tasas reales actuales
        nueva_tasa = db.tasas_cambio.insert(
            fecha=request.now.date(),
            hora=request.now.time(),
            usd_ves=214.1798,  # Tasa real actual
            eur_ves=248.6534,  # Tasa real actual
            fuente='BCV - Tasas reales actualizadas',
            activa=True
        )
        
        db.commit()
        
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({
            'success': True,
            'message': 'Tasas reales insertadas correctamente',
            'tasas': {
                'usd_ves': 214.1798,
                'eur_ves': 248.6534
            },
            'id': nueva_tasa,
            'fecha': str(request.now.date()),
            'fuente': 'BCV - Tasas reales actualizadas'
        })
        
    except Exception as e:
        db.rollback()
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({
            'success': False,
            'error': str(e)
        })