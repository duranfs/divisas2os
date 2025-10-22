# -*- coding: utf-8 -*-
"""
Controlador de Administración - Sistema de Divisas Bancario
Funciones administrativas y de auditoría
"""

import datetime
from dateutil.relativedelta import relativedelta

# -------------------------------------------------------------------------
# Panel de Administración Principal
# -------------------------------------------------------------------------

@auth.requires_login()
@requiere_rol('administrador')
def index():
    """
    Panel principal de administración
    """
    try:
        # Registrar acceso al módulo
        log_acceso_modulo('admin', 'consultar')
        
        # Obtener estadísticas generales
        total_clientes = db(db.clientes.id > 0).count()
        total_cuentas = db(db.cuentas.id > 0).count()
        total_transacciones = db(db.transacciones.id > 0).count()
        
        # Transacciones del día
        hoy = datetime.date.today()
        transacciones_hoy = db(
            db.transacciones.fecha_transaccion >= hoy
        ).count()
        
        # Obtener últimas transacciones
        ultimas_transacciones = db(
            db.transacciones.id > 0
        ).select(
            orderby=~db.transacciones.fecha_transaccion,
            limitby=(0, 10)
        )
        
        # Obtener logs de auditoría recientes
        logs_recientes = db(
            db.logs_auditoria.id > 0
        ).select(
            orderby=~db.logs_auditoria.fecha_accion,
            limitby=(0, 20)
        )
        
        # Obtener estadísticas de errores
        from modules.error_handler import get_error_statistics
        error_stats = get_error_statistics(days=7)
        
        return dict(
            total_clientes=total_clientes,
            total_cuentas=total_cuentas,
            total_transacciones=total_transacciones,
            transacciones_hoy=transacciones_hoy,
            ultimas_transacciones=ultimas_transacciones,
            logs_recientes=logs_recientes
        )
        
    except Exception as e:
        log_auditoria(
            accion='consultar',
            modulo='admin',
            resultado='fallido',
            mensaje_error=str(e)
        )
        response.flash = f"Error cargando panel de administración: {str(e)}"
        return dict(
            total_clientes=0,
            total_cuentas=0,
            total_transacciones=0,
            transacciones_hoy=0,
            ultimas_transacciones=[],
            logs_recientes=[]
        )

# -------------------------------------------------------------------------
# Gestión de Logs de Auditoría
# -------------------------------------------------------------------------

@auth.requires_login()
@requiere_rol('administrador')
def logs_auditoria():
    """
    Consulta y filtrado de logs de auditoría
    """
    try:
        # Registrar acceso al módulo
        log_acceso_modulo('admin', 'consultar')
        
        # Parámetros de filtrado
        fecha_inicio = request.vars.fecha_inicio
        fecha_fin = request.vars.fecha_fin
        modulo = request.vars.modulo
        accion = request.vars.accion
        usuario_id = request.vars.usuario_id
        resultado = request.vars.resultado
        
        # Construir query base
        query = db.logs_auditoria.id > 0
        
        # Aplicar filtros
        if fecha_inicio:
            try:
                fecha_inicio_dt = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
                query &= db.logs_auditoria.fecha_accion >= fecha_inicio_dt
            except ValueError:
                response.flash = "Formato de fecha inicio inválido"
        
        if fecha_fin:
            try:
                fecha_fin_dt = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d')
                fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
                query &= db.logs_auditoria.fecha_accion <= fecha_fin_dt
            except ValueError:
                response.flash = "Formato de fecha fin inválido"
        
        if modulo and modulo != 'todos':
            query &= db.logs_auditoria.modulo == modulo
        
        if accion and accion != 'todas':
            query &= db.logs_auditoria.accion == accion
        
        if usuario_id and usuario_id != 'todos':
            query &= db.logs_auditoria.usuario_id == usuario_id
        
        if resultado and resultado != 'todos':
            query &= db.logs_auditoria.resultado == resultado
        
        # Paginación
        page = int(request.vars.page or 1)
        items_per_page = 50
        offset = (page - 1) * items_per_page
        
        # Obtener logs
        logs = db(query).select(
            orderby=~db.logs_auditoria.fecha_accion,
            limitby=(offset, offset + items_per_page)
        )
        
        # Contar total para paginación
        total_logs = db(query).count()
        total_pages = (total_logs + items_per_page - 1) // items_per_page
        
        # Obtener listas para filtros
        modulos = db().select(
            db.logs_auditoria.modulo,
            distinct=True,
            orderby=db.logs_auditoria.modulo
        )
        
        acciones = db().select(
            db.logs_auditoria.accion,
            distinct=True,
            orderby=db.logs_auditoria.accion
        )
        
        usuarios = db(
            db.auth_user.id.belongs(
                db().select(db.logs_auditoria.usuario_id, distinct=True)
            )
        ).select(orderby=db.auth_user.first_name)
        
        return dict(
            logs=logs,
            modulos=modulos,
            acciones=acciones,
            usuarios=usuarios,
            filtros={
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'modulo': modulo,
                'accion': accion,
                'usuario_id': usuario_id,
                'resultado': resultado
            },
            paginacion={
                'page': page,
                'total_pages': total_pages,
                'total_logs': total_logs,
                'items_per_page': items_per_page
            }
        )
        
    except Exception as e:
        log_auditoria(
            accion='consultar',
            modulo='admin',
            resultado='fallido',
            mensaje_error=str(e)
        )
        response.flash = f"Error consultando logs de auditoría: {str(e)}"
        return dict(
            logs=[],
            modulos=[],
            acciones=[],
            usuarios=[],
            filtros={},
            paginacion={}
        )

# -------------------------------------------------------------------------
# Estadísticas de Auditoría
# -------------------------------------------------------------------------

@auth.requires_login()
@requiere_rol('administrador')
def estadisticas_auditoria():
    """
    Estadísticas y métricas de auditoría
    """
    try:
        # Registrar acceso al módulo
        log_acceso_modulo('admin', 'consultar')
        
        # Período de análisis (último mes por defecto)
        fecha_fin = datetime.date.today()
        fecha_inicio = fecha_fin - relativedelta(months=1)
        
        if request.vars.fecha_inicio:
            fecha_inicio = datetime.datetime.strptime(request.vars.fecha_inicio, '%Y-%m-%d').date()
        
        if request.vars.fecha_fin:
            fecha_fin = datetime.datetime.strptime(request.vars.fecha_fin, '%Y-%m-%d').date()
        
        # Obtener estadísticas
        stats = obtener_estadisticas_auditoria(fecha_inicio, fecha_fin)
        
        # Estadísticas por día
        stats_diarias = db(
            (db.logs_auditoria.fecha_accion >= fecha_inicio) &
            (db.logs_auditoria.fecha_accion <= fecha_fin)
        ).select(
            db.logs_auditoria.fecha_accion.date().with_alias('fecha'),
            db.logs_auditoria.id.count().with_alias('total'),
            groupby=db.logs_auditoria.fecha_accion.date(),
            orderby=db.logs_auditoria.fecha_accion.date()
        )
        
        # Top usuarios más activos
        usuarios_activos = db(
            (db.logs_auditoria.fecha_accion >= fecha_inicio) &
            (db.logs_auditoria.fecha_accion <= fecha_fin) &
            (db.logs_auditoria.usuario_id != None)
        ).select(
            db.logs_auditoria.usuario_id,
            db.auth_user.first_name,
            db.auth_user.last_name,
            db.logs_auditoria.id.count().with_alias('total_acciones'),
            left=db.auth_user.on(db.auth_user.id == db.logs_auditoria.usuario_id),
            groupby=db.logs_auditoria.usuario_id,
            orderby=~db.logs_auditoria.id.count(),
            limitby=(0, 10)
        )
        
        # Errores recientes
        errores_recientes = db(
            (db.logs_auditoria.resultado == 'fallido') &
            (db.logs_auditoria.fecha_accion >= fecha_inicio) &
            (db.logs_auditoria.fecha_accion <= fecha_fin)
        ).select(
            orderby=~db.logs_auditoria.fecha_accion,
            limitby=(0, 20)
        )
        
        return dict(
            stats=stats,
            stats_diarias=stats_diarias,
            usuarios_activos=usuarios_activos,
            errores_recientes=errores_recientes,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        
    except Exception as e:
        log_auditoria(
            accion='consultar',
            modulo='admin',
            resultado='fallido',
            mensaje_error=str(e)
        )
        response.flash = f"Error generando estadísticas: {str(e)}"
        return dict(
            stats={},
            stats_diarias=[],
            usuarios_activos=[],
            errores_recientes=[],
            fecha_inicio=datetime.date.today(),
            fecha_fin=datetime.date.today()
        )

# -------------------------------------------------------------------------
# Gestión de Usuarios y Roles
# -------------------------------------------------------------------------

@auth.requires_login()
@requiere_rol('administrador')
def gestionar_usuarios():
    """
    Gestión de usuarios y asignación de roles
    """
    try:
        # Registrar acceso al módulo
        log_acceso_modulo('admin', 'consultar')
        
        # Obtener todos los usuarios con sus roles
        usuarios = db(
            db.auth_user.id > 0
        ).select(
            db.auth_user.ALL,
            left=[
                db.clientes.on(db.clientes.user_id == db.auth_user.id),
                db.auth_membership.on(db.auth_membership.user_id == db.auth_user.id),
                db.auth_group.on(db.auth_group.id == db.auth_membership.group_id)
            ],
            orderby=db.auth_user.first_name
        )
        
        # Procesar cambio de rol si se envió el formulario
        if request.vars.cambiar_rol and request.vars.user_id and request.vars.nuevo_rol:
            try:
                user_id = int(request.vars.user_id)
                nuevo_rol = request.vars.nuevo_rol
                
                # Remover roles existentes
                db(db.auth_membership.user_id == user_id).delete()
                
                # Asignar nuevo rol
                grupo = db(db.auth_group.role == nuevo_rol).select().first()
                if grupo:
                    auth.add_membership(grupo.id, user_id)
                    
                    # Registrar cambio en auditoría
                    log_auditoria(
                        accion='cambio_rol',
                        modulo='admin',
                        tabla_afectada='auth_membership',
                        registro_id=user_id,
                        datos_nuevos={'nuevo_rol': nuevo_rol},
                        resultado='exitoso'
                    )
                    
                    session.flash = f"Rol cambiado exitosamente a {nuevo_rol}"
                else:
                    session.flash = "Rol no válido"
                    
            except Exception as e:
                log_auditoria(
                    accion='cambio_rol',
                    modulo='admin',
                    resultado='fallido',
                    mensaje_error=str(e)
                )
                session.flash = f"Error cambiando rol: {str(e)}"
            
            redirect(URL('admin', 'gestionar_usuarios'))
        
        # Obtener roles disponibles
        roles = db(db.auth_group.id > 0).select(orderby=db.auth_group.role)
        
        return dict(
            usuarios=usuarios,
            roles=roles
        )
        
    except Exception as e:
        log_auditoria(
            accion='consultar',
            modulo='admin',
            resultado='fallido',
            mensaje_error=str(e)
        )
        response.flash = f"Error gestionando usuarios: {str(e)}"
        return dict(usuarios=[], roles=[])

# -------------------------------------------------------------------------
# Configuración del Sistema
# -------------------------------------------------------------------------

@auth.requires_login()
@requiere_rol('administrador')
def configuracion():
    """
    Gestión de configuración del sistema
    """
    try:
        # Registrar acceso al módulo
        log_acceso_modulo('admin', 'consultar')
        
        # Procesar actualización de configuración
        if request.vars.actualizar_config:
            try:
                clave = request.vars.clave
                nuevo_valor = request.vars.valor
                
                if clave and nuevo_valor is not None:
                    # Obtener valor anterior
                    config_actual = db(db.configuracion.clave == clave).select().first()
                    valor_anterior = config_actual.valor if config_actual else None
                    
                    # Actualizar configuración
                    db(db.configuracion.clave == clave).update(
                        valor=nuevo_valor,
                        fecha_actualizacion=datetime.datetime.now()
                    )
                    
                    # Registrar cambio en auditoría
                    log_cambio_configuracion(clave, valor_anterior, nuevo_valor)
                    
                    session.flash = f"Configuración '{clave}' actualizada exitosamente"
                else:
                    session.flash = "Parámetros inválidos"
                    
            except Exception as e:
                log_auditoria(
                    accion='actualizar',
                    modulo='configuracion',
                    resultado='fallido',
                    mensaje_error=str(e)
                )
                session.flash = f"Error actualizando configuración: {str(e)}"
            
            redirect(URL('admin', 'configuracion'))
        
        # Obtener todas las configuraciones
        configuraciones = db(db.configuracion.id > 0).select(
            orderby=db.configuracion.clave
        )
        
        return dict(configuraciones=configuraciones)
        
    except Exception as e:
        log_auditoria(
            accion='consultar',
            modulo='admin',
            resultado='fallido',
            mensaje_error=str(e)
        )
        response.flash = f"Error cargando configuración: {str(e)}"
        return dict(configuraciones=[])

# -------------------------------------------------------------------------
# Gestión de Errores y Logs
# -------------------------------------------------------------------------

@auth.requires_login()
@requiere_rol('administrador')
def logs_errores():
    """
    Visualización y gestión de logs de errores del sistema
    """
    try:
        # Registrar acceso al módulo
        log_acceso_modulo('admin', 'consultar')
        
        # Obtener parámetros de filtro
        fecha_inicio = request.vars.fecha_inicio
        fecha_fin = request.vars.fecha_fin
        tipo_error = request.vars.tipo_error
        usuario_id = request.vars.usuario_id
        
        # Construir query base
        query = db.system_errors.id > 0
        
        # Aplicar filtros
        if fecha_inicio:
            try:
                fecha_inicio_dt = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
                query &= db.system_errors.timestamp >= fecha_inicio_dt
            except ValueError:
                session.flash = "Formato de fecha inicio inválido"
        
        if fecha_fin:
            try:
                fecha_fin_dt = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d')
                fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
                query &= db.system_errors.timestamp <= fecha_fin_dt
            except ValueError:
                session.flash = "Formato de fecha fin inválido"
        
        if tipo_error:
            query &= db.system_errors.error_type == tipo_error
        
        if usuario_id:
            try:
                query &= db.system_errors.user_id == int(usuario_id)
            except ValueError:
                session.flash = "ID de usuario inválido"
        
        # Obtener errores con paginación
        page = int(request.vars.page or 1)
        items_per_page = 25
        
        total_errors = db(query).count()
        errors = db(query).select(
            orderby=~db.system_errors.timestamp,
            limitby=((page-1)*items_per_page, page*items_per_page)
        )
        
        # Obtener estadísticas de errores
        from modules.error_handler import get_error_statistics
        error_stats = get_error_statistics(days=30)
        
        # Obtener tipos de error únicos para filtro
        error_types = db(db.system_errors.id > 0).select(
            db.system_errors.error_type,
            distinct=True,
            orderby=db.system_errors.error_type
        )
        
        # Obtener usuarios para filtro
        users = db(db.auth_user.id > 0).select(
            db.auth_user.id,
            db.auth_user.first_name,
            db.auth_user.last_name,
            db.auth_user.email,
            orderby=db.auth_user.first_name
        )
        
        return dict(
            errors=errors,
            error_stats=error_stats,
            error_types=error_types,
            users=users,
            total_errors=total_errors,
            current_page=page,
            items_per_page=items_per_page,
            total_pages=(total_errors + items_per_page - 1) // items_per_page,
            filters={
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'tipo_error': tipo_error,
                'usuario_id': usuario_id
            }
        )
        
    except Exception as e:
        from modules.error_handler import log_error
        log_error(e, context={'function': 'logs_errores'})
        session.flash = "Error cargando logs de errores"
        redirect(URL('admin', 'index'))

@auth.requires_login()
@requiere_rol('administrador')
def detalle_error():
    """
    Muestra detalles completos de un error específico
    """
    try:
        error_id = request.args(0)
        if not error_id:
            session.flash = "ID de error requerido"
            redirect(URL('admin', 'logs_errores'))
        
        # Obtener error
        error = db.system_errors(error_id)
        if not error:
            session.flash = "Error no encontrado"
            redirect(URL('admin', 'logs_errores'))
        
        # Registrar acceso al detalle
        log_acceso_modulo('admin', 'consultar')
        
        return dict(error=error)
        
    except Exception as e:
        from modules.error_handler import log_error
        log_error(e, context={'function': 'detalle_error'})
        session.flash = "Error cargando detalle del error"
        redirect(URL('admin', 'logs_errores'))

@auth.requires_login()
@requiere_rol('administrador')
def resolver_error():
    """
    Marca un error como resuelto con notas de resolución
    """
    try:
        if request.env.request_method != 'POST':
            raise HTTP(405, "Método no permitido")
        
        error_id = request.vars.error_id
        resolution_notes = request.vars.resolution_notes
        
        if not error_id:
            session.flash = "ID de error requerido"
            redirect(URL('admin', 'logs_errores'))
        
        # Obtener error
        error = db.system_errors(error_id)
        if not error:
            session.flash = "Error no encontrado"
            redirect(URL('admin', 'logs_errores'))
        
        # Actualizar error como resuelto
        error.update_record(
            resolved=True,
            resolution_notes=resolution_notes or "Resuelto por administrador"
        )
        
        # Registrar acción de resolución
        log_auditoria(
            accion='actualizar',
            modulo='admin',
            tabla_afectada='system_errors',
            registro_id=error_id,
            datos_nuevos={'resolved': True, 'resolution_notes': resolution_notes}
        )
        
        session.flash = "Error marcado como resuelto"
        redirect(URL('admin', 'detalle_error', args=[error_id]))
        
    except Exception as e:
        from modules.error_handler import log_error
        log_error(e, context={'function': 'resolver_error'})
        session.flash = "Error resolviendo el error"
        redirect(URL('admin', 'logs_errores'))

@auth.requires_login()
@requiere_rol('administrador')
def reporte_errores():
    """
    Genera reporte detallado de errores del sistema
    """
    try:
        # Obtener parámetros
        formato = request.vars.formato or 'html'
        dias = int(request.vars.dias or 30)
        
        # Obtener estadísticas completas
        from modules.error_handler import get_error_statistics, create_error_report
        
        error_stats = get_error_statistics(days=dias)
        error_report = create_error_report(days=dias)
        
        if formato == 'json':
            return response.json({
                'statistics': error_stats,
                'report': error_report
            })
        elif formato == 'pdf':
            # Generar PDF del reporte
            return generar_reporte_errores_pdf(error_stats, error_report, dias)
        else:
            # Mostrar en HTML
            return dict(
                error_stats=error_stats,
                error_report=error_report,
                dias=dias
            )
        
    except Exception as e:
        from modules.error_handler import log_error
        log_error(e, context={'function': 'reporte_errores'})
        session.flash = "Error generando reporte de errores"
        redirect(URL('admin', 'index'))

def generar_reporte_errores_pdf(error_stats, error_report, dias):
    """
    Genera un reporte PDF de errores del sistema
    """
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        import io
        
        # Crear buffer para PDF
        buffer = io.BytesIO()
        
        # Crear documento
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center
        )
        
        story.append(Paragraph(f"Reporte de Errores del Sistema - Últimos {dias} días", title_style))
        story.append(Spacer(1, 20))
        
        # Información general
        if error_stats:
            story.append(Paragraph("Resumen Ejecutivo", styles['Heading2']))
            
            summary_data = [
                ['Métrica', 'Valor'],
                ['Errores sin resolver', str(error_stats.get('unresolved_count', 0))],
                ['Período analizado', f"{dias} días"],
                ['Fecha de generación', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            ]
            
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 20))
            
            # Errores por tipo
            if error_stats.get('error_counts'):
                story.append(Paragraph("Errores por Tipo", styles['Heading2']))
                
                error_data = [['Tipo de Error', 'Cantidad']]
                for error_type, count in error_stats['error_counts']:
                    error_data.append([error_type, str(count)])
                
                error_table = Table(error_data)
                error_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(error_table)
                story.append(Spacer(1, 20))
        
        # Recomendaciones
        if error_report and error_report.get('recommendations'):
            story.append(Paragraph("Recomendaciones", styles['Heading2']))
            
            for i, recommendation in enumerate(error_report['recommendations'], 1):
                story.append(Paragraph(f"{i}. {recommendation}", styles['Normal']))
                story.append(Spacer(1, 10))
        
        # Construir PDF
        doc.build(story)
        
        # Preparar respuesta
        buffer.seek(0)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="reporte_errores_{datetime.date.today()}.pdf"'
        
        return buffer.getvalue()
        
    except Exception as e:
        from modules.error_handler import log_error
        log_error(e, context={'function': 'generar_reporte_errores_pdf'})
        session.flash = "Error generando PDF del reporte"
        redirect(URL('admin', 'reporte_errores'))

@auth.requires_login()
@requiere_rol('administrador')
def limpiar_logs_antiguos():
    """
    Limpia logs de errores antiguos según política de retención
    """
    try:
        if request.env.request_method != 'POST':
            raise HTTP(405, "Método no permitido")
        
        # Obtener parámetros
        dias_retencion = int(request.vars.dias_retencion or 90)
        confirmar = request.vars.confirmar == 'true'
        
        if not confirmar:
            session.flash = "Debe confirmar la operación"
            redirect(URL('admin', 'logs_errores'))
        
        # Calcular fecha límite
        fecha_limite = datetime.datetime.now() - datetime.timedelta(days=dias_retencion)
        
        # Contar registros a eliminar
        registros_a_eliminar = db(
            (db.system_errors.timestamp < fecha_limite) &
            (db.system_errors.resolved == True)
        ).count()
        
        if registros_a_eliminar == 0:
            session.flash = "No hay registros antiguos para eliminar"
            redirect(URL('admin', 'logs_errores'))
        
        # Eliminar registros antiguos resueltos
        eliminados = db(
            (db.system_errors.timestamp < fecha_limite) &
            (db.system_errors.resolved == True)
        ).delete()
        
        # Registrar acción de limpieza
        log_auditoria(
            accion='eliminar',
            modulo='admin',
            tabla_afectada='system_errors',
            datos_anteriores={'registros_eliminados': eliminados, 'dias_retencion': dias_retencion}
        )
        
        session.flash = f"Se eliminaron {eliminados} registros de errores antiguos"
        redirect(URL('admin', 'logs_errores'))
        
    except Exception as e:
        from modules.error_handler import log_error
        log_error(e, context={'function': 'limpiar_logs_antiguos'})
        session.flash = "Error limpiando logs antiguos"
        redirect(URL('admin', 'logs_errores'))

@auth.requires_login()
@requiere_rol('administrador')
def configurar_alertas_errores():
    """
    Configura alertas automáticas para errores críticos
    """
    try:
        if request.env.request_method == 'POST':
            # Guardar configuración de alertas
            alertas_config = {
                'email_enabled': request.vars.email_enabled == 'on',
                'email_recipients': request.vars.email_recipients or '',
                'critical_threshold': int(request.vars.critical_threshold or 5),
                'notification_interval': int(request.vars.notification_interval or 60)
            }
            
            # Guardar en configuración del sistema
            for key, value in alertas_config.items():
                config_key = f'error_alerts_{key}'
                existing = db(db.configuracion.clave == config_key).select().first()
                
                if existing:
                    existing.update_record(
                        valor=str(value),
                        fecha_actualizacion=datetime.datetime.now()
                    )
                else:
                    db.configuracion.insert(
                        clave=config_key,
                        valor=str(value),
                        descripcion=f'Configuración de alertas de errores: {key}'
                    )
            
            db.commit()
            
            # Registrar cambio de configuración
            log_auditoria(
                accion='actualizar',
                modulo='admin',
                tabla_afectada='configuracion',
                datos_nuevos=alertas_config
            )
            
            session.flash = "Configuración de alertas actualizada"
            redirect(URL('admin', 'configurar_alertas_errores'))
        
        # Obtener configuración actual
        config_actual = {}
        config_keys = ['email_enabled', 'email_recipients', 'critical_threshold', 'notification_interval']
        
        for key in config_keys:
            config_key = f'error_alerts_{key}'
            config = db(db.configuracion.clave == config_key).select().first()
            if config:
                if key in ['email_enabled']:
                    config_actual[key] = config.valor.lower() == 'true'
                elif key in ['critical_threshold', 'notification_interval']:
                    config_actual[key] = int(config.valor)
                else:
                    config_actual[key] = config.valor
            else:
                # Valores por defecto
                if key == 'email_enabled':
                    config_actual[key] = False
                elif key == 'email_recipients':
                    config_actual[key] = ''
                elif key == 'critical_threshold':
                    config_actual[key] = 5
                elif key == 'notification_interval':
                    config_actual[key] = 60
        
        return dict(config=config_actual)
        
    except Exception as e:
        from modules.error_handler import log_error
        log_error(e, context={'function': 'configurar_alertas_errores'})
        session.flash = "Error configurando alertas de errores"
        redirect(URL('admin', 'index'))