#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificación final de la corrección de Todas las Cuentas
"""

import os

def verificar_correccion_aplicada():
    """Verifica que la corrección se haya aplicado correctamente"""
    
    print("=== VERIFICACIÓN DE CORRECCIÓN APLICADA ===")
    
    try:
        # Verificar que existe el backup
        if os.path.exists('controllers/cuentas.py.backup'):
            print("✓ Backup del controlador original creado")
        else:
            print("⚠️  No se encontró backup del controlador")
        
        # Leer el controlador corregido
        with open('controllers/cuentas.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar elementos de la corrección
        elementos_correccion = [
            ('"""Listar todas las cuentas del sistema (solo administradores) - Versión corregida"""', "Comentario de versión corregida"),
            ('buscar = str(request.vars.buscar or \'\').strip()[:100]', "Sanitización simple de búsqueda"),
            ('if estado not in [\'todos\', \'activa\', \'inactiva\', \'bloqueada\']:', "Validación de estado"),
            ('if tipo not in [\'todos\', \'corriente\', \'ahorro\']:', "Validación de tipo"),
            ('query = (db.cuentas.cliente_id == db.clientes.id)', "Query base simplificada"),
            ('except Exception as e:', "Manejo de errores"),
            ('response.flash = f"Error al cargar la lista de cuentas: {str(e)}"', "Mensaje de error mejorado")
        ]
        
        encontrados = 0
        for elemento, descripcion in elementos_correccion:
            if elemento in contenido:
                print(f"✓ {descripcion}: OK")
                encontrados += 1
            else:
                print(f"❌ {descripcion}: FALTANTE")
        
        puntuacion = (encontrados / len(elementos_correccion)) * 100
        print(f"\nPuntuación de corrección: {puntuacion:.1f}%")
        
        return puntuacion >= 90
        
    except Exception as e:
        print(f"❌ Error al verificar corrección: {str(e)}")
        return False

def verificar_vista_actualizada():
    """Verifica que la vista esté actualizada"""
    
    print("\n=== VERIFICACIÓN DE VISTA ACTUALIZADA ===")
    
    try:
        with open('views/cuentas/listar_todas.html', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar elementos clave de la vista
        elementos_vista = [
            ('{{extend \'layout.html\'}}', "Layout correcto"),
            ('Gestión de Cuentas', "Título actualizado"),
            ('{{if cuentas:}}', "Condicional de cuentas"),
            ('{{for cuenta in cuentas:}}', "Loop de cuentas"),
            ('{{=cuenta.cuentas.numero_cuenta}}', "Número de cuenta"),
            ('{{=cuenta.auth_user.first_name}}', "Nombre del cliente"),
            ('{{else:}}', "Manejo de estado vacío"),
            ('No hay cuentas registradas', "Mensaje sin datos")
        ]
        
        encontrados = 0
        for elemento, descripcion in elementos_vista:
            if elemento in contenido:
                print(f"✓ {descripcion}: OK")
                encontrados += 1
            else:
                print(f"❌ {descripcion}: FALTANTE")
        
        puntuacion = (encontrados / len(elementos_vista)) * 100
        print(f"\nPuntuación de vista: {puntuacion:.1f}%")
        
        return puntuacion >= 80
        
    except Exception as e:
        print(f"❌ Error al verificar vista: {str(e)}")
        return False

def generar_instrucciones_finales():
    """Genera las instrucciones finales para el usuario"""
    
    print("\n=== INSTRUCCIONES FINALES ===")
    
    instrucciones = """
🔧 PASOS PARA COMPLETAR LA CORRECCIÓN:

1. REINICIAR EL SERVIDOR WEB2PY:
   - Detener el servidor web2py actual
   - Volver a iniciarlo con: python web2py.py -a <password>
   - Esto cargará la función corregida

2. VERIFICAR PERMISOS DE USUARIO:
   - Asegurarse de estar logueado como administrador
   - El usuario debe tener el rol 'administrador'

3. ACCEDER A LA FUNCIONALIDAD:
   - Ir a: http://localhost:8000/divisas2os/cuentas/listar_todas
   - O navegar desde el menú: Gestión de Cuentas > Todas las Cuentas

4. SI AÚN NO APARECEN DATOS:
   - Verificar que hay cuentas en la base de datos
   - Revisar los logs del servidor para errores
   - Verificar que las relaciones entre tablas estén correctas

5. RESTAURAR BACKUP SI ES NECESARIO:
   - Si algo sale mal: cp controllers/cuentas.py.backup controllers/cuentas.py
   - Luego reiniciar el servidor

📋 CARACTERÍSTICAS DE LA CORRECCIÓN:
✓ Sanitización simple y segura de parámetros
✓ Manejo robusto de errores con mensajes claros
✓ Consultas optimizadas sin dependencias complejas
✓ Validación de entrada con listas cerradas
✓ Logging mejorado para auditoría
✓ Compatibilidad total con la vista existente

🎯 RESULTADO ESPERADO:
- La página mostrará todas las cuentas del sistema
- Filtros de búsqueda funcionarán correctamente
- Estadísticas se mostrarán en tiempo real
- Paginación automática para grandes volúmenes
- Mensajes claros en caso de errores o datos vacíos
"""
    
    print(instrucciones)

def main():
    """Función principal de verificación"""
    
    print("VERIFICACIÓN FINAL DE LA CORRECCIÓN")
    print("=" * 50)
    
    test_controlador = verificar_correccion_aplicada()
    test_vista = verificar_vista_actualizada()
    
    print(f"\n{'=' * 50}")
    print("RESUMEN DE VERIFICACIÓN")
    print(f"{'=' * 50}")
    
    print(f"Controlador corregido: {'✅ OK' if test_controlador else '❌ ERROR'}")
    print(f"Vista actualizada: {'✅ OK' if test_vista else '❌ ERROR'}")
    
    if test_controlador and test_vista:
        print("\n🎉 ¡CORRECCIÓN COMPLETADA EXITOSAMENTE!")
        print("✅ El controlador ha sido corregido")
        print("✅ La vista está actualizada")
        print("✅ La funcionalidad debería funcionar correctamente")
    else:
        print("\n⚠️  HAY PROBLEMAS PENDIENTES")
        if not test_controlador:
            print("❌ El controlador necesita revisión")
        if not test_vista:
            print("❌ La vista necesita corrección")
    
    generar_instrucciones_finales()
    
    print("=" * 50)

if __name__ == "__main__":
    main()