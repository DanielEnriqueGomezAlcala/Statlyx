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
            Redacta una conclusión técnica de EXACTAMENTE 4 líneas siguiendo este orden:
            1. Identifica la combinación Curso/Cuatrimestre con las tasas más bajas y más altas globalmente.
            2. Analiza si existe un patrón por curso o cuatrimestre destacable.
            3. Señala la mayor brecha entre Tasa de Éxito y Tasa de Rendimiento e interprétala.
            4. Valora si la progresión refleja una selección natural o mejora progresiva de competencias.
            Tono académico, directo, sin introducciones ni conclusiones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 4 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
