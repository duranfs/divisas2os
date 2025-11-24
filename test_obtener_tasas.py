print("Probando obtener tasas...")

try:
    tasa = db(db.tasas_cambio.activa == True).select(
        orderby=~db.tasas_cambio.fecha | ~db.tasas_cambio.hora,
        limitby=(0, 1)
    ).first()
    
    if tasa:
        print("Tasa encontrada:")
        print("USD/VES:", tasa.usd_ves)
        print("USDT/VES:", tasa.usdt_ves)
        print("EUR/VES:", tasa.eur_ves)
        print("Tipo de usdt_ves:", type(tasa.usdt_ves))
        print("usdt_ves es None?:", tasa.usdt_ves is None)
        print("usdt_ves evalúa como False?:", not tasa.usdt_ves)
    else:
        print("No se encontró tasa activa")
        
except Exception as e:
    print("ERROR:", str(e))
    import traceback
    traceback.print_exc()
