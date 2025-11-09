# 📚 EXPLICACIÓN SIMPLE: LÍMITES DE VENTA

## ❓ ¿Qué es un límite de venta?

Un **límite de venta** es el **monto máximo** que puedes vender en un día de una moneda específica.

### 🎯 Ejemplo Real:

Imagina que tu banco recibe hoy:
- **$10,000 USD** en remesas

Pero NO quieres vender todo hoy porque:
- ✅ Necesitas liquidez para mañana
- ✅ Quieres controlar el flujo de ventas
- ✅ Evitas quedarte sin divisas

**Solución:** Configuras un **límite de $7,000 USD**

Esto significa:
- ✅ Puedes vender hasta $7,000 hoy
- ❌ El sistema bloqueará ventas que excedan $7,000
- 💰 Te quedan $3,000 de reserva

---

## 🔄 ¿Cómo funciona AUTOMÁTICAMENTE?

### ✅ LO QUE TÚ HACES (1 vez al día):

```
Configuras: "Límite diario USD = $7,000"
```

### ✅ LO QUE EL SISTEMA HACE (automáticamente):

```
Inicio del día:
├─ Límite diario: $7,000
├─ Monto vendido: $0
└─ Monto disponible: $7,000

Cliente compra $2,000:
├─ Límite diario: $7,000 (no cambia)
├─ Monto vendido: $2,000 ✅ (actualizado automáticamente)
└─ Monto disponible: $5,000 ✅ (actualizado automáticamente)

Cliente compra $3,000:
├─ Límite diario: $7,000 (no cambia)
├─ Monto vendido: $5,000 ✅ (actualizado automáticamente)
└─ Monto disponible: $2,000 ✅ (actualizado automáticamente)

Cliente intenta comprar $3,000:
└─ ❌ RECHAZADO: "Venta de $3,000 excede límite disponible de $2,000"
```

---

## 🎨 NUEVA VISTA SIMPLIFICADA

### Antes (confusa):
```
❌ Configurar:
   - Fecha
   - Moneda
   - Límite diario
   - Monto vendido  ← ¿Por qué configurar esto?
   - Monto disponible  ← ¿Por qué configurar esto?
   - Usuario configuración  ← ¿Para qué?
```

### Ahora (simple):
```
✅ Solo configuras:
   - Límite diario: $7,000
   
   [Botón: Guardar]
   
✅ El sistema muestra automáticamente:
   - Vendido: $2,000
   - Disponible: $5,000
   - Porcentaje usado: 28.6%
```

---

## 📱 CÓMO USAR LA NUEVA VISTA

### Paso 1: Acceder
```
Menú > Remesas > Configurar Límites
```

### Paso 2: Ver remesas disponibles
Cada tarjeta muestra:
```
┌─────────────────────────────┐
│         💵 USD              │
├─────────────────────────────┤
│ Remesa disponible hoy:      │
│ $10,000.00                  │
│                             │
│ Límite de venta para HOY:   │
│ $ [_______]                 │
│                             │
│ [50%] [75%] [90%] [100%]   │ ← Botones rápidos
│                             │
│ [Configurar Límite]         │
└─────────────────────────────┘
```

### Paso 3: Configurar límite

**Opción A - Manual:**
1. Escribe el monto: `7000`
2. Click en "Configurar Límite"

**Opción B - Rápida:**
1. Click en botón "90%" 
2. Se llena automáticamente: `9000` (90% de $10,000)
3. Click en "Configurar Límite"

### Paso 4: Ver estado actual
Si ya hay un límite configurado, verás:
```
⚠️ Límite actual: $7,000.00
   Vendido: $2,000.00
   Disponible: $5,000.00
   
   [████████░░] 28%
```

---

## 🧪 EJEMPLO COMPLETO

### Escenario: Banco recibe remesas

**Lunes 9:00 AM:**
```
Recibes remesas:
├─ USD: $10,000
├─ EUR: €8,000
└─ USDT: ₮15,000
```

**Lunes 9:15 AM - Configuras límites:**
```
USD:  $7,000  (70% de la remesa)
EUR:  €6,000  (75% de la remesa)
USDT: ₮13,000 (87% de la remesa)
```

**Lunes 10:00 AM - Cliente compra:**
```
Cliente 1: Compra $2,000 USD ✅
├─ Límite USD: $7,000
├─ Vendido: $2,000
└─ Disponible: $5,000
```

**Lunes 11:00 AM - Cliente compra:**
```
Cliente 2: Compra $3,500 USD ✅
├─ Límite USD: $7,000
├─ Vendido: $5,500
└─ Disponible: $1,500
```

**Lunes 12:00 PM - Cliente intenta comprar:**
```
Cliente 3: Intenta comprar $2,000 USD ❌
└─ RECHAZADO: "Venta de $2,000 excede límite disponible de $1,500"
```

**Lunes 12:15 PM - Cliente compra:**
```
Cliente 3: Compra $1,500 USD ✅
├─ Límite USD: $7,000
├─ Vendido: $7,000
└─ Disponible: $0
```

**Lunes 2:00 PM - Cliente intenta comprar:**
```
Cliente 4: Intenta comprar $500 USD ❌
└─ RECHAZADO: "Venta de $500 excede límite disponible de $0"
```

**Martes 9:00 AM - Nuevo día:**
```
✅ Límites se resetean automáticamente
✅ Debes configurar nuevos límites para hoy
```

---

## ❓ PREGUNTAS FRECUENTES

### 1. ¿Tengo que configurar límites todos los días?
**Sí**, los límites son diarios. Cada día debes configurar nuevos límites basados en las remesas recibidas.

### 2. ¿Puedo cambiar el límite durante el día?
**Sí**, puedes actualizar el límite en cualquier momento. El sistema mantendrá el monto ya vendido.

**Ejemplo:**
```
Límite inicial: $7,000
Vendido: $3,000
Disponible: $4,000

Actualizas límite a: $10,000
Vendido: $3,000 (se mantiene)
Disponible: $7,000 (se recalcula)
```

### 3. ¿Qué pasa si tengo $10,000 en remesas pero configuro límite de $5,000?
**Perfecto**, solo podrás vender $5,000 aunque tengas $10,000 disponibles. Los otros $5,000 quedan como reserva.

### 4. ¿Puedo configurar un límite mayor a la remesa?
**No**, el sistema no te dejará. El límite máximo es igual a la remesa disponible.

### 5. ¿Qué son las alertas del 80% y 95%?
Cuando alcanzas esos porcentajes del límite, el sistema envía alertas:
```
80% alcanzado: ⚠️ "Alerta: Límite USD al 80%"
95% alcanzado: 🚨 "Crítico: Límite USD al 95%"
```

### 6. ¿Tengo que configurar "monto vendido" o "monto disponible"?
**NO**, ¡nunca! El sistema los calcula automáticamente. Solo configuras el "límite diario".

### 7. Si tengo 1000 clientes, ¿debo configurar 1000 límites?
**NO**, configuras UN límite por moneda por día:
```
Límite USD: $7,000 (para TODOS los clientes)
```

Todos los clientes comparten el mismo límite. Cuando se agota, nadie más puede comprar hasta el día siguiente.

---

## 🎯 VENTAJAS DEL SISTEMA

### ✅ Control de liquidez
No vendes más de lo que quieres vender.

### ✅ Reserva automática
Siempre mantienes una reserva de divisas.

### ✅ Alertas proactivas
Te avisa cuando te estás quedando sin límite.

### ✅ Bloqueo automático
No necesitas estar pendiente, el sistema bloquea ventas que excedan el límite.

### ✅ Trazabilidad completa
Todo queda registrado en el historial.

---

## 🚀 ACCESO A LA NUEVA VISTA

### URL directa:
```
http://127.0.0.1:8000/divisas2os/remesas/configurar_limites_simple
```

### Desde el menú:
```
Remesas > Configurar Límites (Simple)
```

---

## 📞 ¿NECESITAS AYUDA?

Si algo no está claro:
1. Revisa este documento
2. Prueba con montos pequeños primero
3. Verifica el historial de movimientos

**Recuerda:** Solo configuras el límite diario, el sistema hace todo lo demás automáticamente.
