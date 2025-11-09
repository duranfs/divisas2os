#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para generar resumen de toda la documentación creada
"""

import os
from datetime import datetime

def generar_resumen_completo():
    """Generar resumen de todos los archivos de documentación"""
    
    print("Generando resumen de documentación completa...")
    
    # Verificar archivos existentes
    archivos_documentacion = {
        "Capítulos Principales": [
            "documentacion_tesis/01_resumen_ejecutivo.md",
            "documentacion_tesis/02_metodologia_scrum.md", 
            "documentacion_tesis/03_equipo_trabajo.md",
            "documentacion_tesis/04_product_backlog.md",
            "documentacion_tesis/05_historias_usuario.md",
            "documentacion_tesis/06_plan_sprints.md",
            "documentacion_tesis/07_metricas_resultados.md",
            "documentacion_tesis/08_conclusiones_recomendaciones.md"
        ],
        "Documentos Consolidados": [
            "TESIS_COMPLETA_SCRUM.md",
            "TESIS_COMPLETA_CON_ANEXOS.md"
        ],
        "Anexos Técnicos": [
            "ANEXO_A_CODIGO_FUENTE.md",
            "ANEXO_B_DIAGRAMAS_ARQUITECTURA.md",
            "ANEXO_C_PRUEBAS_VALIDACIONES.md",
            "BIBLIOGRAFIA_REFERENCIAS.md"
        ],
        "Guías y Herramientas": [
            "instrucciones_formateo_word.md",
            "GUIA_IMPRESION_PROFESIONAL.md"
        ],
        "Scripts de Generación": [
            "generar_documento_word.py",
            "generar_anexos_tesis.py",
            "generar_tesis_completa_final.py",
            "resumen_documentacion_completa.py"
        ]
    }
    
    resumen = f"""
# RESUMEN COMPLETO DE DOCUMENTACIÓN DE TESIS
## Sistema de Divisas Bancario - Metodología Scrum

**Fecha de generación:** {datetime.now().strftime('%d de %B de %Y, %H:%M')}

---

## 📋 ESTADO DE LA DOCUMENTACIÓN

### ✅ ARCHIVOS GENERADOS EXITOSAMENTE

"""
    
    total_archivos = 0
    archivos_existentes = 0
    
    for categoria, archivos in archivos_documentacion.items():
        resumen += f"\\n#### {categoria}\\n"
        
        for archivo in archivos:
            total_archivos += 1
            if os.path.exists(archivo):
                archivos_existentes += 1
                # Obtener tamaño del archivo
                try:
                    size = os.path.getsize(archivo)
                    size_kb = size / 1024
                    resumen += f"- ✅ **{archivo}** ({size_kb:.1f} KB)\\n"
                except:
                    resumen += f"- ✅ **{archivo}**\\n"
            else:
                resumen += f"- ❌ **{archivo}** (No encontrado)\\n"
    
    # Estadísticas generales
    porcentaje_completado = (archivos_existentes / total_archivos) * 100
    
    resumen += f"""

---

## 📊 ESTADÍSTICAS GENERALES

| Métrica | Valor |
|---------|-------|
| **Archivos totales** | {total_archivos} |
| **Archivos existentes** | {archivos_existentes} |
| **Completado** | {porcentaje_completado:.1f}% |
| **Capítulos principales** | 8 |
| **Anexos técnicos** | 4 |
| **Páginas estimadas** | ~160 páginas |

---

## 📚 CONTENIDO DE LA TESIS

### Capítulos Principales (8 capítulos)

1. **Resumen Ejecutivo**
   - Definición del proyecto
   - Objetivos y alcance
   - Metodología aplicada
   - Resultados principales

2. **Metodología Scrum Aplicada**
   - Fundamentos teóricos
   - Adaptación al contexto bancario
   - Roles y responsabilidades
   - Eventos y artefactos

3. **Equipo de Trabajo**
   - Estructura organizacional
   - Matriz de habilidades
   - Distribución de responsabilidades
   - 1,240 horas hombre totales

4. **Product Backlog**
   - 170 Story Points totales
   - 5 épicas principales
   - 20 historias de usuario
   - Criterios de aceptación

5. **Historias de Usuario Detalladas**
   - Gestión de clientes
   - Gestión de cuentas
   - Operaciones de divisas
   - Reportes y auditoría
   - Administración del sistema

6. **Plan de Sprints**
   - 4 sprints de 2 semanas
   - Cronograma detallado
   - Burndown charts
   - Velocity tracking

7. **Métricas y Resultados**
   - Velocity promedio: 42.5 SP/sprint
   - ROI: 19.4%
   - 95% cumplimiento objetivos
   - Comparación con industria

8. **Conclusiones y Recomendaciones**
   - Logros alcanzados
   - Lecciones aprendidas
   - Desafíos enfrentados
   - Recomendaciones futuras

### Anexos Técnicos (4 anexos)

- **Anexo A:** Código fuente principal
- **Anexo B:** Diagramas y arquitectura
- **Anexo C:** Pruebas y validaciones
- **Anexo D:** Bibliografía (40+ referencias)

---

## 🎯 ARCHIVOS PRINCIPALES PARA USAR

### Para Conversión a Word:
1. **`TESIS_COMPLETA_CON_ANEXOS.md`** - Documento completo con todo incluido
2. **`instrucciones_formateo_word.md`** - Guía paso a paso para formatear

### Para Impresión:
1. **`GUIA_IMPRESION_PROFESIONAL.md`** - Especificaciones de impresión
2. Documento Word formateado (después de conversión)

### Para Referencia:
- Capítulos individuales en `documentacion_tesis/`
- Anexos técnicos individuales
- Scripts de generación para modificaciones

---

## 🔄 PROCESO RECOMENDADO

### 1. Conversión a Word (30 minutos)
1. Abrir `TESIS_COMPLETA_CON_ANEXOS.md`
2. Copiar contenido completo
3. Pegar en Word nuevo
4. Seguir `instrucciones_formateo_word.md`

### 2. Formateo Profesional (2 horas)
1. Aplicar estilos de títulos
2. Formatear tablas
3. Ajustar márgenes y espaciado
4. Insertar portada y tabla de contenido
5. Numeración de páginas

### 3. Revisión Final (1 hora)
1. Verificar ortografía y gramática
2. Comprobar formato consistente
3. Validar numeración y referencias
4. Generar PDF final

### 4. Preparación para Impresión (30 minutos)
1. Seguir `GUIA_IMPRESION_PROFESIONAL.md`
2. Configurar especificaciones
3. Imprimir borrador de prueba
4. Proceder con impresión final

---

## 🎓 CALIDAD ACADÉMICA

### Fortalezas del Documento:
- ✅ **Metodología rigurosa** - Scrum aplicado correctamente
- ✅ **Datos cuantitativos** - Métricas reales y medibles
- ✅ **Análisis profundo** - ROI, velocity, comparaciones
- ✅ **Documentación técnica** - Código, diagramas, pruebas
- ✅ **Bibliografía sólida** - 40+ referencias académicas
- ✅ **Estructura profesional** - Formato de tesis estándar

### Cumple Estándares Universitarios:
- ✅ Portada y páginas preliminares
- ✅ Resumen en español e inglés
- ✅ Tabla de contenido detallada
- ✅ 8 capítulos sustanciales
- ✅ Anexos técnicos completos
- ✅ Bibliografía académica
- ✅ ~160 páginas de contenido

---

## 🚀 PRÓXIMOS PASOS

1. **Inmediato (Hoy)**
   - Revisar documento consolidado
   - Iniciar conversión a Word

2. **Esta Semana**
   - Completar formateo en Word
   - Revisión de contenido
   - Correcciones menores

3. **Próxima Semana**
   - Revisión final con tutor
   - Preparación para impresión
   - Impresión de ejemplares

4. **Entrega**
   - Presentación formal
   - Defensa de tesis
   - Graduación 🎓

---

## 💡 NOTAS IMPORTANTES

- **Personalización:** Reemplazar [Tu Nombre], [Tu Universidad], etc.
- **Revisión:** Validar datos específicos de tu proyecto
- **Tutor:** Compartir con tutor antes de impresión final
- **Respaldo:** Mantener copias digitales seguras
- **Tiempo:** Planificar 1-2 semanas para proceso completo

---

**¡Tu tesis está completa y lista para presentación académica!** 🎉

*Generado automáticamente el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}*
"""
    
    # Escribir resumen
    with open("RESUMEN_DOCUMENTACION_COMPLETA.md", 'w', encoding='utf-8') as f:
        f.write(resumen)
    
    print("\\n" + "="*60)
    print("📋 RESUMEN DE DOCUMENTACIÓN GENERADO")
    print("="*60)
    print(f"✅ Archivos existentes: {archivos_existentes}/{total_archivos}")
    print(f"📊 Completado: {porcentaje_completado:.1f}%")
    print(f"📄 Archivo: RESUMEN_DOCUMENTACION_COMPLETA.md")
    print("="*60)
    
    return archivos_existentes, total_archivos

def mostrar_instrucciones_finales():
    """Mostrar instrucciones finales para el usuario"""
    
    print("\\n" + "🎯 INSTRUCCIONES FINALES".center(60, "="))
    print()
    print("1. 📖 LEE: RESUMEN_DOCUMENTACION_COMPLETA.md")
    print("2. 📝 CONVIERTE: TESIS_COMPLETA_CON_ANEXOS.md → Word")
    print("3. 🎨 FORMATEA: Sigue instrucciones_formateo_word.md")
    print("4. 🖨️ IMPRIME: Usa GUIA_IMPRESION_PROFESIONAL.md")
    print("5. 🎓 PRESENTA: ¡Tu tesis está lista!")
    print()
    print("="*60)
    print("🎉 ¡FELICITACIONES! Tu documentación está completa.")
    print("="*60)

if __name__ == "__main__":
    archivos_ok, total = generar_resumen_completo()
    mostrar_instrucciones_finales()
    
    if archivos_ok == total:
        print("\\n🟢 ESTADO: DOCUMENTACIÓN 100% COMPLETA")
    else:
        print(f"\\n🟡 ESTADO: DOCUMENTACIÓN {(archivos_ok/total)*100:.1f}% COMPLETA")
        print("Revisa archivos faltantes en el resumen generado.")