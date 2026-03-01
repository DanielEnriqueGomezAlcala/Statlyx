from string import Template

plantilla_resumen_curso_cuatrimestre = Template("""
Actúa como un analista experto en calidad educativa de la $universidad. 
Tu tarea es analizar el siguiente dataset de la titulación "$titulacion" y redactar una conclusión técnica de EXACTAMENTE 7 líneas.

Contexto del gráfico:
- El análisis muestra la evolución temporal por Curso Académico y Cuatrimestre.
- La "Tasa de Éxito" mide aprobados sobre presentados a evaluación.
- La "Tasa de Rendimiento" mide aprobados sobre matriculados totales.

Instrucciones de redacción:
1. Analiza la tendencia general de las tasas a medida que el estudiante avanza de curso (ej. ¿actúa el primer año como filtro natural?).
2. Compara el desempeño entre los distintos cuatrimestres, señalando si históricamente el primero o el segundo suelen presentar mayor dificultad.
3. Identifica el periodo exacto (Curso y Cuatrimestre) con la mayor brecha entre éxito y rendimiento, y justifica brevemente si esto sugiere una alta tasa de abandono o "no presentados".
4. Mantén un tono académico, directo, puramente analítico y sin introducciones ni conclusiones genéricas.

Datos para analizar:
$datos
""")

plantilla_resumen_itinerarios = Template("""
Actúa como un analista experto en calidad educativa de la $universidad. 
Tu tarea es analizar el siguiente dataset de la titulación "$titulacion" y redactar una conclusión técnica de EXACTAMENTE 7 líneas.

Contexto del gráfico:
- El análisis compara las tasas académicas según los distintos Itinerarios (menciones o especialidades) elegidos por los estudiantes.
- La "Tasa de Éxito" mide aprobados sobre presentados.
- La "Tasa de Rendimiento" mide aprobados sobre matriculados totales.

Instrucciones de redacción:
1. Compara el desempeño general entre los diferentes itinerarios para identificar si alguna especialidad resulta académicamente más exigente o más accesible.
2. Señala qué itinerario presenta las mejores métricas de éxito y rendimiento, valorando brevemente si la elección vocacional de la especialidad influye en estas cifras.
3. Identifica el itinerario con la mayor brecha entre la tasa de éxito y la de rendimiento, interpretando esto como la especialidad con mayor índice de abandono o estudiantes "no presentados".
4. Mantén un tono académico, directo, puramente analítico y sin introducciones ni conclusiones genéricas.

Datos para analizar:
$datos
""")

plantilla_resumen_tipologia = Template("""
Actúa como un analista experto en calidad educativa de la $universidad. 
Tu tarea es analizar el siguiente dataset de la titulación "$titulacion" y redactar una conclusión técnica de EXACTAMENTE 7 líneas.

Contexto del gráfico:
- El análisis compara las métricas académicas globales según la Tipología de las asignaturas (ej. Formación Básica, Obligatoria, Optativa, Prácticas).
- La "Tasa de Éxito" mide aprobados sobre presentados.
- La "Tasa de Rendimiento" mide aprobados sobre matriculados totales.

Instrucciones de redacción:
1. Compara el desempeño general entre las diferentes tipologías, destacando el contraste habitual entre las materias de Formación Básica/Obligatorias y las Optativas.
2. Argumenta brevemente si los altos valores en tipologías específicas (como Optativas o Prácticas) responden a una mayor motivación, especialización o madurez del alumnado.
3. Identifica la tipología que presenta la mayor brecha entre la tasa de éxito y la de rendimiento, vinculando este dato con el volumen de estudiantes "no presentados" o abandono de la materia.
4. Mantén un tono académico, directo, puramente analítico y sin introducciones ni conclusiones genéricas.

Datos para analizar:
$datos
""")