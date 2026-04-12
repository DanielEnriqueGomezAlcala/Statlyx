import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptResumenDesgloseMencion(BasePrompt):
    def build(self) -> str:
        """
        Genera el prompt para el análisis del resumen de las tasas de éxito y rendimiento por mención.
        """
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
            1. Identifica la mención con las tasas más altas y la de tasas más bajas en ambas métricas, citando sus valores.
            2. Describe si las menciones con las tasas más altas coinciden o difieren de las que tienen las tasas más bajas en cada métrica.
            3. Señala la mayor brecha entre Tasa de Éxito y Tasa de Rendimiento e indica la diferencia numérica.
            4. Indica la diferencia numérica entre la mención con mayor y menor tasa en cada métrica.
            Tono académico, directo, sin introducciones ni conclusiones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 4 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
