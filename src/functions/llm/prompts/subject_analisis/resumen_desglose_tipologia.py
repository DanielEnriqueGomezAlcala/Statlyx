import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptResumenDesgloseTipologia(BasePrompt):
    def build(self) -> str:
        """
        Genera el prompt para el análisis del resumen de las tasas de éxito y rendimiento por tipología.
        """
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
            1. Identifica la tipología con las tasas más altas y la de tasas más bajas en ambas métricas, citando sus valores.
            2. Contrasta la Tasa de Éxito y Tasa de Rendimiento de Formación Básica/Obligatoria frente a Optativas, y cita los valores de Prácticas Externas y TFG.
            3. Señala la mayor brecha entre Tasa de Éxito y Tasa de Rendimiento dentro de una misma tipología e indica la diferencia numérica.
            4. Indica la diferencia numérica entre la tipología con mayor y menor tasa en cada métrica.
            Tono académico, directo, sin introducciones ni conclusiones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 4 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
