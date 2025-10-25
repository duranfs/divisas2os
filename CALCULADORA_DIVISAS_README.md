# 🧮 Calculadora Automática de Divisas

## 📋 Descripción

Nueva funcionalidad implementada en el Sistema de Divisas Bancario que permite a los usuarios calcular automáticamente los montos en bolívares al comprar o vender divisas extranjeras.

## ✨ Características Principales

### 🎯 Facilidad de Uso
- **Entrada intuitiva**: El usuario solo ingresa la cantidad de divisa que quiere comprar/vender
- **Cálculo automático**: El sistema calcula automáticamente los bolívares necesarios/recibidos
- **Actualización en tiempo real**: Los cálculos se actualizan mientras el usuario escribe

### 🎨 Diseño Visual
- **Colores distintivos**:
  - 🟡 **Amarillo**: Campos que muestran dinero que el usuario paga
  - 🟢 **Verde**: Campos que muestran dinero que el usuario recibe
- **Iconos descriptivos**: Calculadora, monedas, ojo (solo lectura)
- **Responsive**: Funciona perfectamente en móviles y escritorio

### 🔧 Funcionalidades Técnicas
- **Tasas en tiempo real**: Integración con API del BCV
- **Fallback inteligente**: Valores por defecto si no hay conexión
- **Validación automática**: Verifica fondos antes de procesar
- **Logging completo**: Registra todos los cálculos para auditoría

## 📁 Archivos Modificados/Creados

### Vistas (HTML)
- `views/divisas/comprar.html` - Formulario de compra mejorado
- `views/divisas/vender.html` - Formulario de venta mejorado
- `views/divisas/prueba_calculadora.html` - Página de prueba
- `views/default/dashboard.html` - Widget informativo agregado

### JavaScript
- `static/js/calculadora_divisas.js` - Lógica de cálculo automático

### CSS
- `static/css/calculadora-divisas.css` - Estilos para campos calculados

### Controladores (Python)
- `controllers/divisas.py` - Funciones actualizadas para nueva lógica
- `controllers/api.py` - Endpoint de tasas agregado

### Configuración
- `models/menu.py` - Enlace a página de prueba agregado

## 🎮 Flujo de Usuario

### Para Comprar Divisas:
1. Usuario accede a **Divisas → Comprar Divisas**
2. Selecciona la divisa (USD o EUR)
3. Ingresa la **cantidad de divisa** que quiere comprar
4. Ve automáticamente cuántos **bolívares necesita pagar** (campo amarillo)
5. Confirma la operación

### Para Vender Divisas:
1. Usuario accede a **Divisas → Vender Divisas**
2. Selecciona la divisa (USD o EUR)
3. Ingresa la **cantidad de divisa** que quiere vender
4. Ve automáticamente cuántos **bolívares recibirá** (campo verde)
5. Confirma la operación

## 🧪 Página de Prueba

**URL**: `/divisas/prueba_calculadora`

**Acceso**: Menú Divisas → 🧪 Prueba Calculadora

**Funciones**:
- Simulación de compra y venta sin procesar transacciones reales
- Widget de tasas en tiempo real
- Log de cálculos realizados
- Ejemplos interactivos

## 📊 Ejemplos de Uso

### Ejemplo 1: Comprar USD
```
Usuario quiere: 100 USD
Tasa del día: 36.50 VES/USD
Sistema calcula: 3,650.00 VES necesarios
```

### Ejemplo 2: Vender EUR
```
Usuario quiere vender: 50 EUR
Tasa del día: 40.60 VES/EUR
Sistema calcula: 2,030.00 VES a recibir
```

## 🔗 Integración con Sistema Existente

### Compatibilidad
- ✅ Mantiene funcionamiento con método anterior
- ✅ Acepta tanto `cantidad_divisa` (nuevo) como `monto_origen` (anterior)
- ✅ No afecta transacciones existentes
- ✅ Funciona con todas las validaciones actuales

### API Endpoints
- `GET /api/tasas_actuales` - Obtiene tasas actuales en formato JSON
- `POST /divisas/calcular_cambio` - Calcula conversiones (existente)
- `POST /divisas/validar_fondos` - Valida fondos disponibles (existente)

## 🎯 Beneficios para el Usuario

1. **Simplicidad**: No necesita calcular manualmente
2. **Precisión**: Usa tasas oficiales actualizadas
3. **Transparencia**: Ve exactamente cuánto pagará/recibirá
4. **Rapidez**: Cálculos instantáneos mientras escribe
5. **Confianza**: Colores y iconos claros indican entrada/salida de dinero

## 🛠️ Configuración Técnica

### Tasas por Defecto
```javascript
USD: { compra: 36.50, venta: 36.80 }
EUR: { compra: 40.25, venta: 40.60 }
```

### Actualización de Tasas
- **Fuente**: API del BCV
- **Frecuencia**: Tiempo real al cargar página
- **Fallback**: Valores por defecto si hay error

### Validaciones
- Monto mínimo: 0.01 para divisas
- Verificación de fondos automática
- Validación de cuentas activas

## 📱 Responsive Design

La calculadora funciona perfectamente en:
- 💻 **Desktop**: Experiencia completa
- 📱 **Móvil**: Campos adaptados, texto centrado
- 📟 **Tablet**: Layout optimizado

## 🎨 Ayuda Contextual

Cada página incluye:
- **Botón "¿Cómo funciona?"**: Modal explicativo
- **Ejemplos prácticos**: Casos de uso reales
- **Colores explicados**: Qué significa cada color
- **Pasos simples**: Guía paso a paso

## 🔍 Testing

Para probar la funcionalidad:
1. Acceder a `/divisas/prueba_calculadora`
2. Probar diferentes cantidades y divisas
3. Verificar cálculos en el log
4. Comprobar actualización de tasas

## 📈 Métricas de Éxito

- ✅ Reducción de errores de usuario en cálculos
- ✅ Menor tiempo para completar transacciones
- ✅ Mayor satisfacción del usuario
- ✅ Menos consultas de soporte sobre cálculos

---

**Desarrollado para el Sistema de Divisas Bancario**  
*Versión: 1.0 - Implementación Inicial*