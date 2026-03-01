from string import Template

plantilla_resumen_tipologia = Template("""
Actúa como un analista experto en calidad educativa de la $universidad. 
Tu tarea es analizar el siguiente dataset de la titulación "$titulacion" y redactar una conclusión técnica de EXACTAMENTE 7 líneas.

Contexto del gráfico:
- La "Tasa de Éxito" mide aprobados sobre presentados.
- La "Tasa de Rendimiento" mide aprobados sobre matriculados totales.

Instrucciones de redacción:
1. Compara el desempeño entre los tipos de asignaturas.
2. Identifica cuál tipología presenta mayor brecha entre éxito y rendimiento.
3. Propón una interpretación de por qué las optativas suelen tener tasas más altas (ej. motivación, especialización).
4. Mantén un tono académico, directo y sin introducciones innecesarias.

Datos para analizar:
$datos
""")