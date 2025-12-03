# Design Document - Rediseño de Cuentas por Moneda

## Overview

Este diseño transforma el sistema de cuentas multi-moneda a un modelo bancario tradicional donde cada cuenta maneja una sola moneda. El cambio principal es en la estructura de la tabla `cuentas` y cómo se relacionan las transacciones.

## Architecture

### Modelo Actual vs Nuevo Modelo

**Actual (Multi-moneda):**
```
Cliente → Cuenta (saldo_ves, saldo_usd, saldo_eur, saldo_usdt)
```

**Nuevo (Una moneda por cuenta):**
```
Cliente → Cuenta VES (saldo, moneda='VES')
        → Cuenta USD (saldo, moneda='USD')
        → Cuenta EUR (saldo, moneda='EUR')
        → Cuenta USDT (saldo, moneda='USDT')
```

## Components and Interfaces

### 1. Modelo de Base de Datos

#### Tabla `cuentas` - Nueva Estructura

```python
db.define_table('cuentas',
    Field('cliente_id', 'reference clientes', required=True),
    Field('numero_cuenta', 'string', length=25, unique=True, required=True),
    Field('tipo_cuenta', 'string', length=20, required=True),  # 'corriente', 'ahorro'
    Field('moneda', 'string', length=10, required=True),  # 'VES', 'USD', 'EUR', 'USDT'
    Field('saldo', 'decimal(15,4)', default=0, required=True),  # Un solo campo de saldo
    Field('estado', 'string', length=20, default='activa'),
    Field('fecha_creacion', 'datetime', default=request.now),
    Field('fecha_actualizacion', 'datetime', update=request.now),
    format='%(numero_cuenta)s - %(moneda)s'
)
```

**Cambios clave:**
- ✅ Nuevo campo: `moneda` (VES, USD, EUR, USDT)
- ✅ Un solo campo: `saldo` (en lugar de 4 campos)
- ❌ Eliminados: `saldo_ves`, `saldo_usd`, `saldo_eur`, `saldo_usdt`

#### Índices y Constraints

```python
# Índice compuesto para búsquedas rápidas
db.executesql('CREATE INDEX IF NOT EXISTS idx_cliente_moneda ON cuentas(cliente_id, moneda)')

# Constraint: Un cliente no puede tener dos cuentas activas de la misma moneda
db.executesql('''
    CREATE UNIQUE INDEX IF NOT EXISTS idx_cliente_moneda_activa 
    ON cuentas(cliente_id, moneda) 
    WHERE estado = 'activa'
''')
```

### 2. Generación de Números de Cuenta

#### Formato con Prefijo por Moneda

```
Formato: [PREFIJO][16 DÍGITOS ALEATORIOS]

Prefijos:
- VES: 01xx xxxx xxxx xxxx xxxx
- USD: 02xx xxxx xxxx xxxx xxxx
- EUR: 03xx xxxx xxxx xxxx xxxx
- USDT: 04xx xxxx xxxx xxxx xxxx
```

#### Función de Generación

```python
def generar_numero_cuenta_por_moneda(moneda):
    """
    Genera número de cuenta único con prefijo por moneda
    """
    prefijos = {
        'VES': '01',
        'USD': '02',
        'EUR': '03',
        'USDT': '04'
    }
    
    prefijo = prefijos.get(moneda, '01')
    
    # Generar 18 dígitos aleatorios
    import random
    digitos = ''.join([str(random.randint(0, 9)) for _ in range(18)])
    
    numero_cuenta = prefijo + digitos
    
    # Verificar unicidad
    while db(db.cuentas.numero_cuenta == numero_cuenta).count() > 0:
        digitos = ''.join([str(random.randint(0, 9)) for _ in range(18)])
        numero_cuenta = prefijo + digitos
    
    return numero_cuenta
```

### 3. Script de Migración

#### Estrategia de Migración

1. **Backup**: Respaldar base de datos actual
2. **Análisis**: Identificar cuentas con saldos > 0
3. **Creación**: Crear nuevas cuentas por moneda
4. **Transferencia**: Migrar saldos a nuevas cuentas
5. **Actualización**: Actualizar referencias en transacciones
6. **Validación**: Verificar integridad de datos

#### Script de Migración

```python
def migrar_cuentas_a_moneda_unica():
    """
    Migra cuentas multi-moneda a cuentas individuales por moneda
    """
    print("Iniciando migración de cuentas...")
    
    # 1. Agregar columna 'moneda' si no existe
    try:
        db.executesql("ALTER TABLE cuentas ADD COLUMN moneda VARCHAR(10) DEFAULT 'VES'")
        db.executesql("ALTER TABLE cuentas ADD COLUMN saldo DECIMAL(15,4) DEFAULT 0")
    except:
        pass  # Columnas ya existen
    
    # 2. Obtener todas las cuentas actuales
    cuentas_antiguas = db(db.cuentas.id > 0).select()
    
    cuentas_creadas = 0
    cuentas_migradas = 0
    
    for cuenta_antigua in cuentas_antiguas:
        cliente_id = cuenta_antigua.cliente_id
        
        # Migrar cada moneda con saldo > 0
        monedas_saldos = {
            'VES': float(cuenta_antigua.saldo_ves or 0),
            'USD': float(cuenta_antigua.saldo_usd or 0),
            'EUR': float(cuenta_antigua.saldo_eur or 0),
            'USDT': float(cuenta_antigua.saldo_usdt or 0)
        }
        
        for moneda, saldo in monedas_saldos.items():
            if saldo > 0 or moneda == 'VES':  # Siempre crear cuenta VES
                # Verificar si ya existe cuenta para esta moneda
                cuenta_existente = db(
                    (db.cuentas.cliente_id == cliente_id) &
                    (db.cuentas.moneda == moneda) &
                    (db.cuentas.estado == 'activa')
                ).select().first()
                
                if not cuenta_existente:
                    # Crear nueva cuenta
                    if moneda == 'VES':
                        # Mantener número de cuenta original para VES
                        numero_cuenta = cuenta_antigua.numero_cuenta
                    else:
                        # Generar nuevo número para otras monedas
                        numero_cuenta = generar_numero_cuenta_por_moneda(moneda)
                    
                    db.cuentas.insert(
                        cliente_id=cliente_id,
                        numero_cuenta=numero_cuenta,
                        tipo_cuenta=cuenta_antigua.tipo_cuenta,
                        moneda=moneda,
                        saldo=saldo,
                        estado='activa',
                        fecha_creacion=cuenta_antigua.fecha_creacion
                    )
                    cuentas_creadas += 1
        
        cuentas_migradas += 1
    
    db.commit()
    
    print(f"Migración completada:")
    print(f"  - Cuentas antiguas procesadas: {cuentas_migradas}")
    print(f"  - Nuevas cuentas creadas: {cuentas_creadas}")
    
    return True
```

### 4. Operaciones de Cambio de Divisas

#### Flujo de Compra de Divisas

```
1. Cliente selecciona cuenta VES origen
2. Cliente selecciona moneda a comprar (USD/EUR/USDT)
3. Sistema identifica/crea cuenta destino en esa moneda
4. Sistema calcula monto a debitar en VES
5. Sistema valida saldo suficiente en cuenta VES
6. Sistema debita cuenta VES
7. Sistema acredita cuenta de divisa
8. Sistema registra transacción con ambas cuentas
```

#### Función de Compra

```python
def comprar_divisa(cuenta_ves_id, moneda_comprar, monto_divisa, tasa_cambio):
    """
    Compra divisa debitando de cuenta VES y acreditando en cuenta de divisa
    """
    # Obtener cuenta VES
    cuenta_ves = db.cuentas[cuenta_ves_id]
    if not cuenta_ves or cuenta_ves.moneda != 'VES':
        raise ValueError("Cuenta VES inválida")
    
    # Buscar o crear cuenta de divisa
    cuenta_divisa = db(
        (db.cuentas.cliente_id == cuenta_ves.cliente_id) &
        (db.cuentas.moneda == moneda_comprar) &
        (db.cuentas.estado == 'activa')
    ).select().first()
    
    if not cuenta_divisa:
        # Crear cuenta automáticamente
        numero_cuenta = generar_numero_cuenta_por_moneda(moneda_comprar)
        cuenta_divisa_id = db.cuentas.insert(
            cliente_id=cuenta_ves.cliente_id,
            numero_cuenta=numero_cuenta,
            tipo_cuenta=cuenta_ves.tipo_cuenta,
            moneda=moneda_comprar,
            saldo=0,
            estado='activa'
        )
        cuenta_divisa = db.cuentas[cuenta_divisa_id]
    
    # Calcular monto en VES
    monto_ves = monto_divisa * tasa_cambio
    
    # Validar saldo
    if cuenta_ves.saldo < monto_ves:
        raise ValueError("Saldo insuficiente en cuenta VES")
    
    # Realizar transacción
    cuenta_ves.update_record(saldo=cuenta_ves.saldo - monto_ves)
    cuenta_divisa.update_record(saldo=cuenta_divisa.saldo + monto_divisa)
    
    # Registrar transacción
    db.transacciones.insert(
        cuenta_origen_id=cuenta_ves.id,
        cuenta_destino_id=cuenta_divisa.id,
        tipo_operacion='compra',
        moneda_origen='VES',
        moneda_destino=moneda_comprar,
        monto_origen=monto_ves,
        monto_destino=monto_divisa,
        tasa_cambio=tasa_cambio,
        fecha_transaccion=datetime.datetime.now()
    )
    
    db.commit()
    return True
```

## Data Models

### Modelo de Transacciones Actualizado

```python
db.define_table('transacciones',
    Field('cuenta_origen_id', 'reference cuentas'),  # Cuenta que debita
    Field('cuenta_destino_id', 'reference cuentas'),  # Cuenta que acredita
    Field('tipo_operacion', 'string'),  # 'compra', 'venta', 'transferencia'
    Field('moneda_origen', 'string'),
    Field('moneda_destino', 'string'),
    Field('monto_origen', 'decimal(15,4)'),
    Field('monto_destino', 'decimal(15,4)'),
    Field('tasa_cambio', 'decimal(15,4)'),
    Field('comprobante', 'string', unique=True),
    Field('fecha_transaccion', 'datetime'),
    Field('estado', 'string', default='completada')
)
```

## Error Handling

### Validaciones Principales

1. **Creación de cuenta duplicada**: Validar que no exista cuenta activa de la misma moneda
2. **Saldo insuficiente**: Validar antes de debitar
3. **Cuenta inexistente**: Crear automáticamente si es necesario
4. **Moneda inválida**: Validar que sea VES, USD, EUR o USDT
5. **Cliente inválido**: Validar que las cuentas pertenezcan al mismo cliente

## Testing Strategy

### Pruebas de Migración

1. Crear cuentas de prueba con saldos en múltiples monedas
2. Ejecutar migración
3. Verificar que se crearon las cuentas correctas
4. Verificar que los saldos se transfirieron correctamente
5. Verificar que las transacciones históricas mantienen referencias correctas

### Pruebas de Operaciones

1. Compra de USD desde VES
2. Venta de USD a VES
3. Compra con creación automática de cuenta
4. Validación de saldo insuficiente
5. Transacciones entre cuentas del mismo cliente

## Migration Plan

### Fase 1: Preparación (Sin downtime)
- Agregar columnas nuevas a tabla existente
- Crear funciones de migración
- Realizar backup completo

### Fase 2: Migración (Downtime mínimo)
- Ejecutar script de migración
- Validar integridad de datos
- Actualizar referencias en transacciones

### Fase 3: Actualización de Código
- Actualizar controladores para usar nuevo modelo
- Actualizar vistas para mostrar cuentas por moneda
- Actualizar formularios de creación de cuentas

### Fase 4: Validación
- Pruebas de operaciones de compra/venta
- Pruebas de visualización
- Pruebas de reportes

### Fase 5: Limpieza (Opcional)
- Eliminar columnas antiguas (saldo_ves, saldo_usd, etc.)
- Optimizar índices
- Actualizar documentación
