# -*- coding: utf-8 -*-
"""
Controlador de Gestión de Clientes
Sistema de Divisas Bancario
"""

import re
from datetime import datetime
from gluon.storage import Storage

# -------------------------------------------------------------------------
# Funciones de utilidad para validación
# -------------------------------------------------------------------------

def validar_cedula(cedula):
    """
    Valida el formato de cédula venezolana
    Formato aceptado: V-12345678 o E-12345678
    """
    if not cedula:
        return False, "La cédula es requerida"
    
    # Limpiar espacios y convertir a mayúsculas
    cedula = cedula.strip().upper()
    
    # Validar formato con regex
    patron = r'^[VE]-?\d{7,8}$'
    if not re.match(patron, cedula):
        return False, "Formato de cédula inválido. Use V-12345678 o E-12345678"
    
    # Verificar que no esté ya registrada
    cliente_existente = db(db.clientes.cedula == cedula).select().first()
    if cliente_existente:
        return False, "Esta cédula ya está registrada en el sistema"
    
    return True, "Cédula válida"

def generar_numero_cuenta():
    """
    Genera un número de cuenta único de 20 dígitos
    """
    import random
    while True:
        # Generar número de cuenta con prefijo 2001 (código del banco)
        numero = "2001" + "".join([str(random.randint(0, 9)) for _ in range(16)])
        
        # Verificar que no exista
        cuenta_existente = db(db.cuentas.numero_cuenta == numero).select().first()
        if not cuenta_existente:
            return numero

# -------------------------------------------------------------------------
# Función de registro de clientes
# -------------------------------------------------------------------------

@auth.requires_login()
# @requiere_permiso('create', 'clientes')  # Temporalmente deshabilitado
def registrar():
    """
    Función de registro de nuevos clientes con validación de cédula
    Requisitos: 2.1, 2.2
    """
    
    # Solo administradores y operadores pueden registrar clientes
    if not (auth.has_membership('administrador') or auth.has_membership('operador')):
        session.flash = "No tiene permisos para registrar clientes"
        redirect(URL('default', 'index'))
    
    # Crear objeto form vacío para evitar errores en la vista
    form = Storage()
    form.errors = Storage()
    
    # Procesar formulario con validaciones básicas
    if request.vars.first_name:  # Si se envió el formulario
        try:
            # Debug: log de los datos recibidos
            import logging
            logger = logging.getLogger("web2py.app.clientes")
            logger.info(f"Registrando cliente: {request.vars.first_name} {request.vars.last_name}")
            # Validaciones básicas
            errores = False
            
            # Validar email
            if not request.vars.email:
                form.errors.email = "El email es requerido"
                errores = True
            else:
                usuario_existente = db(db.auth_user.email == request.vars.email).select().first()
                if usuario_existente:
                    form.errors.email = "Este email ya está registrado"
                    errores = True
            
            # Validar cédula
            if request.vars.cedula:
                cedula_existente = db(db.clientes.cedula == request.vars.cedula).select().first()
                if cedula_existente:
                    form.errors.cedula = "Esta cédula ya está registrada"
                    errores = True
            
            # Validar teléfono (opcional pero si se proporciona debe tener formato válido)
            if request.vars.telefono and len(request.vars.telefono) < 10:
                form.errors.telefono = "El teléfono debe tener al menos 10 dígitos"
                errores = True
            
            # Si hay errores, mostrar el formulario con errores
            if errores:
                response.flash = "Por favor corrija los errores indicados"
                return dict(form=form)
            
            # Crear usuario en auth_user
            # Hashear la contraseña manualmente
            from gluon.validators import CRYPT
            password_hash = CRYPT()(request.vars.password)[0]
            
            user_id = db.auth_user.insert(
                first_name=request.vars.first_name,
                last_name=request.vars.last_name,
                email=request.vars.email,
                password=password_hash,
                telefono=request.vars.telefono or '',
                direccion=request.vars.direccion or '',
                fecha_nacimiento=request.vars.fecha_nacimiento,
                estado='activo'
            )
            
            # Crear registro en tabla clientes
            cliente_id = db.clientes.insert(
                user_id=user_id,
                cedula=request.vars.cedula or '',
                fecha_registro=datetime.now()
            )
            
            # Asignar rol de cliente
            auth.add_membership('cliente', user_id)
            
            # Crear cuenta bancaria inicial
            numero_cuenta = generar_numero_cuenta()
            db.cuentas.insert(
                cliente_id=cliente_id,
                numero_cuenta=numero_cuenta,
                tipo_cuenta='corriente',
                saldo_ves=0,
                saldo_usd=0,
                saldo_eur=0,
                estado='activa'
            )
            
            db.commit()
            
            # Registrar en log de auditoría
            log_auditoria(
                accion='crear',
                modulo='clientes',
                tabla_afectada='clientes',
                registro_id=cliente_id,
                datos_nuevos={
                    'cedula': request.vars.cedula or '',
                    'user_id': user_id,
                    'numero_cuenta': numero_cuenta
                },
                resultado='exitoso'
            )
            
            session.flash = f"Cliente registrado exitosamente. Número de cuenta: {numero_cuenta}"
            redirect(URL('clientes', 'listar'))
            
        except Exception as e:
            db.rollback()
            
            # Registrar error en log de auditoría
            log_auditoria(
                accion='crear',
                modulo='clientes',
                tabla_afectada='clientes',
                datos_nuevos={
                    'cedula': request.vars.cedula or 'N/A',
                    'email': request.vars.email or 'N/A'
                },
                resultado='fallido',
                mensaje_error=str(e)
            )
            
            response.flash = f"Error al registrar cliente: {str(e)}"
            return dict(form=form)
    
    return dict(form=form)

# -------------------------------------------------------------------------
# Función de gestión de perfil de cliente
# -------------------------------------------------------------------------

@auth.requires_login()
@requiere_permiso('update', 'clientes')
def perfil():
    """
    Función de gestión de perfil de cliente
    Requisitos: 2.2
    """
    
    # Obtener información del cliente actual
    if auth.has_membership('cliente'):
        # Cliente puede ver/editar solo su propio perfil
        cliente = db((db.clientes.user_id == auth.user.id) & 
                    (db.clientes.user_id == db.auth_user.id)).select(
                        db.clientes.ALL, db.auth_user.ALL).first()
    else:
        # Administradores y operadores pueden ver perfil específico
        cliente_id = request.args(0)
        if not cliente_id:
            session.flash = "ID de cliente requerido"
            redirect(URL('clientes', 'listar'))
        
        cliente = db((db.clientes.id == cliente_id) & 
                    (db.clientes.user_id == db.auth_user.id)).select(
                        db.clientes.ALL, db.auth_user.ALL).first()
    
    if not cliente:
        session.flash = "Cliente no encontrado"
        redirect(URL('default', 'index'))
    
    # Crear formulario de edición
    form = SQLFORM.factory(
        Field('first_name', 'string', label='Nombres', 
              default=cliente.auth_user.first_name, requires=IS_NOT_EMPTY()),
        Field('last_name', 'string', label='Apellidos', 
              default=cliente.auth_user.last_name, requires=IS_NOT_EMPTY()),
        Field('email', 'string', label='Email', 
              default=cliente.auth_user.email, requires=[IS_NOT_EMPTY(), IS_EMAIL()]),
        Field('telefono', 'string', label='Teléfono', 
              default=cliente.auth_user.telefono, requires=IS_NOT_EMPTY()),
        Field('direccion', 'text', label='Dirección', 
              default=cliente.auth_user.direccion, requires=IS_NOT_EMPTY()),
        Field('fecha_nacimiento', 'date', label='Fecha de Nacimiento', 
              default=cliente.auth_user.fecha_nacimiento, requires=IS_DATE()),
        Field('cedula', 'string', label='Cédula', 
              default=cliente.clientes.cedula, writable=False),
        submit_button='Actualizar Perfil',
        formstyle='bootstrap4_inline'
    )
    
    if form.process().accepted:
        try:
            # Verificar que el email no esté usado por otro usuario
            usuario_existente = db((db.auth_user.email == form.vars.email) & 
                                 (db.auth_user.id != cliente.auth_user.id)).select().first()
            if usuario_existente:
                form.errors.email = "Este email ya está registrado por otro usuario"
                response.flash = "Error en la validación de datos"
                return dict(form=form, cliente=cliente)
            
            # Actualizar datos del usuario
            db(db.auth_user.id == cliente.auth_user.id).update(
                first_name=form.vars.first_name,
                last_name=form.vars.last_name,
                email=form.vars.email,
                telefono=form.vars.telefono,
                direccion=form.vars.direccion,
                fecha_nacimiento=form.vars.fecha_nacimiento
            )
            
            db.commit()
            session.flash = "Perfil actualizado exitosamente"
            
            # Redirigir según el rol
            if auth.has_membership('cliente'):
                redirect(URL('default', 'index'))
            else:
                redirect(URL('clientes', 'listar'))
                
        except Exception as e:
            db.rollback()
            response.flash = f"Error al actualizar perfil: {str(e)}"
            
    elif form.errors:
        response.flash = "Por favor corrija los errores en el formulario"
    
    # Obtener cuentas del cliente
    cuentas = db(db.cuentas.cliente_id == cliente.clientes.id).select()
    
    return dict(form=form, cliente=cliente, cuentas=cuentas)

# -------------------------------------------------------------------------
# Función de listado de clientes para administradores
# -------------------------------------------------------------------------

@auth.requires_login()
@requiere_rol('administrador', 'operador')
def listar():
    """
    Función de listado de clientes para administradores
    Requisitos: 2.4
    """
    
    # Solo administradores y operadores pueden ver la lista
    if not (auth.has_membership('administrador') or auth.has_membership('operador')):
        session.flash = "No tiene permisos para ver la lista de clientes"
        redirect(URL('default', 'index'))
    
    # Parámetros de búsqueda y filtrado
    buscar = request.vars.buscar or ''
    estado_filtro = request.vars.estado or 'todos'
    
    # Construir query base
    query = (db.clientes.user_id == db.auth_user.id)
    
    # Aplicar filtros
    if buscar:
        query &= ((db.auth_user.first_name.contains(buscar)) |
                 (db.auth_user.last_name.contains(buscar)) |
                 (db.auth_user.email.contains(buscar)) |
                 (db.clientes.cedula.contains(buscar)))
    
    if estado_filtro != 'todos':
        query &= (db.auth_user.estado == estado_filtro)
    
    # Obtener clientes con paginación
    page = int(request.vars.page or 1)
    items_per_page = 20
    
    total_clientes = db(query).count()
    clientes = db(query).select(
        db.clientes.ALL,
        db.auth_user.ALL,
        limitby=((page-1)*items_per_page, page*items_per_page),
        orderby=db.clientes.fecha_registro
    )
    
    # Calcular información de paginación
    total_pages = (total_clientes + items_per_page - 1) // items_per_page
    
    # Obtener estadísticas
    stats = {
        'total': db(db.clientes.id > 0).count(),
        'activos': db((db.clientes.user_id == db.auth_user.id) & 
                     (db.auth_user.estado == 'activo')).count(),
        'inactivos': db((db.clientes.user_id == db.auth_user.id) & 
                       (db.auth_user.estado == 'inactivo')).count()
    }
    
    return dict(
        clientes=clientes,
        buscar=buscar,
        estado_filtro=estado_filtro,
        page=page,
        total_pages=total_pages,
        total_clientes=total_clientes,
        stats=stats
    )

# -------------------------------------------------------------------------
# Función para cambiar estado de cliente
# -------------------------------------------------------------------------

@auth.requires_login()
def cambiar_estado():
    """
    Función para activar/desactivar clientes
    Solo para administradores
    """
    
    if not auth.has_membership('administrador'):
        session.flash = "No tiene permisos para cambiar estados de clientes"
        redirect(URL('clientes', 'listar'))
    
    cliente_id = request.args(0)
    nuevo_estado = request.args(1)
    
    if not cliente_id or nuevo_estado not in ['activo', 'inactivo']:
        session.flash = "Parámetros inválidos"
        redirect(URL('clientes', 'listar'))
    
    try:
        # Obtener cliente
        cliente = db((db.clientes.id == cliente_id) & 
                    (db.clientes.user_id == db.auth_user.id)).select().first()
        
        if not cliente:
            session.flash = "Cliente no encontrado"
            redirect(URL('clientes', 'listar'))
        
        # Actualizar estado
        db(db.auth_user.id == cliente.clientes.user_id).update(estado=nuevo_estado)
        
        # También actualizar estado de cuentas si se desactiva
        if nuevo_estado == 'inactivo':
            db(db.cuentas.cliente_id == cliente_id).update(estado='inactiva')
        elif nuevo_estado == 'activo':
            db(db.cuentas.cliente_id == cliente_id).update(estado='activa')
        
        db.commit()
        session.flash = f"Cliente {nuevo_estado} exitosamente"
        
    except Exception as e:
        db.rollback()
        session.flash = f"Error al cambiar estado: {str(e)}"
    
    redirect(URL('clientes', 'listar'))

# -------------------------------------------------------------------------
# Función para ver detalles de cliente
# -------------------------------------------------------------------------

@auth.requires_login()
def detalle():
    """
    Función para ver detalles completos de un cliente
    """
    
    if not (auth.has_membership('administrador') or auth.has_membership('operador')):
        session.flash = "No tiene permisos para ver detalles de clientes"
        redirect(URL('default', 'index'))
    
    cliente_id = request.args(0)
    if not cliente_id:
        session.flash = "ID de cliente requerido"
        redirect(URL('clientes', 'listar'))
    
    # Obtener información completa del cliente
    cliente = db((db.clientes.id == cliente_id) & 
                (db.clientes.user_id == db.auth_user.id)).select(
                    db.clientes.ALL, db.auth_user.ALL).first()
    
    if not cliente:
        session.flash = "Cliente no encontrado"
        redirect(URL('clientes', 'listar'))
    
    # Obtener cuentas del cliente
    cuentas = db(db.cuentas.cliente_id == cliente_id).select()
    
    # Obtener últimas transacciones
    ultimas_transacciones = db((db.transacciones.cuenta_id.belongs([c.id for c in cuentas]))).select(
        orderby=~db.transacciones.fecha_transaccion,
        limitby=(0, 10)
    )
    
    return dict(
        cliente=cliente,
        cuentas=cuentas,
        ultimas_transacciones=ultimas_transacciones
    )