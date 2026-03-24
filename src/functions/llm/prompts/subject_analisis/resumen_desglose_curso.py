import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptResumenDesgloseCurso(BasePrompt):
    def build(self) -> str:
        return textwrap.dedent(f"""\
            <rol>
            Eres un analista experto en calidad educativa universitaria de {self.universidad}.
            </rol>

            <contexto>
            Analiza el rendimiento académico agrupado por Curso y Cuatrimestre de la titulación "{self.titulacion}".
            Los datos muestran la media de Tasa de Éxito y Tasa de Rendimiento para cada combinación de Curso
            y Cuatrimestre. La Tasa de Éxito mide aprobados sobre presentados; la de Rendimiento, aprobados
            sobre matriculados totales.
            </contexto>

            <instrucciones>
            Redacta una conclusión técnica de EXACTAMENTE 7 líneas siguiendo este orden:
            1. Identifica la combinación Curso/Cuatrimestre con las tasas más bajas y más altas globalmente.
            2. Analiza si existe un patrón por curso: si los cursos iniciales muestran menor rendimiento que los avanzados,
               interpretando el primer curso como posible filtro natural de la titulación.
            3. Analiza si existe un patrón por cuatrimestre: si el primero resulta sistemáticamente más exigente que el segundo.
            4. Señala la mayor brecha entre Tasa de Éxito y Tasa de Rendimiento en algún curso/cuatrimestre,
               interpretando si ello indica un alto volumen de estudiantes no presentados o abandono de materia.
            5. Identifica si hay alguna combinación con comportamiento anómalo respecto al patrón general.
            6. Valora si la progresión a lo largo de los cursos refleja una selección natural o una mejora progresiva
               de competencias a medida que el alumnado avanza en la titulación.
            7. Mantén tono académico, directo, puramente analítico, sin introducciones ni conclusiones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 7 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
