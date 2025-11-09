
# ANEXO B: DIAGRAMAS Y ARQUITECTURA

## B.1 Diagrama de Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                     │
├─────────────────────────────────────────────────────────────┤
│  Bootstrap 3  │  jQuery  │  CSS Custom  │  JavaScript      │
├─────────────────────────────────────────────────────────────┤
│                    CAPA DE APLICACIÓN                       │
├─────────────────────────────────────────────────────────────┤
│  Controllers  │  Views   │  Models      │  Auth System     │
├─────────────────────────────────────────────────────────────┤
│                    FRAMEWORK WEB2PY                         │
├─────────────────────────────────────────────────────────────┤
│                    CAPA DE DATOS                            │
├─────────────────────────────────────────────────────────────┤
│  SQLite (Dev) │  PostgreSQL (Prod)  │  DAL Abstraction    │
├─────────────────────────────────────────────────────────────┤
│                    SERVICIOS EXTERNOS                       │
├─────────────────────────────────────────────────────────────┤
│  API BCV      │  BeautifulSoup      │  Requests HTTP      │
└─────────────────────────────────────────────────────────────┘
```

## B.2 Diagrama de Flujo de Transacciones

```
[Inicio] → [Login Usuario] → [Seleccionar Operación]
    │
    ├─ Compra Divisas → [Validar Fondos] → [Obtener Tasa BCV]
    │                      │                    │
    │                      ├─ Fondos OK ────────┼─ [Procesar]
    │                      │                    │
    │                      └─ Error ──────────── [Mostrar Error]
    │
    ├─ Venta Divisas → [Validar Divisas] → [Obtener Tasa BCV]
    │                     │                     │
    │                     ├─ Divisas OK ───────┼─ [Procesar]
    │                     │                     │
    │                     └─ Error ─────────── [Mostrar Error]
    │
    └─ Consultar → [Mostrar Saldos] → [Mostrar Historial]

[Procesar] → [Actualizar BD] → [Generar Comprobante] → [Fin]
```

## B.3 Modelo Entidad-Relación

```
┌─────────────────┐    1:N    ┌─────────────────┐    1:N    ┌─────────────────┐
│    CLIENTES     │◄──────────┤     CUENTAS     │◄──────────┤  TRANSACCIONES  │
├─────────────────┤           ├─────────────────┤           ├─────────────────┤
│ id (PK)         │           │ id (PK)         │           │ id (PK)         │
│ cedula (UK)     │           │ cliente_id (FK) │           │ cuenta_id (FK)  │
│ nombre          │           │ numero_cuenta   │           │ tipo_operacion  │
│ apellido        │           │ tipo_cuenta     │           │ moneda_origen   │
│ email           │           │ saldo_ves       │           │ moneda_destino  │
│ telefono        │           │ saldo_usd       │           │ monto_origen    │
│ direccion       │           │ saldo_eur       │           │ monto_destino   │
│ fecha_registro  │           │ fecha_apertura  │           │ tasa_cambio     │
│ activo          │           │ activa          │           │ comprobante     │
└─────────────────┘           └─────────────────┘           │ fecha_transac   │
                                                            │ procesada       │
                                                            └─────────────────┘
```

## B.4 Diagrama de Casos de Uso

```
                    Sistema de Divisas Bancario
    
    ┌─────────────┐                                    ┌─────────────┐
    │   Cliente   │                                    │Administrador│
    └──────┬──────┘                                    └──────┬──────┘
           │                                                  │
           │ ┌─────────────────────────────────────────────┐  │
           ├─┤ Registrarse                                 │  │
           │ └─────────────────────────────────────────────┘  │
           │ ┌─────────────────────────────────────────────┐  │
           ├─┤ Iniciar Sesión                             │  │
           │ └─────────────────────────────────────────────┘  │
           │ ┌─────────────────────────────────────────────┐  │
           ├─┤ Consultar Saldos                           │  │
           │ └─────────────────────────────────────────────┘  │
           │ ┌─────────────────────────────────────────────┐  │
           ├─┤ Comprar Divisas                            │  │
           │ └─────────────────────────────────────────────┘  │
           │ ┌─────────────────────────────────────────────┐  │
           ├─┤ Vender Divisas                             │  │
           │ └─────────────────────────────────────────────┘  │
           │ ┌─────────────────────────────────────────────┐  │
           ├─┤ Ver Historial                              │  │
           │ └─────────────────────────────────────────────┘  │
           │                                                  │
           │                                                  ├─┐
           │                                                  │ │ ┌─────────────────┐
           │                                                  │ ├─┤ Gestionar       │
           │                                                  │ │ │ Clientes        │
           │                                                  │ │ └─────────────────┘
           │                                                  │ │ ┌─────────────────┐
           │                                                  │ ├─┤ Generar         │
           │                                                  │ │ │ Reportes        │
           │                                                  │ │ └─────────────────┘
           │                                                  │ │ ┌─────────────────┐
           │                                                  │ └─┤ Configurar      │
           │                                                  │   │ Sistema         │
           │                                                  │   └─────────────────┘
           │                                                  │
    ┌──────┴──────┐                                    ┌──────┴──────┐
    │ <<include>> │                                    │ <<extend>>  │
    │ Autenticar  │                                    │ Auditoría   │
    └─────────────┘                                    └─────────────┘
```
