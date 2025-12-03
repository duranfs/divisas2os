# Guía Rápida de Migración de Cuentas

## Comandos Esenciales

### 1. Backup (OBLIGATORIO)
```bash
python web2py.py -S sistema_divisas -M -R backup_bd_antes_migracion.py
```

### 2. Pruebas
```bash
python test_migracion_cuentas.py
```

### 3. Migración
```bash
python web2py.py -S sistema_divisas -M -R migrar_cuentas.py
```

## Flujo de Ejecución

```
┌─────────────────────────────────────────────────────────────┐
│ 1. BACKUP                                                   │
│    ✓ Copia de seguridad de storage.sqlite                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. PRUEBAS                                                  │
│    ✓ Validar lógica de migración                           │
│    ✓ Verificar generación de números                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. SIMULACIÓN (automática)                                  │
│    ✓ Ejecuta sin modificar BD                              │
│    ✓ Muestra cambios propuestos                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. CONFIRMACIÓN                                             │
│    ⚠️  Escribir "SI" para continuar                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. MIGRACIÓN REAL                                           │
│    ✓ Agrega columnas moneda y saldo                        │
│    ✓ Crea cuentas por moneda                               │
│    ✓ Valida integridad                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. REPORTE                                                  │
│    ✓ Genera reporte_migracion_TIMESTAMP.txt                │
│    ✓ Muestra estadísticas                                  │
└─────────────────────────────────────────────────────────────┘
```

## Qué Hace la Migración

### Antes
```
Cuenta: 12345678901234567890
├── saldo_ves: 1000.00
├── saldo_usd: 50.00
├── saldo_eur: 0.00
└── saldo_usdt: 25.00
```

### Después
```
Cuenta VES: 12345678901234567890 (original)
├── moneda: VES
└── saldo: 1000.00

Cuenta USD: 02[18 dígitos] (nuevo)
├── moneda: USD
└── saldo: 50.00

Cuenta USDT: 04[18 dígitos] (nuevo)
├── moneda: USDT
└── saldo: 25.00
```

## Prefijos de Moneda

| Moneda | Prefijo |
|--------|---------|
| VES    | 01      |
| USD    | 02      |
| EUR    | 03      |
| USDT   | 04      |

## Reglas Importantes

✅ **Siempre se crea cuenta VES** (incluso con saldo 0)
✅ **Mantiene número original** para cuenta VES
✅ **Genera nuevos números** para USD, EUR, USDT
✅ **Solo crea cuentas** con saldo > 0 (excepto VES)

## Validaciones Automáticas

- ✓ Saldos totales coinciden antes/después
- ✓ No se pierden datos
- ✓ Números de cuenta únicos
- ✓ Una cuenta VES por cliente

## Rollback

Si algo sale mal:

```bash
# Restaurar backup
copy backups\storage_antes_migracion_YYYYMMDD.sqlite databases\storage.sqlite
```

## Verificación Post-Migración

```python
# En consola web2py
python web2py.py -S sistema_divisas -M

# Verificar cuentas creadas
print("Total cuentas:", db(db.cuentas.id > 0).count())

# Ver cuentas por moneda
for moneda in ['VES', 'USD', 'EUR', 'USDT']:
    count = db(db.cuentas.moneda == moneda).count()
    print(f"{moneda}: {count} cuentas")

# Ver ejemplo de cuenta
cuenta = db(db.cuentas.moneda == 'VES').select().first()
print(cuenta)
```

## Tiempo Estimado

- Backup: 1-2 minutos
- Pruebas: < 1 minuto
- Migración: 2-10 minutos (depende del tamaño de BD)
- Validación: 1-2 minutos

**Total: ~5-15 minutos**

## Checklist Rápido

Antes:
- [ ] Backup realizado
- [ ] Pruebas OK
- [ ] Horario de baja actividad

Durante:
- [ ] Simulación revisada
- [ ] "SI" confirmado

Después:
- [ ] Reporte revisado
- [ ] Validaciones OK
- [ ] Sistema funcional

## Soporte

❌ **Si hay errores**: NO continuar, restaurar backup
✅ **Si todo OK**: Revisar reporte y validar sistema
