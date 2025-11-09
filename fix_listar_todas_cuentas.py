#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Corrección para la función listar_todas del controlador de cuentas
"""

def crear_listar_todas_corregida():
    """Crea una versión corregida de la función listar_todas"""
    
    funcion_corregida = '''
@auth.requires_membership('administrador')
def listar_todas():
    """Listar todas las cuentas del sistema (solo administradores) - Versión corregida"""
    try:
        # Log de acceso para auditoría
        import logging
        logger = logging.getLogger("web2py.app.cuentas")
        logger.info(f"Acceso a lista completa de cuentas por administrador {auth.user.id} ({auth.user.email})")
        
        # Obtener y sanitizar parámetros de búsqueda de forma simple
        buscar = str(request.vars.buscar or '').strip()[:100]  # Limitar longitud
        numero_cuenta = str(request.vars.numero_cuenta or '').strip()[:25]
        estado = str(request.vars.estado or 'todos').strip().lower()
        tipo = str(request.vars.tipo or 'todos').strip().lower()
        saldo_min = str(request.vars.saldo_min or '').strip()
        saldo_max = str(request.vars.saldo_max or '').strip()
        moneda_saldo = str(request.vars.moneda_saldo or 'VES').strip().upper()
        
        # Validar página
        try:
            page = int(request.vars.page or 1)
            if page < 1:
                page = 1
        except (ValueError, TypeError):
            page = 1
        
        # Validar estado y tipo (listas cerradas)
        if estado not in ['todos', 'activa', 'inactiva', 'bloqueada']:
            estado = 'todos'
        
        if tipo not in ['todos', 'corriente', 'ahorro']:
            tipo = 'todos'
        
        if moneda_saldo not in ['VES', 'USD', 'EUR', 'USDT']:
            moneda_saldo = 'VES'
        
        # Query base con JOIN explícito para obtener datos del cliente
        query = (db.cuentas.cliente_id == db.clientes.id) & \\
                (db.clientes.user_id == db.auth_user.id)
        
        # Aplicar filtros de búsqueda general
        if buscar:
            query &= ((db.cuentas.numero_cuenta.contains(buscar)) |
                     (db.clientes.cedula.contains(buscar)) |
                     (db.auth_user.first_name.contains(buscar)) |
                     (db.auth_user.last_name.contains(buscar)) |
                     (db.auth_user.email.contains(buscar)))
        
        # Filtro específico por número de cuenta
        if numero_cuenta:
            query &= (db.cuentas.numero_cuenta.contains(numero_cuenta))
        
        # Filtros por estado y tipo
        if estado != 'todos':
            query &= (db.cuentas.estado == estado)
        
        if tipo != 'todos':
            query &= (db.cuentas.tipo_cuenta == tipo)
        
        # Filtros por rango de saldos
        if saldo_min:
            try:
                saldo_min_val = float(saldo_min)
                if moneda_saldo == 'VES':
                    query &= (db.cuentas.saldo_ves >= saldo_min_val)
                elif moneda_saldo == 'USD':
                    query &= (db.cuentas.saldo_usd >= saldo_min_val)
                elif moneda_saldo == 'EUR':
                    query &= (db.cuentas.saldo_eur >= saldo_min_val)
                elif moneda_saldo == 'USDT':
                    query &= (db.cuentas.saldo_usdt >= saldo_min_val)
            except (ValueError, TypeError):
                pass  # Ignorar valores inválidos
        
        if saldo_max:
            try:
                saldo_max_val = float(saldo_max)
                if moneda_saldo == 'VES':
                    query &= (db.cuentas.saldo_ves <= saldo_max_val)
                elif moneda_saldo == 'USD':
                    query &= (db.cuentas.saldo_usd <= saldo_max_val)
                elif moneda_saldo == 'EUR':
                    query &= (db.cuentas.saldo_eur <= saldo_max_val)
                elif moneda_saldo == 'USDT':
                    query &= (db.cuentas.saldo_usdt <= saldo_max_val)
            except (ValueError, TypeError):
                pass  # Ignorar valores inválidos
        
        # Configurar paginación
        items_per_page = 25
        
        cuentas = db(query).select(
            db.cuentas.ALL,
            db.clientes.cedula,
            db.auth_user.first_name,
            db.auth_user.last_name,
            db.auth_user.email,
            orderby=~db.cuentas.fecha_creacion,
            limitby=((page-1)*items_per_page, page*items_per_page)
        )
        
        # Contar total para paginación
        total_cuentas = db(query).count()
        total_pages = (total_cuentas + items_per_page - 1) // items_per_page
        
        # Obtener estadísticas generales
        from gluon.storage import Storage
        stats = Storage(
            total=db(db.cuentas.id > 0).count(),
            activas=db(db.cuentas.estado == 'activa').count(),
            inactivas=db(db.cuentas.estado == 'inactiva').count(),
            corrientes=db(db.cuentas.tipo_cuenta == 'corriente').count(),
            ahorros=db(db.cuentas.tipo_cuenta == 'ahorro').count()
        )
        
        return dict(
            cuentas=cuentas,
            buscar=buscar,
            numero_cuenta=numero_cuenta,
            estado=estado,
            tipo=tipo,
            saldo_min=saldo_min,
            saldo_max=saldo_max,
            moneda_saldo=moneda_saldo,
            page=page,
            total_pages=total_pages,
            total_cuentas=total_cuentas,
            stats=stats
        )
        
    except Exception as e:
        # Log del error
        import logging
        logger = logging.getLogger("web2py.app.cuentas")
        logger.error(f"Error al obtener lista de cuentas: {str(e)}")
        
        # Mostrar mensaje de error al usuario
        response.flash = f"Error al cargar la lista de cuentas: {str(e)}"
        
        from gluon.storage import Storage
        return dict(
            cuentas=[],
            error_message="No se pudieron cargar los datos de cuentas.",
            buscar='',
            numero_cuenta='',
            estado='todos',
            tipo='todos',
            saldo_min='',
            saldo_max='',
            moneda_saldo='VES',
            page=1,
            total_pages=0,
            total_cuentas=0,
            stats=Storage(total=0, activas=0, inactivas=0, corrientes=0, ahorros=0)
        )
'''
    
    return funcion_corregida

def aplicar_correccion():
    """Aplica la corrección al controlador"""
    
    print("=== APLICANDO CORRECCIÓN AL CONTROLADOR ===")
    
    try:
        # Leer el controlador actual
        with open('controllers/cuentas.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar el inicio de la función listar_todas
        inicio_funcion = contenido.find('@auth.requires_membership(\'administrador\')\ndef listar_todas():')
        
        if inicio_funcion == -1:
            print("❌ No se encontró la función listar_todas")
            return False
        
        # Buscar el final de la función (siguiente función o final del archivo)
        # Buscar la siguiente función que empiece con @auth o def
        resto_contenido = contenido[inicio_funcion + 50:]  # Saltar el inicio de la función actual
        
        # Buscar patrones que indiquen el final de la función
        patrones_fin = [
            '\n@auth.',
            '\ndef ',
            '\n# ===',
            '\n\n\n'
        ]
        
        fin_funcion = len(contenido)  # Por defecto, hasta el final
        
        for patron in patrones_fin:
            pos = resto_contenido.find(patron)
            if pos != -1:
                fin_funcion = inicio_funcion + 50 + pos
                break
        
        # Crear el nuevo contenido
        funcion_corregida = crear_listar_todas_corregida()
        
        nuevo_contenido = (
            contenido[:inicio_funcion] + 
            funcion_corregida + 
            '\n\n' +
            contenido[fin_funcion:]
        )
        
        # Crear backup
        import shutil
        shutil.copy('controllers/cuentas.py', 'controllers/cuentas.py.backup')
        print("✓ Backup creado: controllers/cuentas.py.backup")
        
        # Escribir el nuevo contenido
        with open('controllers/cuentas.py', 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        
        print("✓ Función listar_todas corregida")
        print("✓ Controlador actualizado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al aplicar corrección: {str(e)}")
        return False

if __name__ == "__main__":
    print("CORRECCIÓN DE LA FUNCIÓN LISTAR_TODAS")
    print("=" * 50)
    
    # Mostrar la función corregida
    funcion = crear_listar_todas_corregida()
    print("Función corregida creada.")
    print("\nCaracterísticas de la corrección:")
    print("✓ Sanitización simple y segura")
    print("✓ Manejo robusto de errores")
    print("✓ Consultas optimizadas")
    print("✓ Sin dependencias complejas")
    
    # Preguntar si aplicar
    print(f"\n{'=' * 50}")
    print("¿Desea aplicar la corrección al controlador? (y/N)")
    
    # Para automatizar, aplicamos directamente
    resultado = aplicar_correccion()
    
    if resultado:
        print("\n✅ CORRECCIÓN APLICADA EXITOSAMENTE")
        print("📋 Reinicie el servidor web2py para que los cambios tomen efecto")
        print("📋 La página de Todas las Cuentas debería funcionar ahora")
    else:
        print("\n❌ ERROR AL APLICAR LA CORRECCIÓN")
        print("📋 Revisar los errores mostrados arriba")
    
    print("=" * 50)