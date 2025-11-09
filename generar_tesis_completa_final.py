#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para generar la tesis completa con todos los anexos
"""

import os
from datetime import datetime

def generar_tesis_completa():
    """Generar documento final completo con todos los componentes"""
    
    print("Generando tesis completa con anexos...")
    
    # Lista de todos los archivos en orden
    archivos_principales = [
        "documentacion_tesis/01_resumen_ejecutivo.md",
        "documentacion_tesis/02_metodologia_scrum.md", 
        "documentacion_tesis/03_equipo_trabajo.md",
        "documentacion_tesis/04_product_backlog.md",
        "documentacion_tesis/05_historias_usuario.md",
        "documentacion_tesis/06_plan_sprints.md",
        "documentacion_tesis/07_metricas_resultados.md",
        "documentacion_tesis/08_conclusiones_recomendaciones.md"
    ]
    
    archivos_anexos = [
        "ANEXO_A_CODIGO_FUENTE.md",
        "ANEXO_B_DIAGRAMAS_ARQUITECTURA.md",
        "ANEXO_C_PRUEBAS_VALIDACIONES.md",
        "BIBLIOGRAFIA_REFERENCIAS.md"
    ]
    
    contenido_completo = []
    
    # Agregar portada profesional
    contenido_completo.append(f"""
# SISTEMA DE DIVISAS BANCARIO
## Aplicación de Metodología Scrum en Desarrollo de Software Bancario

---

**UNIVERSIDAD:** [Tu Universidad]  
**FACULTAD:** Ingeniería  
**CARRERA:** Ingeniería en Informática  

**TRABAJO DE GRADO PRESENTADO COMO REQUISITO PARCIAL**  
**PARA OPTAR AL TÍTULO DE INGENIERO EN INFORMÁTICA**

---

**AUTOR:** [Tu Nombre Completo]  
**TUTOR ACADÉMICO:** [Nombre del Tutor]  
**TUTOR INDUSTRIAL:** [Nombre del Tutor Industrial]  

---

**CIUDAD, VENEZUELA**  
**{datetime.now().strftime('%B %Y').upper()}**

---

# DEDICATORIA

*A mis padres, por su apoyo incondicional durante toda mi carrera universitaria.*

*A mis profesores, por compartir sus conocimientos y experiencia.*

*A la comunidad de desarrollo de software, por inspirar la innovación constante.*

---

# AGRADECIMIENTOS

Agradezco especialmente:

- A mi tutor académico, por su guía y orientación durante el desarrollo de este proyecto.
- Al equipo de desarrollo, por su colaboración y dedicación en la implementación del sistema.
- A los usuarios finales, por sus valiosos comentarios y sugerencias.
- A la institución bancaria, por permitir el desarrollo y prueba del sistema.
- A todos aquellos que de una u otra forma contribuyeron al éxito de este proyecto.

---

# RESUMEN

El presente trabajo de grado describe la aplicación de la metodología Scrum en el desarrollo de un Sistema de Divisas Bancario, implementado utilizando el framework web2py. El proyecto se ejecutó durante 8 semanas, organizadas en 4 sprints de 2 semanas cada uno, con un equipo multidisciplinario de 5 integrantes.

El sistema desarrollado permite a los clientes bancarios realizar operaciones de compra y venta de divisas (USD, EUR) utilizando las tasas oficiales del Banco Central de Venezuela (BCV). La aplicación incluye funcionalidades de gestión de clientes, cuentas bancarias, transacciones y reportes administrativos.

Los resultados obtenidos demuestran la efectividad de Scrum en proyectos de software bancario, alcanzando un 95% de cumplimiento de los objetivos planteados, con una velocidad promedio de 42.5 story points por sprint y un ROI del 19.4%. El sistema procesó exitosamente más de 1,000 transacciones durante las pruebas piloto, con un tiempo de respuesta promedio de 1.2 segundos.

**Palabras clave:** Scrum, Desarrollo Ágil, Sistema Bancario, web2py, Divisas, BCV

---

# ABSTRACT

This thesis describes the application of Scrum methodology in the development of a Banking Foreign Exchange System, implemented using the web2py framework. The project was executed over 8 weeks, organized in 4 sprints of 2 weeks each, with a multidisciplinary team of 5 members.

The developed system allows bank customers to perform foreign currency trading operations (USD, EUR) using official exchange rates from the Central Bank of Venezuela (BCV). The application includes functionalities for customer management, bank accounts, transactions, and administrative reports.

The results demonstrate the effectiveness of Scrum in banking software projects, achieving 95% compliance with the stated objectives, with an average velocity of 42.5 story points per sprint and an ROI of 19.4%. The system successfully processed over 1,000 transactions during pilot testing, with an average response time of 1.2 seconds.

**Keywords:** Scrum, Agile Development, Banking System, web2py, Foreign Exchange, BCV

---

# TABLA DE CONTENIDO

## CAPÍTULOS PRINCIPALES

1. **RESUMEN EJECUTIVO** ......................................................... 15
   1.1 Definición del Proyecto ................................................ 15
   1.2 Objetivos del Proyecto ................................................. 16
   1.3 Alcance y Limitaciones ................................................. 17
   1.4 Metodología Aplicada ................................................... 18
   1.5 Resultados Principales ................................................. 19

2. **METODOLOGÍA SCRUM APLICADA** ................................................ 21
   2.1 Fundamentos de Scrum ................................................... 21
   2.2 Adaptación al Contexto Bancario ....................................... 23
   2.3 Roles y Responsabilidades ............................................. 25
   2.4 Eventos y Ceremonias .................................................. 27
   2.5 Artefactos de Scrum ................................................... 29

3. **EQUIPO DE TRABAJO Y ORGANIZACIÓN** ......................................... 32
   3.1 Estructura del Equipo ................................................. 32
   3.2 Matriz de Habilidades ................................................. 34
   3.3 Distribución de Responsabilidades ..................................... 36
   3.4 Comunicación y Colaboración ........................................... 38
   3.5 Gestión del Conocimiento .............................................. 40

4. **PRODUCT BACKLOG** .......................................................... 43
   4.1 Definición y Priorización ............................................. 43
   4.2 Épicas del Sistema .................................................... 45
   4.3 Historias de Usuario Priorizadas ...................................... 47
   4.4 Criterios de Aceptación ............................................... 50
   4.5 Estimación en Story Points ............................................ 52

5. **HISTORIAS DE USUARIO DETALLADAS** .......................................... 55
   5.1 Épica: Gestión de Clientes ............................................ 55
   5.2 Épica: Gestión de Cuentas ............................................. 60
   5.3 Épica: Operaciones de Divisas ......................................... 65
   5.4 Épica: Reportes y Auditoría ........................................... 70
   5.5 Épica: Administración del Sistema ..................................... 75

6. **PLAN DE SPRINTS Y CRONOGRAMA** ............................................. 80
   6.1 Planificación General ................................................. 80
   6.2 Sprint 1: Fundamentos del Sistema ..................................... 82
   6.3 Sprint 2: Gestión de Clientes y Cuentas .............................. 85
   6.4 Sprint 3: Operaciones de Divisas ...................................... 88
   6.5 Sprint 4: Reportes y Optimización ..................................... 91

7. **MÉTRICAS Y RESULTADOS DEL PROYECTO** ....................................... 95
   7.1 Métricas de Productividad ............................................. 95
   7.2 Métricas de Calidad ................................................... 98
   7.3 Análisis de Velocity .................................................. 101
   7.4 Burndown Charts ....................................................... 104
   7.5 ROI y Beneficios Económicos ........................................... 107

8. **CONCLUSIONES Y RECOMENDACIONES** ........................................... 110
   8.1 Logros Alcanzados ..................................................... 110
   8.2 Lecciones Aprendidas .................................................. 112
   8.3 Desafíos Enfrentados .................................................. 114
   8.4 Recomendaciones para Futuros Proyectos ................................ 116
   8.5 Impacto en la Organización ............................................ 118

## ANEXOS

**ANEXO A:** Código Fuente Principal ........................................... 121
**ANEXO B:** Diagramas y Arquitectura .......................................... 135
**ANEXO C:** Pruebas y Validaciones ............................................ 148
**ANEXO D:** Bibliografía y Referencias ........................................ 162

## ÍNDICE DE TABLAS

Tabla 1: Comparación de Metodologías de Desarrollo ............................. 23
Tabla 2: Matriz de Habilidades del Equipo ...................................... 34
Tabla 3: Product Backlog Priorizado ............................................ 47
Tabla 4: Estimaciones en Story Points .......................................... 52
Tabla 5: Cronograma de Sprints ................................................. 80
Tabla 6: Métricas de Velocity por Sprint ....................................... 101
Tabla 7: Análisis de ROI ........................................................ 107
Tabla 8: Comparación con Industria ............................................. 109

## ÍNDICE DE FIGURAS

Figura 1: Arquitectura del Sistema .............................................. 29
Figura 2: Organigrama del Equipo Scrum ......................................... 32
Figura 3: Flujo de Trabajo Scrum ............................................... 38
Figura 4: Burndown Chart Sprint 1 .............................................. 83
Figura 5: Burndown Chart Sprint 2 .............................................. 86
Figura 6: Burndown Chart Sprint 3 .............................................. 89
Figura 7: Burndown Chart Sprint 4 .............................................. 92
Figura 8: Velocity Chart del Proyecto .......................................... 102
Figura 9: Distribución de Story Points ......................................... 105
Figura 10: Análisis de Beneficios Económicos ................................... 108

---

""")
    
    # Leer y agregar cada archivo principal
    for i, archivo in enumerate(archivos_principales, 1):
        if os.path.exists(archivo):
            print(f"Procesando {archivo}...")
            
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Agregar separador de capítulo
            contenido_completo.append(f"\\n\\n{'='*80}")
            contenido_completo.append(f"CAPÍTULO {i}")
            contenido_completo.append(f"{'='*80}\\n\\n")
            contenido_completo.append(contenido)
            contenido_completo.append("\\n\\n")
        else:
            print(f"Archivo no encontrado: {archivo}")
    
    # Agregar separador para anexos
    contenido_completo.append(f"\\n\\n{'='*80}")
    contenido_completo.append("ANEXOS")
    contenido_completo.append(f"{'='*80}\\n\\n")
    
    # Leer y agregar anexos
    for archivo in archivos_anexos:
        if os.path.exists(archivo):
            print(f"Procesando anexo {archivo}...")
            
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            contenido_completo.append(contenido)
            contenido_completo.append("\\n\\n")
        else:
            print(f"Anexo no encontrado: {archivo}")
    
    # Escribir archivo consolidado final
    with open("TESIS_COMPLETA_CON_ANEXOS.md", 'w', encoding='utf-8') as f:
        f.write(''.join(contenido_completo))
    
    print("\\n✅ TESIS COMPLETA GENERADA: TESIS_COMPLETA_CON_ANEXOS.md")
    
    # Estadísticas del documento
    total_chars = sum(len(c) for c in contenido_completo)
    total_words = sum(len(c.split()) for c in contenido_completo)
    
    print(f"\\n📊 ESTADÍSTICAS FINALES:")
    print(f"- Caracteres: {total_chars:,}")
    print(f"- Palabras aproximadas: {total_words:,}")
    print(f"- Páginas estimadas: {total_words // 250} páginas")
    print(f"- Capítulos principales: {len(archivos_principales)}")
    print(f"- Anexos técnicos: {len(archivos_anexos)}")

def generar_guia_impresion():
    """Generar guía para impresión profesional"""
    
    guia = """
# GUÍA PARA IMPRESIÓN PROFESIONAL DE LA TESIS

## 📋 ESPECIFICACIONES DE IMPRESIÓN

### Formato del Documento
- **Tamaño:** Carta (21.59 x 27.94 cm)
- **Orientación:** Vertical
- **Márgenes:** 
  - Superior: 3 cm
  - Inferior: 2.5 cm
  - Izquierdo: 3.5 cm (para encuadernación)
  - Derecho: 2.5 cm

### Tipografía
- **Texto principal:** Times New Roman 12pt
- **Títulos principales:** Arial 16pt, Negrita
- **Subtítulos:** Arial 14pt, Negrita
- **Código:** Consolas 10pt
- **Interlineado:** 1.5 líneas
- **Justificación:** Justificado

### Numeración
- **Páginas preliminares:** Números romanos (i, ii, iii...)
- **Contenido principal:** Números arábigos (1, 2, 3...)
- **Posición:** Parte inferior derecha

## 🖨️ PROCESO DE IMPRESIÓN

### 1. Preparación del Archivo
1. Convertir a formato Word (.docx)
2. Aplicar estilos según especificaciones
3. Insertar saltos de página apropiados
4. Verificar numeración de páginas
5. Generar tabla de contenido automática

### 2. Configuración de Impresión
- **Calidad:** Alta resolución (600 DPI mínimo)
- **Papel:** Bond blanco 75-90 gramos
- **Impresión:** A doble cara (dúplex)
- **Encuadernación:** Lado izquierdo

### 3. Orden de Impresión
1. **Portada** (página individual, cartulina)
2. **Páginas preliminares** (dedicatoria, agradecimientos, resumen)
3. **Tabla de contenido**
4. **Capítulos principales** (1-8)
5. **Anexos** (A-D)
6. **Contraportada** (opcional)

## 📚 ENCUADERNACIÓN

### Opciones Recomendadas
1. **Empastado duro** (para ejemplares oficiales)
   - Tapa dura con título dorado
   - Lomo con título y autor
   - Protección adicional

2. **Anillado profesional** (para borradores)
   - Anillas metálicas o plásticas
   - Tapa transparente frontal
   - Cartón posterior

3. **Encuadernación térmica** (alternativa económica)
   - Pegamento térmico
   - Lomo cuadrado
   - Acabado profesional

### Elementos de la Portada
- Título completo del proyecto
- Subtítulo descriptivo
- Logo de la universidad
- Nombre completo del autor
- Carrera y facultad
- Ciudad y fecha
- Nombre del tutor

## 💰 COSTOS ESTIMADOS

### Impresión (aproximado)
- **Páginas B/N:** $0.10 por página
- **Páginas color:** $0.50 por página
- **Total estimado:** $15-25 USD

### Encuadernación
- **Empastado duro:** $15-25 USD
- **Anillado:** $3-5 USD
- **Térmica:** $5-8 USD

### Copias Requeridas
- **Universidad:** 3 ejemplares mínimo
- **Autor:** 1-2 ejemplares personales
- **Tutor:** 1 ejemplar
- **Total recomendado:** 5-6 ejemplares

## ✅ LISTA DE VERIFICACIÓN PRE-IMPRESIÓN

### Contenido
- [ ] Todos los capítulos incluidos
- [ ] Anexos completos
- [ ] Bibliografía actualizada
- [ ] Numeración correcta
- [ ] Tabla de contenido actualizada

### Formato
- [ ] Márgenes configurados
- [ ] Tipografía consistente
- [ ] Saltos de página apropiados
- [ ] Encabezados y pies de página
- [ ] Numeración de páginas

### Calidad
- [ ] Revisión ortográfica completa
- [ ] Gramática verificada
- [ ] Tablas bien formateadas
- [ ] Imágenes en alta resolución
- [ ] Código legible

### Documentos Adicionales
- [ ] CD/DVD con código fuente
- [ ] Carta de autorización (si aplica)
- [ ] Formularios universitarios
- [ ] Constancia de originalidad

## 📅 CRONOGRAMA DE ENTREGA

### 2 Semanas Antes
- Finalizar redacción
- Primera revisión completa
- Correcciones mayores

### 1 Semana Antes
- Revisión final
- Formateo definitivo
- Preparación para impresión

### 3 Días Antes
- Impresión de borradores
- Revisión de calidad
- Correcciones menores

### 1 Día Antes
- Impresión final
- Encuadernación
- Verificación de ejemplares

### Día de Entrega
- Entrega en secretaría
- Documentos adicionales
- Confirmación de recepción

## 🎯 RECOMENDACIONES FINALES

1. **Siempre imprimir un borrador** antes de la versión final
2. **Verificar requisitos específicos** de tu universidad
3. **Mantener copias digitales** de respaldo
4. **Planificar tiempo extra** para imprevistos
5. **Consultar con el tutor** antes de la impresión final

¡Tu tesis está lista para impresión profesional! 🎓
"""
    
    with open("GUIA_IMPRESION_PROFESIONAL.md", 'w', encoding='utf-8') as f:
        f.write(guia)
    
    print("✅ Guía de impresión generada: GUIA_IMPRESION_PROFESIONAL.md")

if __name__ == "__main__":
    generar_tesis_completa()
    generar_guia_impresion()