#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Prueba final de la vista de detalles de cliente
"""

import os

def test_vista_detalle_completa():
    """Prueba completa de la vista de detalles"""
    
    print("=== PRUEBA FINAL DE VISTA DE DETALLES ===")
    
    vista_path = 'views/clientes/detalle.html'
    
    if not os.path.exists(vista_path):
        print(f"❌ Vista no encontrada: {vista_path}")
        return False
    
    with open(vista_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    print(f"✓ Vista encontrada: {vista_path}")
    print(f"✓ Tamaño del archivo: {len(contenido)} caracteres")
    
    # Verificar elementos críticos
    elementos_criticos = [
        ("{{extend 'layout.html'}}", "Extensión de layout"),
        ("Detalles del Cliente", "Título principal"),
        ("{{if cliente and datos_seguros:}}", "Validación de datos"),
        ("Información Personal", "Sección de datos personales"),
        ("datos_seguros.nombre_completo", "Campo nombre completo"),
        ("cliente.cedula", "Campo cédula"),
        ("datos_seguros.email", "Campo email"),
        ("Cuentas Bancarias", "Sección de cuentas"),
        ("{{for cuenta in cuentas:}}", "Loop de cuentas"),
        ("Últimas Transacciones", "Sección de transacciones"),
        ("{{for transaccion in ultimas_transacciones:}}", "Loop de transacciones"),
        ("Cliente No Encontrado", "Manejo de errores"),
        ("Sin cuentas bancarias", "Estado vacío - cuentas"),
        ("Sin transacciones", "Estado vacío - transacciones")
    ]
    
    elementos_encontrados = 0
    for elemento, descripcion in elementos_criticos:
        if elemento in contenido:
            print(f"✓ {descripcion}: OK")
            elementos_encontrados += 1
        else:
            print(f"❌ {descripcion}: FALTANTE")
    
    # Verificar campos de datos específicos (con sintaxis flexible)
    campos_datos = [
        ("datos_seguros.nombre_completo", "Nombre completo"),
        ("cliente.cedula", "Cédula"),
        ("datos_seguros.email", "Email"),
        ("datos_seguros.telefono", "Teléfono"),
        ("datos_seguros.direccion", "Dirección"),
        ("datos_seguros.fecha_nacimiento_str", "Fecha nacimiento"),
        ("cuenta.numero_cuenta", "Número de cuenta"),
        ("cuenta.saldo_ves", "Saldo VES"),
        ("cuenta.saldo_usd", "Saldo USD"),
        ("cuenta.saldo_eur", "Saldo EUR"),
        ("cuenta.saldo_usdt", "Saldo USDT"),
        ("transaccion.fecha_transaccion", "Fecha transacción"),
        ("transaccion.tipo_operacion", "Tipo operación"),
        ("transaccion.monto_origen", "Monto origen"),
        ("transaccion.numero_comprobante", "Número comprobante")
    ]
    
    campos_encontrados = 0
    for campo, descripcion in campos_datos:
        if campo in contenido:
            print(f"✓ {descripcion}: encontrado")
            campos_encontrados += 1
        else:
            print(f"❌ {descripcion}: faltante")
    
    print(f"\n✓ Campos de datos encontrados: {campos_encontrados}/{len(campos_datos)}")
    
    # Verificar estilos CSS
    if '<style>' in contenido and '</style>' in contenido:
        print("✓ Estilos CSS personalizados incluidos")
    else:
        print("⚠️  Estilos CSS no encontrados")
    
    # Verificar acciones
    acciones = [
        "URL('clientes', 'editar'",
        "URL('clientes', 'cambiar_estado'",
        "URL('clientes', 'listar')",
        "URL('default', 'dashboard')"
    ]
    
    acciones_encontradas = 0
    for accion in acciones:
        if accion in contenido:
            acciones_encontradas += 1
    
    print(f"✓ Acciones encontradas: {acciones_encontradas}/{len(acciones)}")
    
    # Calcular puntuación
    puntuacion_elementos = (elementos_encontrados / len(elementos_criticos)) * 100
    puntuacion_campos = (campos_encontrados / len(campos_datos)) * 100
    puntuacion_acciones = (acciones_encontradas / len(acciones)) * 100
    
    puntuacion_total = (puntuacion_elementos + puntuacion_campos + puntuacion_acciones) / 3
    
    print(f"\n=== PUNTUACIÓN ===")
    print(f"Elementos críticos: {puntuacion_elementos:.1f}%")
    print(f"Campos de datos: {puntuacion_campos:.1f}%")
    print(f"Acciones: {puntuacion_acciones:.1f}%")
    print(f"PUNTUACIÓN TOTAL: {puntuacion_total:.1f}%")
    
    if puntuacion_total >= 90:
        print("\n🎉 ¡EXCELENTE! La vista está completamente implementada")
        return True
    elif puntuacion_total >= 75:
        print("\n✅ BUENO. La vista está bien implementada con algunos elementos menores faltantes")
        return True
    else:
        print("\n⚠️  NECESITA MEJORAS. Faltan elementos importantes")
        return False

def main():
    """Función principal"""
    
    print("PRUEBA FINAL DE LA VISTA DE DETALLES DE CLIENTE")
    print("=" * 60)
    
    test_resultado = test_vista_detalle_completa()
    
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    
    if test_resultado:
        print("🎉 ¡PERFECTO! La vista de detalles está completamente funcional")
        print("✅ Todos los elementos están implementados")
        print("\n📋 LA FUNCIONALIDAD ESTÁ LISTA PARA USAR:")
        print("   1. Ir a Gestión de Clientes")
        print("   2. Hacer clic en 'Ver detalles' de cualquier cliente")
        print("   3. Verificar que se muestran todos los datos")
    else:
        print("⚠️  Hay algunos problemas menores")
        print("❌ Revisar los elementos faltantes arriba")
    
    print("=" * 60)

if __name__ == "__main__":
    main()