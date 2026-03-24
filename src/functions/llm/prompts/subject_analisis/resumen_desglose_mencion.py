import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptResumenDesgloseMencion(BasePrompt):
    def build(self) -> str:
        return textwrap.dedent(f"""\
            <rol>
            Eres un analista experto en calidad educativa universitaria de {self.universidad}.
            </rol>

            <contexto>
            Analiza el rendimiento académico por Mención (itinerario de especialización) de la titulación
            "{self.titulacion}". Las menciones representan especialidades optativas elegidas por el alumnado
            según sus intereses. Los datos muestran la media de Tasa de Éxito y Tasa de Rendimiento por cada
            mención. La Tasa de Éxito mide aprobados sobre presentados; la de Rendimiento, aprobados sobre
            matriculados totales.
            </contexto>

            <instrucciones>
            Redacta una conclusión técnica de EXACTAMENTE 7 líneas siguiendo este orden:
            1. Identifica la mención con mejores y peores resultados globales en ambas tasas.
            2. Analiza si la elección vocacional de la especialidad se refleja en mejores métricas de rendimiento,
               valorando si el interés por la mención favorece el desempeño académico.
            3. Señala qué mención presenta la mayor brecha entre Tasa de Éxito y Tasa de Rendimiento,
               interpretando esto como la especialidad con mayor proporción de no-presentados o abandono de materia.
            4. Evalúa si las diferencias entre menciones son sustanciales o marginales, valorando la equidad
               curricular entre los diferentes itinerarios ofrecidos.
            5. Identifica si alguna mención muestra resultados anómalos que puedan requerir revisión académica
               o acciones de mejora específicas.
            6. Compara brevemente el perfil de cada mención desde la perspectiva del rendimiento global,
               señalando si alguna destaca consistentemente por encima o por debajo de la media.
            7. Mantén tono académico, directo, puramente analítico, sin introducciones ni conclusiones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 7 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
