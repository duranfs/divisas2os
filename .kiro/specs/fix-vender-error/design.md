# Design Document - Fix Vender Error

## Overview

Este diseño aborda la corrección del error crítico en la función `comprobante()` del controlador de divisas. El problema radica en que la función intenta usar variables `cuenta_origen` y `cuenta_destino` que nunca fueron definidas, causando un error cuando los usuarios intentan ver comprobantes de transacciones.

La solución implica simplificar la lógica de la función para usar únicamente la información disponible en la transacción y realizar consultas explícitas cuando se necesite información adicional.

## Architecture

### Componentes Afectados

1. **controllers/divisas.py**
   - Función `comprobante()` - Requiere corrección completa
   - Función `vender()` - Verificar que el flujo de redirección funcione correctamente

2. **views/divisas/comprobante.html** (si existe)
   - Verificar que el template use las variables correctas

### Flujo de Datos Corregido

```
Usuario completa venta
    ↓
procesar_venta_divisa() ejecuta transacción
    ↓
Genera transaccion_id y numero_comprobante
    ↓
Redirect a comprobante(transaccion_id)
    ↓
comprobante() obtiene transacción por ID
    ↓
Obtiene cuenta usando transaccion.cuenta_id
    ↓
Obtiene cliente usando cuenta.cliente_id
    ↓
Renderiza vista con datos completos
```

## Components and Interfaces

### Función comprobante() - Diseño Corregido

```python
@auth.requires_login()
def comprobante():
    """
    Muestra el comprobante de una transacción
    Requisitos: 6.2, 6.4
    """
    try:
        # Validar que se recibió ID de transacción
        if not request.args(0):
            response.flash = "ID de transacción requerido"
            redirect(URL('divisas', 'index'))
        
        transaccion_id = request.args(0)
        
        # Obtener la transacción
        transaccion = db(db.transacciones.id == transaccion_id).select().first()
        
        if not transaccion:
            response.flash = "Transacción no encontrada"
            redirect(URL('divisas', 'index'))
        
        # Obtener cuenta de la transacción (usando cuenta_id que existe en BD)
        cuenta = db(db.cuentas.id == transaccion.cuenta_id).select().first()
        
        if not cuenta:
            response.flash = "Cuenta de la transacción no encontrada"
            redirect(URL('divisas', 'index'))
        
        # Obtener el cliente
        cliente = db(db.clientes.id == cuenta.cliente_id).select().first()
        
        if not cliente:
            response.flash = "Cliente no encontrado"
            redirect(URL('divisas', 'index'))
        
        # Verificar permisos: debe ser el dueño de la cuenta o administrador
        es_admin = auth.has_membership('administrador') or auth.has_membership('operador')
        cliente_actual = db(db.clientes.user_id == auth.user.id).select().first()
        es_propietario = cliente_actual and cliente_actual.id == cliente.id
        
        if not (es_propietario or es_admin):
            response.flash = "Acceso no autorizado a esta transacción"
            redirect(URL('divisas', 'index'))
        
        # Obtener el usuario asociado al cliente
        usuario_cliente = db(db.auth_user.id == cliente.user_id).select().first()
        
        # CORRECCIÓN: Pasar solo variables definidas
        return dict(
            transaccion=transaccion,
            cuenta=cuenta,  # Solo una cuenta, la de la transacción
            cliente=cliente,
            usuario_cliente=usuario_cliente
        )
        
    except Exception as e:
        logger.error(f"Error mostrando comprobante: {str(e)}")
        response.flash = f"Error: {str(e)}"
        redirect(URL('divisas', 'index'))
```

### Cambios Clave

1. **Eliminación de variables no definidas**: Se eliminan las referencias a `cuenta_origen` y `cuenta_destino`
2. **Uso de cuenta única**: Se pasa solo `cuenta` que es la cuenta asociada a la transacción
3. **Información completa en transacción**: La tabla transacciones ya contiene `moneda_origen`, `moneda_destino`, `monto_origen`, `monto_destino`

## Data Models

### Tabla transacciones (existente)

```python
db.define_table('transacciones',
    Field('cuenta_id', 'reference cuentas'),  # Cuenta principal de la transacción
    Field('tipo_operacion', 'string'),        # 'compra' o 'venta'
    Field('moneda_origen', 'string'),         # Moneda que se entrega
    Field('moneda_destino', 'string'),        # Moneda que se recibe
    Field('monto_origen', 'decimal(15,2)'),   # Cantidad entregada
    Field('monto_destino', 'decimal(15,2)'),  # Cantidad recibida
    Field('tasa_aplicada', 'decimal(15,6)'),  # Tasa de cambio usada
    Field('comision', 'decimal(15,2)'),       # Comisión cobrada
    Field('numero_comprobante', 'string'),    # Comprobante único
    Field('estado', 'string'),                # Estado de la transacción
    Field('fecha_transaccion', 'datetime')
)
```

**Nota**: La transacción ya contiene toda la información necesaria. No necesitamos referencias a múltiples cuentas en el comprobante.

## Error Handling

### Escenarios de Error

1. **Transacción no encontrada**
   - Mensaje: "Transacción no encontrada"
   - Acción: Redirect a divisas/index

2. **Cuenta no encontrada**
   - Mensaje: "Cuenta de la transacción no encontrada"
   - Acción: Redirect a divisas/index

3. **Cliente no encontrado**
   - Mensaje: "Cliente no encontrado"
   - Acción: Redirect a divisas/index

4. **Acceso no autorizado**
   - Mensaje: "Acceso no autorizado a esta transacción"
   - Acción: Redirect a divisas/index

5. **Excepción general**
   - Log del error completo
   - Mensaje: "Error: {descripción}"
   - Acción: Redirect a divisas/index

## Testing Strategy

### Pruebas Unitarias

1. **Test de comprobante con transacción válida**
   - Crear transacción de prueba
   - Llamar a comprobante(transaccion_id)
   - Verificar que retorna dict con todas las variables necesarias

2. **Test de comprobante sin ID**
   - Llamar a comprobante() sin args
   - Verificar que redirige con mensaje de error

3. **Test de comprobante con ID inválido**
   - Llamar a comprobante(999999)
   - Verificar que redirige con mensaje de error

4. **Test de permisos**
   - Crear transacción de otro usuario
   - Intentar acceder como usuario no autorizado
   - Verificar que redirige con mensaje de error

### Pruebas de Integración

1. **Flujo completo de venta**
   - Login como cliente
   - Acceder a vender()
   - Completar formulario de venta
   - Verificar que procesa correctamente
   - Verificar que muestra comprobante sin errores

2. **Flujo completo de compra**
   - Login como cliente
   - Acceder a comprar()
   - Completar formulario de compra
   - Verificar que procesa correctamente
   - Verificar que muestra comprobante sin errores

### Pruebas Manuales

1. Acceder a /divisas/vender
2. Completar una venta de prueba
3. Verificar que el comprobante se muestra correctamente
4. Verificar que no hay errores en el log

## Implementation Notes

### Orden de Implementación

1. Corregir función `comprobante()` en controllers/divisas.py
2. Verificar que la vista comprobante.html use las variables correctas
3. Probar flujo completo de venta
4. Probar flujo completo de compra
5. Verificar logs para asegurar que no hay errores

### Consideraciones

- La función `procesar_venta_divisa()` ya funciona correctamente y genera el `transaccion_id`
- El redirect en `vender()` usa `raise HTTP(303, ...)` que es la forma correcta en web2py
- No se requieren cambios en la base de datos
- No se requieren cambios en las funciones de procesamiento de transacciones
