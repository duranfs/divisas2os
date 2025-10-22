# Sistema de Divisas Bancario

## Descripción del Producto

Sistema web bancario desarrollado en web2py para la compra y venta de divisas (VES, USD, EUR) utilizando las tasas oficiales del Banco Central de Venezuela (BCV). 

## Funcionalidades Principales

- **Gestión de Clientes**: Registro y administración de clientes bancarios con validación de cédula venezolana
- **Cuentas Bancarias**: Manejo de múltiples cuentas por cliente con saldos en tres monedas
- **Operaciones de Divisas**: Compra y venta de USD/EUR con VES usando tasas oficiales del BCV
- **Tasas en Tiempo Real**: Integración con API del BCV para obtener tasas actualizadas automáticamente
- **Historial y Reportes**: Seguimiento completo de transacciones y generación de reportes administrativos
- **Sistema de Auditoría**: Logging completo de todas las operaciones críticas del sistema

## Usuarios del Sistema

- **Clientes**: Realizan operaciones de compra/venta de divisas
- **Operadores**: Personal bancario que asiste en operaciones
- **Administradores**: Gestión completa del sistema y reportes

## Monedas Soportadas

- **VES**: Bolívar Venezolano (moneda base)
- **USD**: Dólar Estadounidense
- **EUR**: Euro

## Características Técnicas Clave

- Integración con API oficial del BCV para tasas de cambio
- Sistema de roles y permisos granular
- Generación automática de comprobantes únicos
- Validación de fondos antes de cada transacción
- Cache de tasas para optimizar rendimiento
- Responsive design para dispositivos móviles