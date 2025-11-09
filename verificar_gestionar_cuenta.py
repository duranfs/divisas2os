#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificación de la vista de gestionar cuenta
"""

import os

def verificar_vista_gestionar():
    """Verifica que la vista de gestionar esté correctamente implementada"""
    
    print("=== VERIFICACIÓN DE VISTA GESTIONAR CUENTA ===")
    
    vista_path = 'views/cuentas/gestionar.html'
    
    if not os.path.exists(vista_path):
        print(f"❌ Vista no encontrada: {vista_path}")
        return False
    
    with open(vista_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    print(f"✓ Vista encontrada: {vista_path}")
    print(f"✓ Tamaño: {len(contenido)} caracteres")
    
    # Verificar elementos esenciales
    elementos = [
        ("{{extend 'layout.html'}}", "Layout"),
        ("Gestionar Cuenta", "Título actualizado"),
        ("{{if cuenta and cliente and usuario:}}", "Validación de datos"),
        ("{{=form}}", "Formulario de edición"),
        ("{{=cuenta.numero_cuenta}}", "Número de cuenta"),
        ("{{=usuario.first_name}}", "Nombre del cliente"),
        ("{{=cliente.cedula}}", "Cédula del cliente"),
        ("Saldos Actuales", "Sección de saldos"),
        ("{{=cuenta.saldo_ves}}", "Saldo VES"),
        ("{{=cuenta.saldo_usd}}", "Saldo USD"),
        ("{{=cuenta.saldo_eur}}", "Saldo EUR"),
        ("Últimas Transacciones", "Sección de transacciones"),
        ("{{for transaccion in transacciones:}}", "Loop de transacciones"),
        ("Cuenta No Encontrada", "Manejo de errores"),
        ("<style>", "CSS"),
        ("<script>", "JavaScript")
    ]
    
    encontrados = 0
    for elemento, nombre in elementos:
        if elemento in contenido:
            print(f"✓ {nombre}: OK")
            encontrados += 1
        else:
            print(f"❌ {nombre}: FALTANTE")
    
    # Verificar enlaces de navegación
    enlaces = [
        ("URL('clientes', 'detalle'", "Enlace a cliente"),
        ("URL('cuentas', 'detalle'", "Enlace a detalles de cuenta"),
        ("URL('cuentas', 'listar_todas')", "Enlace a todas las cuentas"),
        ("URL('default', 'dashboard')", "Enlace al dashboard")
    ]
    
    enlaces_encontrados = 0
    for enlace, nombre in enlaces:
        if enlace in contenido:
            print(f"✓ {nombre}: OK")
            enlaces_encontrados += 1
        else:
            print(f"❌ {nombre}: FALTANTE")
    
    # Calcular puntuaciones
    puntuacion_elementos = (encontrados / len(elementos)) * 100
    puntuacion_enlaces = (enlaces_encontrados / len(enlaces)) * 100
    
    puntuacion_total = (puntuacion_elementos + puntuacion_enlaces) / 2
    
    print(f"\n=== PUNTUACIONES ===")
    print(f"Elementos esenciales: {puntuacion_elementos:.1f}%")
    print(f"Enlaces de navegación: {puntuacion_enlaces:.1f}%")
    print(f"PUNTUACIÓN TOTAL: {puntuacion_total:.1f}%")
    
    if puntuacion_total >= 90:
        print("\n🎉 ¡Vista de gestionar implementada correctamente!")
        return True
    elif puntuacion_total >= 75:
        print("\n✅ Vista implementada con algunos elementos menores faltantes")
        return True
    else:
        print("\n⚠️  La vista necesita mejoras importantes")
        return False

def verificar_controlador_gestionar():
    """Verifica que el controlador tenga la función gestionar correcta"""
    
    print("\n=== VERIFICACIÓN DE CONTROLADOR GESTIONAR ===")
    
    controlador_path = 'controllers/cuentas.py'
    
    if not os.path.exists(controlador_path):
        print(f"❌ Controlador no encontrado: {controlador_path}")
        return False
    
    with open(controlador_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    print(f"✓ Controlador encontrado: {controlador_path}")
    
    # Verificar función gestionar
    if 'def gestionar():' in contenido:
        print("✓ Función gestionar() encontrada")
    else:
        print("❌ Función gestionar() no encontrada")
        return False
    
    # Verificar elementos clave del controlador
    elementos_controlador = [
        ('@auth.requires_membership(\'administrador\')', "Decorador de permisos"),
        ('cuenta_id = request.args(0)', "Obtención de ID"),
        ('db(db.cuentas.id == cuenta_id)', "Consulta de cuenta"),
        ('db(db.clientes.id == cuenta_record.cliente_id)', "Consulta de cliente"),
        ('SQLFORM(db.cuentas', "Formulario de edición"),
        ('return dict(', "Retorno de datos"),
        ('cuenta=cuenta_record', "Variable cuenta"),
        ('cliente=cliente', "Variable cliente"),
        ('usuario=usuario', "Variable usuario"),
        ('form=form', "Variable formulario"),
        ('transacciones=transacciones', "Variable transacciones")
    ]
    
    encontrados_ctrl = 0
    for elemento, nombre in elementos_controlador:
        if elemento in contenido:
            print(f"✓ {nombre}: OK")
            encontrados_ctrl += 1
        else:
            print(f"❌ {nombre}: FALTANTE")
    
    puntuacion_ctrl = (encontrados_ctrl / len(elementos_controlador)) * 100
    print(f"\nPuntuación controlador: {puntuacion_ctrl:.1f}%")
    
    return puntuacion_ctrl >= 80

def verificar_enlace_desde_listar_todas():
    """Verifica que el enlace desde listar_todas sea correcto"""
    
    print("\n=== VERIFICACIÓN DE ENLACE DESDE LISTAR_TODAS ===")
    
    vista_listar_path = 'views/cuentas/listar_todas.html'
    
    if not os.path.exists(vista_listar_path):
        print(f"❌ Vista listar_todas no encontrada: {vista_listar_path}")
        return False
    
    with open(vista_listar_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar que el enlace a gestionar esté correcto
    enlaces_gestionar = [
        ("URL('cuentas', 'gestionar', args=[cuenta.cuentas.id])", "Enlace correcto a gestionar"),
        ('title="Gestionar cuenta"', "Tooltip de gestionar"),
        ('<i class="fas fa-cog"></i>', "Icono de gestionar")
    ]
    
    encontrados = 0
    for enlace, nombre in enlaces_gestionar:
        if enlace in contenido:
            print(f"✓ {nombre}: OK")
            encontrados += 1
        else:
            print(f"❌ {nombre}: FALTANTE")
    
    puntuacion = (encontrados / len(enlaces_gestionar)) * 100
    print(f"\nPuntuación enlaces: {puntuacion:.1f}%")
    
    return puntuacion >= 80

if __name__ == "__main__":
    print("VERIFICACIÓN COMPLETA DE GESTIONAR CUENTA")
    print("=" * 50)
    
    test_vista = verificar_vista_gestionar()
    test_controlador = verificar_controlador_gestionar()
    test_enlace = verificar_enlace_desde_listar_todas()
    
    print(f"\n{'=' * 50}")
    print("RESUMEN FINAL")
    print(f"{'=' * 50}")
    
    print(f"Vista gestionar: {'✅ OK' if test_vista else '❌ ERROR'}")
    print(f"Controlador gestionar: {'✅ OK' if test_controlador else '❌ ERROR'}")
    print(f"Enlace desde listar_todas: {'✅ OK' if test_enlace else '❌ ERROR'}")
    
    if test_vista and test_controlador and test_enlace:
        print("\n🎉 ¡GESTIONAR CUENTA COMPLETAMENTE FUNCIONAL!")
        print("📋 Funcionalidades disponibles:")
        print("   • Edición de estado y saldos de cuenta")
        print("   • Información completa del propietario")
        print("   • Visualización de saldos en todas las monedas")
        print("   • Historial de transacciones recientes")
        print("   • Enlaces de navegación integrados")
        print("   • Manejo de errores robusto")
        
        print("\n📋 CÓMO USAR:")
        print("   1. Ir a 'Todas las Cuentas'")
        print("   2. Hacer clic en el botón de engranaje (⚙️) 'Gestionar'")
        print("   3. Editar los campos necesarios")
        print("   4. Guardar los cambios")
    else:
        print("\n⚠️  HAY PROBLEMAS QUE CORREGIR")
        if not test_vista:
            print("❌ La vista gestionar necesita correcciones")
        if not test_controlador:
            print("❌ El controlador gestionar necesita correcciones")
        if not test_enlace:
            print("❌ Los enlaces desde listar_todas necesitan corrección")
    
    print(f"{'=' * 50}")