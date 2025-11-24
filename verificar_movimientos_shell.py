#!/usr/bin/env python
# -*- coding: utf-8 -*-

print("=" * 80)
print("DIAGNÓSTICO DE MOVIMIENTOS DE REMESAS")
print("=" * 80)

# 1. Verificar remesas
print("\n1. REMESAS EN LA BASE DE DATOS:")
remesas = db(db.remesas).select(orderby=~db.remesas.id)
print("   Total de remesas: %d" % len(remesas))
for r in remesas:
    print("   - ID: %s, Fecha: %s, USD: %s, USDT: %s, Activa: %s" % (r.id, r.fecha, r.monto_usd, r.monto_usdt, r.activa))

# 2. Verificar movimientos
print("\n2. MOVIMIENTOS DE REMESAS EN LA BASE DE DATOS:")
movimientos = db(db.movimientos_remesas).select(orderby=~db.movimientos_remesas.id)
print("   Total de movimientos: %d" % len(movimientos))
for m in movimientos:
    print("   - ID: %s, Remesa: %s, Fecha: %s, Tipo: %s" % (m.id, m.remesa_id, m.fecha, m.tipo))
    print("     Monto USD: %s, Monto USDT: %s" % (m.monto_usd, m.monto_usdt))
    print("     Descripcion: %s" % m.descripcion)

# 3. Verificar la consulta que usa el controlador
print("\n3. SIMULANDO LA CONSULTA DEL CONTROLADOR:")
query = (db.movimientos_remesas.id > 0)
movimientos_query = db(query).select(
    db.movimientos_remesas.ALL,
    orderby=~db.movimientos_remesas.fecha,
    limitby=(0, 50)
)
print("   Movimientos encontrados con la query: %d" % len(movimientos_query))
for m in movimientos_query:
    print("   - ID: %s, Tipo: %s, Fecha: %s" % (m.id, m.tipo, m.fecha))

print("\n" + "=" * 80)
print("FIN DEL DIAGNOSTICO")
print("=" * 80)
