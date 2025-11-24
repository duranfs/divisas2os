#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

print("=" * 80)
print("TEST: Historial de Movimientos")
print("=" * 80)

try:
    # Verificar que la tabla existe
    print("\n1. Verificando tabla movimientos_remesas...")
    count = db(db.movimientos_remesas).count()
    print("   Total de registros: %d" % count)
    
    # Probar la query básica
    print("\n2. Probando query básica...")
    query = (db.movimientos_remesas.id > 0)
    movimientos = db(query).select(
        db.movimientos_remesas.ALL,
        orderby=~db.movimientos_remesas.fecha,
        limitby=(0, 100)
    )
    print("   Movimientos encontrados: %d" % len(movimientos))
    
    # Mostrar algunos movimientos
    print("\n3. Primeros movimientos:")
    for i, mov in enumerate(movimientos[:5]):
        print("   %d. ID: %s, Fecha: %s, Tipo: %s" % (i+1, mov.id, mov.fecha, mov.tipo))
        print("      USD: %s, USDT: %s" % (mov.monto_usd, mov.monto_usdt))
        print("      Descripcion: %s" % mov.descripcion)
    
    # Probar con filtros de fecha
    print("\n4. Probando con filtros de fecha...")
    fecha_desde = datetime.date.today() - datetime.timedelta(days=30)
    fecha_hasta = datetime.date.today()
    
    query_fecha = (db.movimientos_remesas.id > 0)
    query_fecha &= (db.movimientos_remesas.fecha >= fecha_desde)
    fecha_hasta_fin = datetime.datetime.combine(fecha_hasta, datetime.time(23, 59, 59))
    query_fecha &= (db.movimientos_remesas.fecha <= fecha_hasta_fin)
    
    movimientos_filtrados = db(query_fecha).select(
        db.movimientos_remesas.ALL,
        orderby=~db.movimientos_remesas.fecha,
        limitby=(0, 100)
    )
    print("   Movimientos con filtro de fecha: %d" % len(movimientos_filtrados))
    
    print("\n" + "=" * 80)
    print("TEST COMPLETADO EXITOSAMENTE")
    print("=" * 80)
    
except Exception as e:
    print("\n" + "=" * 80)
    print("ERROR ENCONTRADO:")
    print("=" * 80)
    print(str(e))
    import traceback
    traceback.print_exc()
