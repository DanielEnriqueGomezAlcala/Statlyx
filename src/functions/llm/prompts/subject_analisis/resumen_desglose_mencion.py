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
            Redacta una conclusión técnica de EXACTAMENTE 4 líneas siguiendo este orden:
            1. Identifica la mención con mejores y peores resultados globales en ambas tasas.
            2. Analiza si la elección vocacional se refleja en mejores métricas de rendimiento.
            3. Señala la mayor brecha entre Tasa de Éxito y Tasa de Rendimiento e interprétala.
            4. Evalúa si las diferencias entre menciones son sustanciales o marginales.
            Tono académico, directo, sin introducciones ni conclusiones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 4 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
