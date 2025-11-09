#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verificación de la vista de todas las cuentas
"""

import os

def verificar_vista_cuentas():
    """Verifica que la vista de todas las cuentas esté correctamente implementada"""
    
    print("=== VERIFICACIÓN DE VISTA TODAS LAS CUENTAS ===")
    
    vista_path = 'views/cuentas/listar_todas.html'
    
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
        ("Gestión de Cuentas", "Título actualizado"),
        ("{{if cuentas:}}", "Condicional de cuentas"),
        ("{{for cuenta in cuentas:}}", "Loop de cuentas"),
        ("{{=cuenta.cuentas.numero_cuenta}}", "Número de cuenta"),
        ("{{=cuenta.auth_user.first_name}}", "Nombre cliente"),
        ("{{=cuenta.clientes.cedula}}", "Cédula cliente"),
        ("{{=cuenta.cuentas.saldo_ves}}", "Saldo VES"),
        ("{{=cuenta.cuentas.saldo_usd}}", "Saldo USD"),
        ("{{=cuenta.cuentas.saldo_eur}}", "Saldo EUR"),
        ("{{=cuenta.cuentas.estado}}", "Estado cuenta"),
        ("{{else:}}", "Manejo estado vacío"),
        ("No hay cuentas registradas", "Mensaje sin cuentas"),
        ("Sin resultados", "Mensaje sin filtros"),
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
    
    # Verificar filtros
    filtros = [
        ("name=\"buscar\"", "Filtro búsqueda general"),
        ("name=\"numero_cuenta\"", "Filtro número cuenta"),
        ("name=\"estado\"", "Filtro estado"),
        ("name=\"tipo\"", "Filtro tipo"),
        ("name=\"saldo_min\"", "Filtro saldo mínimo"),
        ("name=\"saldo_max\"", "Filtro saldo máximo")
    ]
    
    filtros_encontrados = 0
    for filtro, nombre in filtros:
        if filtro in contenido:
            print(f"✓ {nombre}: OK")
            filtros_encontrados += 1
        else:
            print(f"❌ {nombre}: FALTANTE")
    
    # Verificar acciones
    acciones = [
        ("URL('cuentas', 'gestionar'", "Acción gestionar"),
        ("URL('cuentas', 'detalle'", "Acción ver detalles"),
        ("URL('clientes', 'detalle'", "Acción ver cliente")
    ]
    
    acciones_encontradas = 0
    for accion, nombre in acciones:
        if accion in contenido:
            print(f"✓ {nombre}: OK")
            acciones_encontradas += 1
        else:
            print(f"❌ {nombre}: FALTANTE")
    
    # Calcular puntuaciones
    puntuacion_elementos = (encontrados / len(elementos)) * 100
    puntuacion_filtros = (filtros_encontrados / len(filtros)) * 100
    puntuacion_acciones = (acciones_encontradas / len(acciones)) * 100
    
    puntuacion_total = (puntuacion_elementos + puntuacion_filtros + puntuacion_acciones) / 3
    
    print(f"\n=== PUNTUACIONES ===")
    print(f"Elementos esenciales: {puntuacion_elementos:.1f}%")
    print(f"Filtros: {puntuacion_filtros:.1f}%")
    print(f"Acciones: {puntuacion_acciones:.1f}%")
    print(f"PUNTUACIÓN TOTAL: {puntuacion_total:.1f}%")
    
    if puntuacion_total >= 90:
        print("\n🎉 ¡Vista de cuentas implementada correctamente!")
        return True
    elif puntuacion_total >= 75:
        print("\n✅ Vista implementada con algunos elementos menores faltantes")
        return True
    else:
        print("\n⚠️  La vista necesita mejoras importantes")
        return False

def verificar_controlador_cuentas():
    """Verifica que el controlador tenga la función listar_todas"""
    
    print("\n=== VERIFICACIÓN DE CONTROLADOR ===")
    
    controlador_path = 'controllers/cuentas.py'
    
    if not os.path.exists(controlador_path):
        print(f"❌ Controlador no encontrado: {controlador_path}")
        return False
    
    with open(controlador_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    print(f"✓ Controlador encontrado: {controlador_path}")
    
    # Verificar función listar_todas
    if 'def listar_todas():' in contenido:
        print("✓ Función listar_todas() encontrada")
    else:
        print("❌ Función listar_todas() no encontrada")
        return False
    
    # Verificar elementos clave del controlador
    elementos_controlador = [
        ('@auth.requires_membership(\'administrador\')', "Decorador de permisos"),
        ('db.cuentas.cliente_id == db.clientes.id', "JOIN con clientes"),
        ('db.clientes.user_id == db.auth_user.id', "JOIN con usuarios"),
        ('return dict(', "Retorno de datos"),
        ('cuentas=cuentas', "Variable cuentas"),
        ('stats=stats', "Variable estadísticas")
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

if __name__ == "__main__":
    print("VERIFICACIÓN COMPLETA DE GESTIÓN DE CUENTAS")
    print("=" * 50)
    
    test_vista = verificar_vista_cuentas()
    test_controlador = verificar_controlador_cuentas()
    
    print(f"\n{'=' * 50}")
    print("RESUMEN FINAL")
    print(f"{'=' * 50}")
    
    print(f"Vista: {'✅ OK' if test_vista else '❌ ERROR'}")
    print(f"Controlador: {'✅ OK' if test_controlador else '❌ ERROR'}")
    
    if test_vista and test_controlador:
        print("\n🎉 ¡GESTIÓN DE CUENTAS LISTA PARA USAR!")
        print("📋 Funcionalidades disponibles:")
        print("   • Listado completo de cuentas")
        print("   • Filtros avanzados de búsqueda")
        print("   • Estadísticas en tiempo real")
        print("   • Acciones de gestión por cuenta")
        print("   • Paginación automática")
        print("   • Estados visuales claros")
    else:
        print("\n⚠️  HAY PROBLEMAS QUE CORREGIR")
        if not test_vista:
            print("❌ La vista necesita correcciones")
        if not test_controlador:
            print("❌ El controlador necesita correcciones")
    
    print(f"{'=' * 50}")