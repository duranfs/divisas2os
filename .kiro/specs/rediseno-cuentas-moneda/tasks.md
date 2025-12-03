# Implementation Plan - Rediseño de Cuentas por Moneda

- [x] 1. Preparar Base de Datos


  - Crear script de backup de la base de datos actual
  - Agregar columnas `moneda` y `saldo` a la tabla `cuentas`
  - Crear índices para optimizar consultas por cliente y moneda
  - _Requirements: 1.1, 2.1_

- [x] 2. Implementar Funciones de Generación de Números de Cuenta





  - [x] 2.1 Crear función `generar_numero_cuenta_por_moneda(moneda)`


    - Implementar lógica de prefijos por moneda (01=VES, 02=USD, 03=EUR, 04=USDT)
    - Generar 18 dígitos aleatorios
    - Validar unicidad del número generado
    - _Requirements: 1.5, 3.2_
  
  - [x] 2.2 Actualizar función existente `generar_numero_cuenta()`

    - Modificar para usar la nueva función con moneda por defecto VES
    - Mantener compatibilidad con código existente
    - _Requirements: 1.5_

- [x] 3. Crear Script de Migración de Datos





  - [x] 3.1 Implementar función `migrar_cuentas_a_moneda_unica()`


    - Iterar sobre todas las cuentas existentes
    - Para cada cuenta, crear cuentas separadas por moneda con saldo > 0
    - Mantener número de cuenta original para cuenta VES
    - Generar nuevos números para cuentas USD, EUR, USDT
    - _Requirements: 2.1, 2.2, 2.3_
  
  - [x] 3.2 Implementar validaciones de migración

    - Verificar que no se pierdan datos
    - Validar que los saldos totales coincidan antes y después
    - Generar reporte de migración
    - _Requirements: 2.1, 2.4_
  
  - [x] 3.3 Crear script ejecutable `migrar_cuentas.py`

    - Configurar entorno web2py
    - Ejecutar migración con confirmación del usuario
    - Generar log detallado del proceso
    - _Requirements: 2.1_

- [ ] 4. Actualizar Modelo de Datos en `models/db.py`









  - [x] 4.1 Modificar definición de tabla `cuentas`

    - Agregar campo `moneda` (string, required)
    - Agregar campo `saldo` (decimal, default=0)
    - Marcar campos antiguos como deprecated (comentar)
    - _Requirements: 1.1, 1.2_
  

  - [x] 4.2 Agregar validaciones a nivel de modelo

    - Validar que moneda sea VES, USD, EUR o USDT
    - Validar que saldo sea >= 0
    - Agregar constraint de unicidad (cliente + moneda + estado activa)
    - _Requirements: 1.1, 1.4_
  

  - [x] 4.3 Actualizar modelo de `transacciones`

    - Agregar campos `cuenta_origen_id` y `cuenta_destino_id`
    - Mantener campos de moneda para referencia
    - _Requirements: 4.1, 4.2, 6.2_
-

- [ ] 5. Actualizar Controlador de Cuentas (`controllers/cuentas.py`)




  - [x] 5.1 Modificar función `crear()`


    - Agregar selector de moneda en el formulario
    - Validar que no exista cuenta activa de esa moneda
    - Usar `generar_numero_cuenta_por_moneda()`
    - _Requirements: 3.1, 3.2, 3.4_
  
  - [x] 5.2 Modificar función `index()` (dashboard de cuentas)


    - Obtener todas las cuentas del cliente agrupadas por moneda
    - Calcular totales por moneda
    - Calcular equivalencia total en VES
    - _Requirements: 5.1, 5.2, 5.5_
  
  - [x] 5.3 Modificar función `consultar()`


    - Mostrar saldo de la cuenta específica
    - Indicar claramente la moneda de la cuenta
    - _Requirements: 5.2, 5.3_
  
  - [x] 5.4 Modificar función `movimientos()`


    - Filtrar transacciones por cuenta específica
    - Mostrar cuentas origen y destino en transacciones
    - _Requirements: 6.1, 6.2_

- [x] 6. Actualizar Controlador de Divisas (`controllers/divisas.py`)






  - [x] 6.1 Modificar función `comprar()`

    - Obtener cuenta VES del cliente
    - Obtener o crear cuenta de la divisa a comprar
    - Implementar lógica de débito/crédito entre cuentas
    - Validar saldo suficiente en cuenta VES
    - _Requirements: 4.1, 4.3, 4.4_
  

  - [x] 6.2 Modificar función `vender()`

    - Obtener cuenta de la divisa a vender
    - Obtener cuenta VES del cliente
    - Implementar lógica de débito/crédito entre cuentas
    - Validar saldo suficiente en cuenta de divisa
    - _Requirements: 4.2, 4.3, 4.4_
  


  - [x] 6.3 Actualizar función `historial_transacciones()`





    - Mostrar cuentas origen y destino
    - Permitir filtrar por cuenta específica
    - _Requirements: 6.1, 6.3_

- [x] 7. Actualizar Vistas de Cuentas




  - [x] 7.1 Modificar `views/cuentas/crear.html`


    - Agregar selector de moneda (VES, USD, EUR, USDT)
    - Mostrar información sobre el tipo de cuenta a crear
    - _Requirements: 3.1_
  
  - [x] 7.2 Modificar `views/cuentas/index.html`


    - Mostrar cuentas agrupadas por moneda
    - Indicar claramente la moneda de cada cuenta
    - Mostrar resumen consolidado en VES
    - _Requirements: 5.1, 5.2, 5.5_
  
  - [x] 7.3 Modificar `views/cuentas/detalle.html`


    - Mostrar moneda de la cuenta prominentemente
    - Usar formato de moneda correcto
    - _Requirements: 5.2, 5.3_

- [ ] 8. Actualizar Vistas de Divisas





  - [x] 8.1 Modificar `views/divisas/comprar.html`


    - Mostrar selector de cuenta VES origen
    - Mostrar cuenta destino (o indicar que se creará)
    - Actualizar calculadora para mostrar ambas cuentas
    - _Requirements: 4.1, 5.1_
  
  - [x] 8.2 Modificar `views/divisas/vender.html`


    - Mostrar selector de cuenta de divisa origen
    - Mostrar cuenta VES destino
    - Actualizar calculadora para mostrar ambas cuentas
    - _Requirements: 4.2, 5.1_
  
  - [x] 8.3 Modificar `views/divisas/historial_transacciones.html`


    - Mostrar números de cuenta origen y destino
    - Agregar filtro por cuenta
    - _Requirements: 6.1, 6.2, 6.5_

- [ ] 9. Actualizar Sistema de Remesas




  - [x] 9.1 Modificar función de recepción de remesas


    - Identificar cuenta USD del cliente receptor
    - Crear cuenta USD automáticamente si no existe
    - Acreditar solo en cuenta USD
    - _Requirements: 7.1, 7.2, 7.3_
  
  - [x] 9.2 Actualizar validación de límites


    - Considerar solo saldo de cuenta USD
    - Actualizar cálculos de límites disponibles
    - _Requirements: 7.4_

- [x] 10. Actualizar Reportes




  - [x] 10.1 Modificar reportes administrativos


    - Agregar filtro por moneda
    - Calcular totales por moneda
    - Generar reporte consolidado con conversión a VES
    - _Requirements: 8.1, 8.2, 8.3_
  
  - [x] 10.2 Actualizar exportación de datos


    - Incluir campo de moneda en exportaciones
    - Separar datos por tipo de cuenta
    - _Requirements: 8.4_

- [x] 11. Ejecutar Migración en Producción
















  - Realizar backup completo de la base de datos
  - Ejecutar script de migración `migrar_cuentas.py`
  - Validar integridad de datos migrados
  - Verificar que todas las cuentas se crearon correctamente
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_
-

- [x] 12. Pruebas de Integración





  - [x] 12.1 Probar creación de cuentas por moneda




    - Crear cuenta VES
    - Crear cuenta USD
    - Validar que no se puedan crear duplicadas
    - _Requirements: 3.1, 3.2, 3.4_
  

  - [x] 12.2 Probar operaciones de compra/venta

    - Comprar USD desde VES
    - Vender USD a VES
    - Validar saldos después de cada operación
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  


  - [x] 12.3 Probar visualización de cuentas

    - Ver dashboard con múltiples cuentas
    - Ver detalle de cada cuenta
    - Ver historial por cuenta
    - _Requirements: 5.1, 5.2, 5.3, 6.1_
  

  - [x] 12.4 Probar sistema de remesas

    - Recibir remesa en cuenta USD
    - Validar creación automática de cuenta USD
    - Verificar límites
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ] 13. Documentación y Limpieza
  - Actualizar documentación técnica
  - Actualizar manual de usuario
  - Crear guía de migración para otros ambientes
  - Eliminar código deprecated (opcional)
  - _Requirements: Todos_
