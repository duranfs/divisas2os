# Guía de Migración de Cuentas Multi-Moneda

## Descripción

Este documento describe el proceso de migración del sistema de cuentas bancarias desde el modelo antiguo (una cuenta con múltiples saldos) al nuevo modelo (una cuenta por moneda).

## Modelo Antiguo vs Nuevo

### Modelo Antiguo (Multi-Moneda)
```
Cliente → Cuenta (saldo_ves, saldo_usd, saldo_eur, saldo_usdt)
```

Una sola cuenta por cliente con 4 campos de saldo diferentes.

### Modelo Nuevo (Una Moneda por Cuenta)
```
Cliente → Cuenta VES (saldo, moneda='VES')
        → Cuenta USD (saldo, moneda='USD')
        → Cuenta EUR (saldo, moneda='EUR')
        → Cuenta USDT (saldo, moneda='USDT')
```

Múltiples cuentas por cliente, cada una con su propia moneda y un solo campo de saldo.

## Archivos del Sistema de Migración

### 1. `migrar_cuentas.py`
Script principal de migración que:
- Agrega las columnas `moneda` y `saldo` a la tabla `cuentas`
- Crea cuentas individuales por cada moneda con saldo > 0
- Mantiene el número de cuenta original para cuentas VES
- Genera nuevos números de cuenta para USD, EUR y USDT
- Valida la integridad de los datos
- Genera reportes detallados

### 2. `test_migracion_cuentas.py`
Suite de pruebas que valida:
- Generación correcta de números de cuenta con prefijos
- Lógica de migración
- Validación de saldos
- Manejo de casos especiales

### 3. `backup_bd_antes_migracion.py`
Script para crear backup de la base de datos antes de la migración.

## Proceso de Migración

### Paso 1: Preparación

#### 1.1 Realizar Backup de la Base de Datos

**CRÍTICO**: Siempre haga un backup antes de ejecutar la migración.

```bash
# Opción 1: Usar el script de backup
python web2py.py -S sistema_divisas -M -R backup_bd_antes_migracion.py

# Opción 2: Backup manual
copy databases\storage.sqlite backups\storage_antes_migracion_%date:~-4,4%%date:~-10,2%%date:~-7,2%.sqlite
```

El backup se guardará en la carpeta `backups/` con timestamp.

#### 1.2 Verificar el Estado Actual

Ejecute consultas para conocer el estado actual:

```python
# En la consola de web2py
python web2py.py -S sistema_divisas -M

# Contar cuentas actuales
print("Total de cuentas:", db(db.cuentas.id > 0).count())

# Ver estructura de una cuenta
cuenta = db(db.cuentas.id > 0).select().first()
print(cuenta)
```

### Paso 2: Ejecutar Pruebas

Antes de la migración real, ejecute las pruebas:

```bash
python test_migracion_cuentas.py
```

Debe ver:
```
✅ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE
```

### Paso 3: Simulación de Migración

El script incluye un modo de simulación que no modifica la base de datos:

```bash
python web2py.py -S sistema_divisas -M -R migrar_cuentas.py
```

El script automáticamente:
1. Ejecuta primero en modo simulación
2. Muestra qué cambios se realizarían
3. Solicita confirmación antes de proceder

**Revise cuidadosamente la salida de la simulación.**

### Paso 4: Migración Real

Si la simulación es exitosa, el script solicitará confirmación:

```
¿Desea continuar con la migración REAL? (escriba 'SI' para confirmar):
```

Escriba `SI` (en mayúsculas) para continuar.

### Paso 5: Validación Post-Migración

El script automáticamente:
- Valida que los saldos totales coincidan
- Verifica que se crearon todas las cuentas esperadas
- Genera un reporte detallado

Revise el reporte generado: `reporte_migracion_YYYYMMDD_HHMMSS.txt`

## Estructura de Números de Cuenta

El nuevo sistema usa prefijos para identificar la moneda:

| Moneda | Prefijo | Ejemplo |
|--------|---------|---------|
| VES    | 01      | 01234567890123456789 |
| USD    | 02      | 02987654321098765432 |
| EUR    | 03      | 03111111111111111111 |
| USDT   | 04      | 04555555555555555555 |

- **VES**: Mantiene el número de cuenta original
- **USD/EUR/USDT**: Se generan nuevos números con el prefijo correspondiente

## Reglas de Migración

### 1. Creación de Cuentas VES
- **Siempre** se crea una cuenta VES para cada cliente
- Incluso si el saldo VES es 0
- Mantiene el número de cuenta original

### 2. Creación de Otras Monedas
- Solo se crean cuentas USD, EUR o USDT si tienen saldo > 0
- Se generan nuevos números de cuenta con prefijos

### 3. Preservación de Datos
- Se mantienen todos los campos originales
- Los campos antiguos (`saldo_ves`, `saldo_usd`, etc.) se ponen en 0
- Se agregan los nuevos campos (`moneda`, `saldo`)

## Ejemplos de Migración

### Ejemplo 1: Cuenta con Múltiples Saldos

**Antes:**
```
Cuenta: 12345678901234567890
Cliente: Juan Pérez
saldo_ves: 10,000.00
saldo_usd: 500.00
saldo_eur: 0.00
saldo_usdt: 50.00
```

**Después:**
```
Cuenta 1:
  numero_cuenta: 12345678901234567890 (original)
  moneda: VES
  saldo: 10,000.00

Cuenta 2:
  numero_cuenta: 02[18 dígitos aleatorios] (nuevo)
  moneda: USD
  saldo: 500.00

Cuenta 3:
  numero_cuenta: 04[18 dígitos aleatorios] (nuevo)
  moneda: USDT
  saldo: 50.00
```

**Nota**: No se crea cuenta EUR porque el saldo es 0.

### Ejemplo 2: Cuenta Sin Saldos

**Antes:**
```
Cuenta: 09876543210987654321
Cliente: María González
saldo_ves: 0.00
saldo_usd: 0.00
saldo_eur: 0.00
saldo_usdt: 0.00
```

**Después:**
```
Cuenta 1:
  numero_cuenta: 09876543210987654321 (original)
  moneda: VES
  saldo: 0.00
```

**Nota**: Solo se crea cuenta VES, las demás no se crean.

## Validaciones Automáticas

El script realiza las siguientes validaciones:

### 1. Integridad de Saldos
```
✅ Verifica que la suma de saldos antes = suma de saldos después
```

### 2. Creación de Cuentas
```
✅ Verifica que se creó al menos una cuenta VES por cliente
✅ Verifica que solo se crearon cuentas con saldo > 0 (excepto VES)
```

### 3. Unicidad de Números de Cuenta
```
✅ Verifica que no hay números de cuenta duplicados
```

## Reporte de Migración

El script genera un reporte detallado con:

### Estadísticas
- Cuentas procesadas
- Cuentas creadas
- Desglose por moneda

### Saldos Totales
- Antes de la migración
- Después de la migración
- Diferencias (deben ser 0)

### Problemas Encontrados
- Lista de errores o advertencias
- Detalles de cada problema

### Ejemplo de Reporte
```
================================================================================
REPORTE DE MIGRACIÓN DE CUENTAS
================================================================================

Fecha y Hora: 2025-11-25 14:30:00

Estado: ✅ EXITOSA

--------------------------------------------------------------------------------
ESTADÍSTICAS
--------------------------------------------------------------------------------

Cuentas procesadas: 150
Cuentas creadas: 320

Desglose por moneda:
  - Cuentas VES: 150
  - Cuentas USD: 120
  - Cuentas EUR: 30
  - Cuentas USDT: 20

--------------------------------------------------------------------------------
SALDOS TOTALES
--------------------------------------------------------------------------------

ANTES de la migración:
  VES: 1,500,000.00
  USD: 75,000.00
  EUR: 15,000.00
  USDT: 5,000.00

DESPUÉS de la migración:
  VES: 1,500,000.00
  USD: 75,000.00
  EUR: 15,000.00
  USDT: 5,000.00

DIFERENCIAS:
  VES: 0.00
  USD: 0.00
  EUR: 0.00
  USDT: 0.00

================================================================================
FIN DEL REPORTE
================================================================================
```

## Solución de Problemas

### Problema: "Columnas ya existen"
**Causa**: La migración ya se ejecutó parcialmente.

**Solución**: 
1. Restaure el backup
2. Ejecute la migración completa nuevamente

### Problema: "Diferencias en saldos"
**Causa**: Error en la lógica de migración o datos corruptos.

**Solución**:
1. **NO continúe con la migración**
2. Restaure el backup
3. Revise los datos originales
4. Contacte al equipo de desarrollo

### Problema: "Error al generar número de cuenta"
**Causa**: Demasiados intentos fallidos de generar número único.

**Solución**:
1. Verifique que no hay números de cuenta duplicados en la base de datos
2. Ejecute la migración nuevamente

### Problema: "Timeout o proceso muy lento"
**Causa**: Base de datos muy grande.

**Solución**:
1. Ejecute la migración en horario de baja actividad
2. Considere migrar por lotes (modificar el script)

## Rollback (Reversión)

Si necesita revertir la migración:

### Opción 1: Restaurar Backup Completo
```bash
# Detener el servidor web2py
# Restaurar el archivo de backup
copy backups\storage_antes_migracion_YYYYMMDD.sqlite databases\storage.sqlite
# Reiniciar el servidor
```

### Opción 2: Eliminar Cuentas Nuevas (Parcial)
```python
# Solo si necesita mantener algunos datos
# CUIDADO: Esto es irreversible

# Eliminar cuentas con moneda definida (nuevas)
db(db.cuentas.moneda != None).delete()
db.commit()

# Eliminar columnas nuevas
db.executesql("ALTER TABLE cuentas DROP COLUMN moneda")
db.executesql("ALTER TABLE cuentas DROP COLUMN saldo")
db.commit()
```

## Checklist de Migración

Antes de ejecutar:
- [ ] Backup de base de datos realizado
- [ ] Pruebas ejecutadas exitosamente
- [ ] Simulación revisada
- [ ] Equipo notificado
- [ ] Horario de baja actividad seleccionado

Durante la ejecución:
- [ ] Simulación completada sin errores
- [ ] Confirmación proporcionada
- [ ] Migración real en progreso
- [ ] Monitoreo de salida del script

Después de ejecutar:
- [ ] Reporte de migración revisado
- [ ] Validaciones pasadas
- [ ] Saldos verificados
- [ ] Pruebas funcionales realizadas
- [ ] Sistema en producción

## Contacto y Soporte

Si encuentra problemas durante la migración:

1. **NO continúe** si hay errores críticos
2. Guarde el reporte de migración
3. Restaure el backup si es necesario
4. Contacte al equipo de desarrollo con:
   - Reporte de migración
   - Logs de error
   - Descripción del problema

## Notas Importantes

⚠️ **ADVERTENCIAS**:
- La migración modifica la estructura de la base de datos
- Siempre haga backup antes de ejecutar
- Ejecute en horario de baja actividad
- Revise cuidadosamente la simulación
- No interrumpa el proceso una vez iniciado

✅ **RECOMENDACIONES**:
- Pruebe primero en un ambiente de desarrollo
- Documente cualquier problema encontrado
- Mantenga los backups por al menos 30 días
- Valide el sistema después de la migración

## Historial de Versiones

- **v1.0** (2025-11-25): Versión inicial del script de migración
  - Migración de cuentas multi-moneda a cuentas individuales
  - Validaciones automáticas
  - Generación de reportes
  - Modo de simulación
