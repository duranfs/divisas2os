# Instrucciones para Probar el Flujo de Venta

## Datos de Prueba Creados

✅ **Usuario de prueba:**
- Email: `duranfs.2012@gmail.com`
- Password: `prueba123`
- Rol: Cliente

✅ **Cuentas disponibles:**
- Cuenta USD: `02543488594019134938` - Saldo: 500.00 USD
- Cuenta VES: `20018485269383304044` - Saldo: 0.00 VES

## Pasos para Probar

### 1. Iniciar el servidor
```bash
python ..\..\web2py.py -a admin123 -i 127.0.0.1 -p 8000
```

### 2. Acceder a la aplicación
Abrir en el navegador:
```
http://127.0.0.1:8000/divisas2os_multiple
```

### 3. Iniciar sesión
- Email: `duranfs.2012@gmail.com`
- Password: `prueba123`

### 4. Ir al módulo de venta
Navegar a:
```
http://127.0.0.1:8000/divisas2os_multiple/divisas/vender
```

### 5. Completar el formulario de venta
- Seleccionar cuenta: `02543488594019134938 (USD)`
- Moneda a vender: `USD`
- Cantidad: `50.00` USD
- Click en "Confirmar Venta"

### 6. Verificar resultados

✅ **Debe mostrar:**
- Comprobante de transacción
- Detalles de la venta
- Nuevos saldos actualizados

❌ **NO debe:**
- Generar error 303
- Mostrar tickets de error
- Fallar al mostrar el comprobante

### 7. Verificar que no hay errores
Ejecutar:
```bash
python leer_tickets_error.py
```

Debe mostrar: "✓ No hay tickets de error registrados"

## Verificación Adicional

Para verificar la transacción en la base de datos:
```bash
python ..\..\web2py.py -S divisas2os_multiple -M
```

Luego en el shell:
```python
# Ver última transacción
ultima = db(db.transacciones.id > 0).select(orderby=~db.transacciones.id).first()
print(f"Comprobante: {ultima.numero_comprobante}")
print(f"Estado: {ultima.estado}")
print(f"Monto: {ultima.monto_origen} {ultima.moneda_origen}")
```

## Requisitos Verificados

- ✅ 2.1: Formulario de venta funcional
- ✅ 2.2: Procesamiento sin errores
- ✅ 2.3: Comprobante se muestra correctamente
- ✅ 2.4: No se generan tickets de error
