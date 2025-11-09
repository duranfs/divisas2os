# PLAN DE SPRINTS Y CRONOGRAMA

## 1. CRONOGRAMA GENERAL DEL PROYECTO

**Duración Total:** 8 semanas (4 sprints de 2 semanas)  
**Fecha Inicio:** 1 de Octubre, 2024  
**Fecha Fin:** 26 de Noviembre, 2024  

### 1.1 Calendario de Sprints

| Sprint | Fechas | Duración | Objetivo Principal |
|--------|--------|----------|-------------------|
| **Sprint 1** | Oct 1 - Oct 14 | 2 semanas | Fundación del sistema (Auth + Clientes) |
| **Sprint 2** | Oct 15 - Oct 28 | 2 semanas | Operaciones core (Divisas + BCV) |
| **Sprint 3** | Oct 29 - Nov 11 | 2 semanas | Reportes y UX |
| **Sprint 4** | Nov 12 - Nov 26 | 2 semanas | Refinamiento y entrega |

### 1.2 Hitos Principales

- **Hito 1 (Oct 14):** Sistema básico funcional con autenticación
- **Hito 2 (Oct 28):** Operaciones de divisas implementadas
- **Hito 3 (Nov 11):** Sistema completo con reportes
- **Hito 4 (Nov 26):** Producto final listo para producción

## 2. SPRINT 1: FUNDACIÓN DEL SISTEMA

### 2.1 Objetivo del Sprint
Establecer la base del sistema con autenticación segura, gestión de usuarios y registro de clientes.

### 2.2 Sprint Backlog

| ID | Historia de Usuario | Story Points | Responsable | Estado |
|----|-------------------|--------------|-------------|---------|
| US001 | Autenticación de Administrador | 8 | Ana (FS) | ✅ Completada |
| US002 | Sistema de Roles y Permisos | 13 | Ana (FS) + Luis (BE) | ✅ Completada |
| US003 | Registro de Nuevos Clientes | 8 | Luis (BE) + Sofia (FE) | ✅ Completada |
| US004 | Creación de Cuentas Bancarias | 5 | Luis (BE) | ✅ Completada |
| US005 | Autenticación de Cliente | 5 | Sofia (FE) | ✅ Completada |
| **Total** | **5 Historias** | **39 SP** | **Todo el equipo** | **✅ Sprint Exitoso** |

### 2.3 Ceremonias del Sprint 1

#### Sprint Planning (Oct 1, 9:00-13:00)
**Participantes:** Todo el equipo Scrum  
**Duración:** 4 horas  

**Decisiones Tomadas:**
- Priorizar autenticación como base fundamental
- Ana liderará arquitectura de seguridad
- Luis se enfocará en modelos de datos
- Sofia desarrollará interfaces de login

**Capacity Planning:**
- Equipo disponible: 240 horas de desarrollo
- Velocity estimada: 35-40 SP (primer sprint)
- Buffer del 10% para adaptación del equipo

#### Daily Scrums (Oct 2-14, 9:00-9:15)
**Formato:** Presencial en sala de reuniones  
**Impedimentos Identificados:**
- Oct 3: Configuración inicial de web2py (resuelto por Ana)
- Oct 7: Definición de esquema de base de datos (resuelto en equipo)
- Oct 10: Integración de Bootstrap (resuelto por Sofia)

#### Sprint Review (Oct 14, 14:00-16:00)
**Participantes:** Equipo + Stakeholders  
**Demo Realizada:**
- ✅ Login de administrador funcional
- ✅ Registro de clientes con validaciones
- ✅ Creación automática de cuentas
- ✅ Dashboard básico por roles

**Feedback Recibido:**
- Mejorar mensajes de error en formularios
- Agregar confirmación en acciones críticas
- Considerar recordar sesión de usuario

#### Sprint Retrospective (Oct 14, 16:15-17:45)
**¿Qué funcionó bien?**
- Comunicación diaria efectiva
- Arquitectura sólida establecida por Ana
- Buena distribución de tareas

**¿Qué mejorar?**
- Definir estándares de código más temprano
- Mejorar estimaciones (fueron conservadoras)
- Establecer ambiente de testing

**Acciones para Sprint 2:**
- Crear guía de estándares de código
- Configurar ambiente de testing
- Aumentar velocity objetivo a 45 SP

### 2.4 Métricas del Sprint 1

- **Velocity Alcanzada:** 39 SP
- **Burndown:** Progreso constante, sin bloqueos mayores
- **Bugs Encontrados:** 3 (todos resueltos en el sprint)
- **Technical Debt:** Mínimo (buena arquitectura inicial)

## 3. SPRINT 2: OPERACIONES CORE

### 3.1 Objetivo del Sprint
Implementar las operaciones principales de divisas con integración al BCV y funcionalidades de consulta.

### 3.2 Sprint Backlog

| ID | Historia de Usuario | Story Points | Responsable | Estado |
|----|-------------------|--------------|-------------|---------|
| US006 | Consulta de Saldos Multi-moneda | 8 | Sofia (FE) + Luis (BE) | ✅ Completada |
| US007 | Integración con API del BCV | 13 | Luis (BE) | ✅ Completada |
| US008 | Compra de Divisas | 13 | Ana (FS) + Luis (BE) | ✅ Completada |
| US009 | Venta de Divisas | 13 | Ana (FS) + Sofia (FE) | ✅ Completada |
| **Total** | **4 Historias** | **47 SP** | **Todo el equipo** | **✅ Sprint Exitoso** |

### 3.3 Desafíos del Sprint 2

#### Integración con BCV (US007)
**Desafío:** API del BCV no siempre disponible  
**Solución:** Implementar sistema de cache con fallback  
**Tiempo Extra:** +8 horas para manejo robusto de errores  

#### Validaciones de Operaciones (US008, US009)
**Desafío:** Lógica compleja de validación de fondos  
**Solución:** Crear módulo de validaciones reutilizable  
**Refactoring:** 4 horas para optimizar código  

### 3.4 Métricas del Sprint 2

- **Velocity Alcanzada:** 47 SP (mejora del 20%)
- **Bugs Encontrados:** 5 (4 resueltos, 1 pospuesto)
- **Code Coverage:** 75% (objetivo: 80%)
- **Performance:** Operaciones < 2 segundos

## 4. SPRINT 3: REPORTES Y UX

### 4.1 Objetivo del Sprint
Completar funcionalidades de reportes, mejorar experiencia de usuario y pulir interfaces.

### 4.2 Sprint Backlog

| ID | Historia de Usuario | Story Points | Responsable | Estado |
|----|-------------------|--------------|-------------|---------|
| US010 | Visualización de Todas las Transacciones | 8 | Luis (BE) + Sofia (FE) | ✅ Completada |
| US011 | Historial Personal de Transacciones | 5 | Sofia (FE) | ✅ Completada |
| US012 | Reportes Administrativos por Período | 8 | Ana (FS) | ✅ Completada |
| US013 | Interfaz Responsive | 8 | Sofia (FE) | ✅ Completada |
| US014 | Gestión de Datos de Clientes | 5 | Luis (BE) | ✅ Completada |
| **Mejoras UX** | Refinamientos varios | 8 | Todo el equipo | ✅ Completada |
| **Total** | **6 Historias** | **42 SP** | **Todo el equipo** | **✅ Sprint Exitoso** |

### 4.3 Enfoque en UX

#### Responsive Design (US013)
- **Breakpoints:** 320px, 768px, 1024px, 1200px
- **Testing:** Chrome DevTools + dispositivos reales
- **Optimización:** Imágenes y CSS minificado

#### Mejoras de Usabilidad
- Confirmaciones en operaciones críticas
- Mensajes de error más descriptivos
- Loading indicators en operaciones lentas
- Tooltips explicativos en formularios

### 4.4 Métricas del Sprint 3

- **Velocity Alcanzada:** 42 SP
- **User Testing:** 8 usuarios probaron el sistema
- **Satisfaction Score:** 4.2/5.0
- **Mobile Compatibility:** 100% en dispositivos objetivo

## 5. SPRINT 4: REFINAMIENTO Y ENTREGA

### 5.1 Objetivo del Sprint
Pulir el sistema, resolver bugs pendientes, implementar mejoras finales y preparar entrega.

### 5.2 Sprint Backlog

| ID | Historia de Usuario | Story Points | Responsable | Estado |
|----|-------------------|--------------|-------------|---------|
| US015 | Validación de Fondos | 5 | Ana (FS) | ✅ Completada |
| US016 | Dashboard con Estadísticas | 8 | Luis (BE) + Sofia (FE) | ✅ Completada |
| US017 | Cambio de Contraseña | 3 | Sofia (FE) | ✅ Completada |
| US018 | Exportar Reportes | 5 | Ana (FS) | ✅ Completada |
| US019 | Logging de Auditoría | 8 | Luis (BE) | ✅ Completada |
| **Bug Fixes** | Correcciones pendientes | 8 | Todo el equipo | ✅ Completada |
| **Documentation** | Documentación técnica | 5 | Todo el equipo | ✅ Completada |
| **Total** | **7 Items** | **42 SP** | **Todo el equipo** | **✅ Sprint Exitoso** |

### 5.3 Actividades de Cierre

#### Testing Final
- **Regression Testing:** 40 casos de prueba ejecutados
- **Performance Testing:** Carga de 50 usuarios concurrentes
- **Security Testing:** Penetration testing básico
- **Browser Testing:** Chrome, Firefox, Safari, Edge

#### Documentación
- Manual de usuario (20 páginas)
- Documentación técnica (35 páginas)
- Guía de instalación y configuración
- Procedimientos de backup y recovery

#### Preparación para Producción
- Configuración de ambiente productivo
- Scripts de migración de datos
- Monitoreo y alertas básicas
- Plan de rollback

### 5.4 Métricas Finales del Sprint 4

- **Velocity Alcanzada:** 42 SP
- **Bugs Resueltos:** 12 (100% de bugs críticos)
- **Code Coverage:** 82%
- **Documentation Coverage:** 95%

## 6. MÉTRICAS CONSOLIDADAS DEL PROYECTO

### 6.1 Velocity del Equipo

| Sprint | Story Points Planificados | Story Points Completados | Velocity |
|--------|---------------------------|--------------------------|----------|
| Sprint 1 | 40 | 39 | 39 |
| Sprint 2 | 45 | 47 | 47 |
| Sprint 3 | 45 | 42 | 42 |
| Sprint 4 | 40 | 42 | 42 |
| **Total** | **170** | **170** | **Promedio: 42.5** |

### 6.2 Burndown Chart del Release

```
Story Points Restantes
170 |●
    |  ●
150 |    ●
    |      ●
130 |        ●
    |          ●
110 |            ●
    |              ●
90  |                ●
    |                  ●
70  |                    ●
    |                      ●
50  |                        ●
    |                          ●
30  |                            ●
    |                              ●
10  |                                ●
    |                                  ●
0   |____________________________________●
    Sprint 1    Sprint 2    Sprint 3    Sprint 4
```

### 6.3 Distribución de Esfuerzo

| Actividad | Horas | Porcentaje |
|-----------|-------|------------|
| **Desarrollo** | 640 | 51.6% |
| **Testing** | 160 | 12.9% |
| **Reuniones Scrum** | 120 | 9.7% |
| **Análisis/Diseño** | 160 | 12.9% |
| **Documentación** | 80 | 6.5% |
| **Corrección Bugs** | 80 | 6.5% |
| **Total** | **1,240** | **100%** |

### 6.4 Calidad del Producto

| Métrica | Objetivo | Alcanzado | Estado |
|---------|----------|-----------|---------|
| **Code Coverage** | 80% | 82% | ✅ Superado |
| **Bugs Críticos** | 0 | 0 | ✅ Cumplido |
| **Performance** | < 3s | < 2s | ✅ Superado |
| **User Satisfaction** | 4.0/5 | 4.2/5 | ✅ Superado |
| **Browser Compatibility** | 95% | 100% | ✅ Superado |

## 7. LECCIONES APRENDIDAS

### 7.1 Éxitos del Proyecto
- **Metodología Scrum:** Facilitó adaptación a cambios
- **Equipo Multidisciplinario:** Cobertura completa de habilidades
- **Comunicación Diaria:** Previno bloqueos mayores
- **Incrementos Funcionales:** Valor entregado desde Sprint 1

### 7.2 Desafíos Superados
- **Integración Externa:** API BCV requirió manejo robusto de errores
- **Complejidad de Validaciones:** Solucionado con arquitectura modular
- **Responsive Design:** Logrado con testing exhaustivo

### 7.3 Mejoras para Futuros Proyectos
- Establecer estándares de código desde Sprint 0
- Incluir más tiempo para testing de integración
- Considerar pair programming para módulos críticos
- Implementar CI/CD desde el inicio