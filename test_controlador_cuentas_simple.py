#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Prueba simple del controlador de cuentas
Debe ejecutarse desde web2py: python web2py.py -S divisas2os -M -R test_controlador_cuentas_simple.py
"""

def test_listar_todas_simple():
    """Prueba una versión simplificada de listar_todas"""
    
    print("=== PRUEBA SIMPLE DE LISTAR_TODAS ===")
    
    try:
        # Verificar permisos básicos (simular usuario admin)
        print("1. Verificando datos básicos...")
        
        total_cuentas = db(db.cuentas.id > 0).count()
        print(f"   Total cuentas en BD: {total_cuentas}")
        
        if total_cuentas == 0:
            print("❌ No hay cuentas para mostrar")
            return False
        
        # Consulta simple sin filtros
        print("2. Ejecutando consulta simple...")
        
        query = (db.cuentas.cliente_id == db.clientes.id) & \
                (db.clientes.user_id == db.auth_user.id)
        
        cuentas = db(query).select(
            db.cuentas.ALL,
            db.clientes.cedula,
            db.auth_user.first_name,
            db.auth_user.last_name,
            db.auth_user.email,
            orderby=~db.cuentas.fecha_creacion,
            limitby=(0, 10)
        )
        
        print(f"   Cuentas obtenidas: {len(cuentas)}")
        
        if len(cuentas) == 0:
            print("❌ La consulta no devuelve resultados")
            return False
        
        # Mostrar ejemplo de datos
        print("3. Ejemplo de datos obtenidos:")
        cuenta_ejemplo = cuentas[0]
        print(f"   - Número: {cuenta_ejemplo.cuentas.numero_cuenta}")
        print(f"   - Cliente: {cuenta_ejemplo.auth_user.first_name} {cuenta_ejemplo.auth_user.last_name}")
        print(f"   - Cédula: {cuenta_ejemplo.clientes.cedula}")
        print(f"   - Estado: {cuenta_ejemplo.cuentas.estado}")
        print(f"   - Saldo VES: {cuenta_ejemplo.cuentas.saldo_ves}")
        
        # Calcular estadísticas simples
        print("4. Calculando estadísticas...")
        
        stats = {
            'total': db(db.cuentas.id > 0).count(),
            'activas': db(db.cuentas.estado == 'activa').count(),
            'inactivas': db(db.cuentas.estado == 'inactiva').count(),
            'corrientes': db(db.cuentas.tipo_cuenta == 'corriente').count(),
            'ahorros': db(db.cuentas.tipo_cuenta == 'ahorro').count()
        }
        
        print(f"   Estadísticas: {stats}")
        
        # Simular el dict que devolvería el controlador
        resultado = {
            'cuentas': cuentas,
            'buscar': '',
            'numero_cuenta': '',
            'estado': 'todos',
            'tipo': 'todos',
            'saldo_min': '',
            'saldo_max': '',
            'moneda_saldo': 'VES',
            'page': 1,
            'total_pages': 1,
            'total_cuentas': len(cuentas),
            'stats': stats
        }
        
        print("5. Resultado final:")
        print(f"   - Cuentas: {len(resultado['cuentas'])}")
        print(f"   - Stats: {resultado['stats']}")
        
        print("✅ LA CONSULTA FUNCIONA CORRECTAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def crear_funcion_listar_todas_simple():
    """Crea una versión simplificada de la función listar_todas"""
    
    print("\n=== CREANDO FUNCIÓN SIMPLIFICADA ===")
    
    funcion_simple = '''
@auth.requires_membership('administrador')
def listar_todas_simple():
    """Versión simplificada de listar_todas para debugging"""
    try:
        # Parámetros básicos
        buscar = request.vars.buscar or ''
        estado = request.vars.estado or 'todos'
        tipo = request.vars.tipo or 'todos'
        page = int(request.vars.page or 1)
        
        # Query base
        query = (db.cuentas.cliente_id == db.clientes.id) & \\
                (db.clientes.user_id == db.auth_user.id)
        
        # Aplicar filtros básicos
        if buscar:
            query &= ((db.cuentas.numero_cuenta.contains(buscar)) |
                     (db.clientes.cedula.contains(buscar)) |
                     (db.auth_user.first_name.contains(buscar)) |
                     (db.auth_user.last_name.contains(buscar)))
        
        if estado != 'todos':
            query &= (db.cuentas.estado == estado)
        
        if tipo != 'todos':
            query &= (db.cuentas.tipo_cuenta == tipo)
        
        # Obtener cuentas
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
        
        # Contar total
        total_cuentas = db(query).count()
        total_pages = (total_cuentas + items_per_page - 1) // items_per_page
        
        # Estadísticas
        stats = {
            'total': db(db.cuentas.id > 0).count(),
            'activas': db(db.cuentas.estado == 'activa').count(),
            'inactivas': db(db.cuentas.estado == 'inactiva').count(),
            'corrientes': db(db.cuentas.tipo_cuenta == 'corriente').count(),
            'ahorros': db(db.cuentas.tipo_cuenta == 'ahorro').count()
        }
        
        return dict(
            cuentas=cuentas,
            buscar=buscar,
            numero_cuenta='',
            estado=estado,
            tipo=tipo,
            saldo_min='',
            saldo_max='',
            moneda_saldo='VES',
            page=page,
            total_pages=total_pages,
            total_cuentas=total_cuentas,
            stats=stats
        )
        
    except Exception as e:
        response.flash = f"Error al cargar cuentas: {str(e)}"
        return dict(
            cuentas=[],
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
            stats={'total': 0, 'activas': 0, 'inactivas': 0, 'corrientes': 0, 'ahorros': 0}
        )
'''
    
    print("Función simplificada creada. Para usarla:")
    print("1. Agregar esta función al controlador cuentas.py")
    print("2. Acceder a /cuentas/listar_todas_simple")
    print("3. Si funciona, el problema está en la función original")
    
    # Guardar la función en un archivo
    with open('listar_todas_simple.py', 'w', encoding='utf-8') as f:
        f.write(funcion_simple)
    
    print("✓ Función guardada en listar_todas_simple.py")

if __name__ == "__main__":
    print("PRUEBA SIMPLE DEL CONTROLADOR DE CUENTAS")
    print("=" * 50)
    
    resultado = test_listar_todas_simple()
    
    if resultado:
        print("\n✅ LA CONSULTA FUNCIONA - El problema puede estar en:")
        print("   1. La función de validación de parámetros")
        print("   2. Los permisos de usuario")
        print("   3. Un error en el controlador original")
    else:
        print("\n❌ HAY UN PROBLEMA CON LOS DATOS O LA CONSULTA")
    
    crear_funcion_listar_todas_simple()
    
    print("=" * 50)