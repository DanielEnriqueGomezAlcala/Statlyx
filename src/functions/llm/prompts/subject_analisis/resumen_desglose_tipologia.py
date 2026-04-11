import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptResumenDesgloseTipologia(BasePrompt):
    def build(self) -> str:
        return textwrap.dedent(f"""\
            <rol>
            Eres un analista experto en calidad educativa universitaria de {self.universidad}.
            </rol>

            <contexto>
            Analiza el rendimiento académico por Tipología de asignatura en la titulación "{self.titulacion}".
            Las tipologías contempladas son: Formación Básica, Obligatoria, Optativa, Prácticas Externas y
            Trabajo Fin de Grado. Los datos muestran la media de Tasa de Éxito y Tasa de Rendimiento por
            cada tipología. La Tasa de Éxito mide aprobados sobre presentados; la de Rendimiento, aprobados
            sobre matriculados totales.
            </contexto>

            <instrucciones>
            Redacta una conclusión técnica de EXACTAMENTE 4 líneas siguiendo este orden:
            1. Identifica la tipología con mejores y peores resultados globales en ambas tasas.
            2. Contrasta Formación Básica/Obligatoria frente a Optativas, e interpreta Prácticas Externas y TFG.
            3. Señala la mayor brecha entre Tasa de Éxito y Tasa de Rendimiento por tipología e interprétala.
            4. Valora si la distribución refleja un diseño curricular equilibrado.
            Tono académico, directo, sin introducciones ni conclusiones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 4 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
