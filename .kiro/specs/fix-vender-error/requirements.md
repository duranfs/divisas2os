# Requirements Document - Fix Vender Error

## Introduction

El sistema de divisas bancario presenta un error crítico en el módulo de ventas. Cuando un usuario intenta acceder a la función de ventas (`vender()`), el sistema genera un ticket de error. El análisis del código revela que la función `comprobante()` en `controllers/divisas.py` tiene variables no definidas (`cuenta_origen` y `cuenta_destino`) que causan el fallo cuando se intenta mostrar el comprobante después de una venta.

## Glossary

- **Sistema de Divisas**: Sistema web bancario para compra y venta de divisas
- **Controlador**: Archivo Python que maneja la lógica de negocio en web2py
- **Transacción**: Operación de compra o venta de divisas
- **Comprobante**: Documento que confirma una transacción realizada
- **web2py**: Framework web Python con arquitectura MVC

## Requirements

### Requirement 1: Corregir función comprobante

**User Story:** Como desarrollador del sistema, quiero que la función `comprobante()` funcione correctamente, para que los usuarios puedan ver sus comprobantes de transacción sin errores.

#### Acceptance Criteria

1. WHEN THE Sistema de Divisas ejecuta la función `comprobante()`, THE Sistema de Divisas SHALL obtener la cuenta asociada a la transacción usando el campo `cuenta_id` de la tabla transacciones
2. WHEN THE Sistema de Divisas necesita mostrar información de cuentas en el comprobante, THE Sistema de Divisas SHALL usar únicamente la cuenta obtenida de la transacción sin referenciar variables no definidas
3. WHEN THE Sistema de Divisas renderiza la vista del comprobante, THE Sistema de Divisas SHALL pasar únicamente las variables definidas y válidas al template
4. IF THE Sistema de Divisas encuentra una transacción sin cuenta asociada, THEN THE Sistema de Divisas SHALL mostrar un mensaje de error descriptivo y redirigir al usuario al índice de divisas

### Requirement 2: Validar flujo de venta completo

**User Story:** Como usuario del sistema, quiero poder realizar ventas de divisas sin errores, para que pueda completar mis transacciones exitosamente.

#### Acceptance Criteria

1. WHEN un usuario autenticado accede a la función `vender()`, THE Sistema de Divisas SHALL mostrar el formulario de venta con las cuentas disponibles
2. WHEN un usuario confirma una venta, THE Sistema de Divisas SHALL procesar la transacción y generar un comprobante único
3. WHEN THE Sistema de Divisas completa una venta exitosamente, THE Sistema de Divisas SHALL redirigir al usuario a la página de comprobante usando el ID de transacción
4. WHEN THE Sistema de Divisas muestra el comprobante, THE Sistema de Divisas SHALL mostrar toda la información relevante de la transacción sin generar errores

### Requirement 3: Asegurar consistencia en manejo de cuentas

**User Story:** Como desarrollador del sistema, quiero que el manejo de cuentas sea consistente en todas las funciones, para que no haya errores por referencias incorrectas.

#### Acceptance Criteria

1. THE Sistema de Divisas SHALL usar el campo `cuenta_id` de la tabla transacciones para obtener la cuenta asociada a cada transacción
2. THE Sistema de Divisas SHALL obtener información del cliente a través de la relación cuenta-cliente
3. WHEN THE Sistema de Divisas necesita información de múltiples cuentas, THE Sistema de Divisas SHALL realizar consultas explícitas a la base de datos
4. THE Sistema de Divisas SHALL evitar el uso de variables no definidas en todas las funciones del controlador de divisas
