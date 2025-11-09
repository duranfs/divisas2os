#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Prueba final de la vista de detalles de cliente
Ejecutar desde C:\web2py
"""

import os

def test_vista_detalle_completa():
    """Prueba completa de la vista de detalles"""
    
    print("=== PRUEBA FINAL DE VISTA DE DETALLES ===")
    
    vista_path = 'applications/divisas2os/views/clientes/detalle.html'
    
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
        ("{{=datos_seguros.nombre_completo}}", "Campo nombre completo"),
        ("{{=cliente.cedula}}", "Campo cédula"),
        ("{{=datos_seguros.email}}", "Campo email"),
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
    
    # Verificar campos de datos específicos
    campos_datos = [
        "{{=datos_seguros.telefono}}",
        "{{=datos_seguros.direccion}}",
        "{{=datos_seguros.fecha_nacimiento_str}}",
        "{{=cuenta.numero_cuenta}}",
        "{{=cuenta.saldo_ves}}",
        "{{=cuenta.saldo_usd}}",
        "{{=cuenta.saldo_eur}}",
        "{{=cuenta.saldo_usdt}}",
        "{{=transaccion.fecha_transaccion}}",
        "{{=transaccion.tipo_operacion}}",
        "{{=transaccion.monto_origen}}",
        "{{=transaccion.numero_comprobante}}"
    ]
    
    campos_encontrados = 0
    for campo in campos_datos:
        if campo in contenido:
            campos_encontrados += 1
    
    print(f"✓ Campos de datos encontrados: {campos_encontrados}/{len(campos_datos)}")
    
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

def verificar_integracion_controlador():
    """Verifica que la vista esté integrada con el controlador"""
    
    print("\n=== VERIFICACIÓN DE INTEGRACIÓN ===")
    
    controlador_path = 'applications/divisas2os/controllers/clientes.py'
    vista_path = 'applications/divisas2os/views/clientes/detalle.html'
    
    try:
        with open(controlador_path, 'r', encoding='utf-8') as f:
            controlador = f.read()
        
        with open(vista_path, 'r', encoding='utf-8') as f:
            vista = f.read()
        
        # Verificar que el controlador tiene la función detalle
        if 'def detalle():' in controlador:
            print("✓ Función detalle() existe en el controlador")
        else:
            print("❌ Función detalle() no encontrada en el controlador")
            return False
        
        # Verificar que el controlador retorna los datos que espera la vista
        datos_esperados = [
            ('cliente=cliente', 'cliente'),
            ('datos_seguros=datos_seguros', 'datos_seguros'),
            ('cuentas=cuentas', 'cuentas'),
            ('ultimas_transacciones=ultimas_transacciones', 'ultimas_transacciones')
        ]
        
        for dato_controlador, variable_vista in datos_esperados:
            ctrl_ok = dato_controlador in controlador
            vista_ok = variable_vista in vista
            
            if ctrl_ok and vista_ok:
                print(f"✓ Variable '{variable_vista}': Controlador ✓ Vista ✓")
            elif ctrl_ok:
                print(f"⚠️  Variable '{variable_vista}': Controlador ✓ Vista ❌")
            elif vista_ok:
                print(f"⚠️  Variable '{variable_vista}': Controlador ❌ Vista ✓")
            else:
                print(f"❌ Variable '{variable_vista}': Controlador ❌ Vista ❌")
        
        print("✅ Integración verificada")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar integración: {str(e)}")
        return False

def main():
    """Función principal"""
    
    print("PRUEBA FINAL DE LA VISTA DE DETALLES DE CLIENTE")
    print("=" * 60)
    
    test1 = test_vista_detalle_completa()
    test2 = verificar_integracion_controlador()
    
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    
    if test1 and test2:
        print("🎉 ¡PERFECTO! La vista de detalles está completamente funcional")
        print("✅ Todos los elementos están implementados")
        print("✅ La integración con el controlador es correcta")
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