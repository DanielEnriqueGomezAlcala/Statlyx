import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptResumenDesgloseConvocatoria(BasePrompt):
    def build(self) -> str:
        return textwrap.dedent(f"""\
            <rol>
            Eres un analista experto en calidad educativa universitaria de {self.universidad}.
            </rol>

            <contexto>
            Analiza el rendimiento académico por convocatoria de la titulación "{self.titulacion}".
            Los datos muestran la media de Tasa de Eficiencia y Tasa de Éxito por Curso.
            La Tasa de Éxito mide aprobados sobre presentados; la Tasa de Eficiencia relaciona
            los créditos superados con los créditos matriculados totales.
            Las convocatorias son: Enero (extraordinaria), Marzo, Mayo (ordinaria) y Julio (extraordinaria).
            </contexto>

            <instrucciones>
            Redacta una conclusión técnica de EXACTAMENTE 7 líneas siguiendo este orden:
            1. Identifica el curso con las tasas más bajas y más altas globalmente.
            2. Analiza si existe un patrón por curso: si los cursos iniciales muestran menor rendimiento
               que los avanzados, interpretando el primer curso como posible filtro natural de la titulación.
            3. Analiza el comportamiento entre convocatorias: compara las convocatorias ordinarias (Mayo)
               frente a las extraordinarias (Enero, Julio), indicando si las extraordinarias corrigen
               el rendimiento o siguen siendo bajas.
            4. Señala la mayor brecha entre Tasa de Eficiencia y Tasa de Éxito en algún curso,
               interpretando si ello indica un alto volumen de estudiantes no presentados o abandono de materia.
            5. Identifica si hay algún curso o grupo con comportamiento anómalo respecto al patrón general.
            6. Valora si la distribución del rendimiento entre convocatorias refleja dificultad académica
               estructural o una estrategia de presentación diferida por parte del alumnado.
            7. Mantén tono académico, directo, puramente analítico, sin introducciones ni conclusiones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 7 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
