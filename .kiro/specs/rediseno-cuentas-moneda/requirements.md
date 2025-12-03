# Requirements Document

## Introduction

Este documento define los requisitos para rediseñar el sistema de cuentas bancarias, cambiando de un modelo multi-moneda (una cuenta con múltiples saldos) a un modelo tradicional bancario (una cuenta por moneda).

## Glossary

- **Sistema**: Sistema de Divisas Bancario web2py
- **Cuenta**: Cuenta bancaria asociada a un cliente
- **Moneda**: Tipo de divisa (VES, USD, EUR, USDT)
- **Cliente**: Usuario del sistema bancario
- **Saldo**: Cantidad de dinero en una cuenta
- **Transacción**: Operación de compra/venta de divisas
- **Número de Cuenta**: Identificador único de 20 dígitos

## Requirements

### Requirement 1: Modelo de Cuenta por Moneda

**User Story:** Como administrador del sistema, quiero que cada cuenta bancaria maneje una sola moneda, para cumplir con estándares bancarios tradicionales y facilitar auditorías.

#### Acceptance Criteria

1. WHEN el Sistema crea una cuenta, THE Sistema SHALL asignar exactamente una moneda a esa cuenta
2. WHEN el Sistema almacena el saldo de una cuenta, THE Sistema SHALL usar un único campo de saldo en lugar de múltiples campos por moneda
3. WHEN un cliente consulta sus cuentas, THE Sistema SHALL mostrar una lista de cuentas separadas por moneda
4. WHERE una cuenta existe, THE Sistema SHALL garantizar que solo puede tener transacciones en su moneda asignada
5. WHEN el Sistema genera un número de cuenta, THE Sistema SHALL incluir un prefijo que identifique la moneda

### Requirement 2: Migración de Datos Existentes

**User Story:** Como administrador del sistema, quiero migrar las cuentas existentes multi-moneda a cuentas individuales por moneda, para mantener la integridad de los datos históricos.

#### Acceptance Criteria

1. WHEN el Sistema ejecuta la migración, THE Sistema SHALL crear una cuenta separada por cada moneda que tenga saldo mayor a cero
2. WHEN el Sistema migra una cuenta, THE Sistema SHALL preservar el número de cuenta original para la moneda principal (VES)
3. WHEN el Sistema genera nuevas cuentas durante la migración, THE Sistema SHALL crear números de cuenta únicos con prefijos por moneda
4. WHEN el Sistema migra transacciones, THE Sistema SHALL asociar cada transacción a la cuenta de la moneda correspondiente
5. IF una cuenta tiene saldo cero en todas las monedas, THEN THE Sistema SHALL crear solo una cuenta VES por defecto

### Requirement 3: Creación de Cuentas

**User Story:** Como cliente, quiero crear cuentas específicas para cada moneda que necesite manejar, para organizar mejor mis activos.

#### Acceptance Criteria

1. WHEN un cliente crea una cuenta, THE Sistema SHALL solicitar la selección de una moneda específica
2. WHEN el Sistema crea una cuenta, THE Sistema SHALL generar un número de cuenta con prefijo identificador de moneda
3. WHEN un cliente tiene una cuenta VES, THE Sistema SHALL permitir crear cuentas adicionales en USD, EUR o USDT
4. WHERE un cliente intenta crear una cuenta, THE Sistema SHALL validar que no exista otra cuenta activa del mismo tipo de moneda
5. WHEN el Sistema crea una cuenta, THE Sistema SHALL inicializar el saldo en cero

### Requirement 4: Operaciones de Cambio de Divisas

**User Story:** Como cliente, quiero realizar operaciones de compra/venta de divisas entre mis cuentas, para intercambiar monedas de forma segura.

#### Acceptance Criteria

1. WHEN un cliente compra divisas, THE Sistema SHALL debitar de la cuenta VES y acreditar en la cuenta de la divisa comprada
2. WHEN un cliente vende divisas, THE Sistema SHALL debitar de la cuenta de la divisa vendida y acreditar en la cuenta VES
3. WHEN el Sistema procesa una transacción, THE Sistema SHALL validar que ambas cuentas pertenezcan al mismo cliente
4. WHEN el Sistema procesa una transacción, THE Sistema SHALL validar que la cuenta origen tenga saldo suficiente
5. IF una transacción falla, THEN THE Sistema SHALL revertir todos los cambios y notificar al cliente

### Requirement 5: Visualización de Cuentas

**User Story:** Como cliente, quiero ver todas mis cuentas organizadas por moneda, para tener una vista clara de mis activos.

#### Acceptance Criteria

1. WHEN un cliente accede al dashboard, THE Sistema SHALL mostrar todas sus cuentas agrupadas por moneda
2. WHEN el Sistema muestra una cuenta, THE Sistema SHALL indicar claramente la moneda asociada
3. WHEN el Sistema muestra el saldo, THE Sistema SHALL usar el formato de moneda correspondiente
4. WHEN un cliente tiene múltiples cuentas, THE Sistema SHALL mostrar un resumen consolidado en VES
5. WHERE el Sistema calcula equivalencias, THE Sistema SHALL usar las tasas de cambio actuales

### Requirement 6: Historial de Transacciones

**User Story:** Como cliente, quiero ver el historial de transacciones de cada cuenta por separado, para auditar mis movimientos por moneda.

#### Acceptance Criteria

1. WHEN un cliente consulta el historial, THE Sistema SHALL filtrar transacciones por cuenta específica
2. WHEN el Sistema muestra una transacción, THE Sistema SHALL indicar las cuentas origen y destino involucradas
3. WHEN una transacción involucra cambio de moneda, THE Sistema SHALL mostrar la tasa de cambio aplicada
4. WHEN el Sistema genera un comprobante, THE Sistema SHALL incluir los números de cuenta origen y destino
5. WHERE un cliente busca transacciones, THE Sistema SHALL permitir filtrar por cuenta y rango de fechas

### Requirement 7: Compatibilidad con Remesas

**User Story:** Como administrador, quiero que el sistema de remesas funcione correctamente con el nuevo modelo de cuentas, para mantener la funcionalidad existente.

#### Acceptance Criteria

1. WHEN el Sistema procesa una remesa, THE Sistema SHALL identificar la cuenta USD del cliente receptor
2. IF un cliente no tiene cuenta USD, THEN THE Sistema SHALL crear una automáticamente
3. WHEN el Sistema acredita una remesa, THE Sistema SHALL actualizar solo la cuenta USD correspondiente
4. WHEN el Sistema valida límites, THE Sistema SHALL considerar solo el saldo de la cuenta USD
5. WHERE existen remesas históricas, THE Sistema SHALL mantener la referencia a las cuentas correctas

### Requirement 8: Reportes y Auditoría

**User Story:** Como administrador, quiero generar reportes por moneda y por cuenta, para facilitar auditorías y análisis financieros.

#### Acceptance Criteria

1. WHEN el Sistema genera un reporte, THE Sistema SHALL permitir filtrar por moneda específica
2. WHEN el Sistema calcula totales, THE Sistema SHALL sumar solo cuentas de la misma moneda
3. WHEN el Sistema genera un reporte consolidado, THE Sistema SHALL convertir todas las monedas a VES usando tasas actuales
4. WHEN el Sistema exporta datos, THE Sistema SHALL incluir el tipo de moneda de cada cuenta
5. WHERE se requiere auditoría, THE Sistema SHALL proporcionar trazabilidad completa por cuenta

## Non-Functional Requirements

### Performance
- El Sistema SHALL procesar transacciones entre cuentas en menos de 2 segundos
- El Sistema SHALL cargar el dashboard de cuentas en menos de 3 segundos

### Security
- El Sistema SHALL validar que solo el propietario pueda acceder a sus cuentas
- El Sistema SHALL registrar todas las operaciones en el log de auditoría

### Usability
- El Sistema SHALL mantener una interfaz intuitiva similar a la actual
- El Sistema SHALL proporcionar mensajes claros sobre el tipo de cuenta

### Compatibility
- El Sistema SHALL mantener compatibilidad con la base de datos SQLite existente
- El Sistema SHALL preservar todos los datos históricos durante la migración
