"""
Prompt para el análisis de la tasa de eficiencia a nivel de titulación.
"""

import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptTasaEficiencia(BasePrompt):
    """
    Prompt para analizar la evolución temporal de la tasa de eficiencia.
    """

    def build(self) -> str:
        """
        Genera el prompt para el análisis de la tasa de eficiencia.
        """
        return textwrap.dedent(f"""\
            <rol>
            Eres un analista experto en calidad educativa universitaria de {self.universidad}.
            </rol>

            <contexto>
            Analiza la evolución temporal de la Tasa de Eficiencia de la titulación "{self.titulacion}".
            La Tasa de Eficiencia relaciona los créditos teóricos necesarios para graduarse con los créditos
            realmente matriculados por los graduados, midiendo el sobrecoste académico en repeticiones.
            Un valor del 100% implica que los graduados no repitieron ningún crédito; valores inferiores
            indican que los estudiantes necesitaron matricularse en más créditos de los previstos.
            </contexto>

            <instrucciones>
            Redacta una conclusión técnica de EXACTAMENTE 3 líneas siguiendo este orden:
            1. Indica el valor máximo y mínimo con su año exacto, y describe si la eficiencia mejora o empeora.
            2. Señala si algún año presenta una variación brusca con hipótesis explicativa breve.
            3. Indica si la tasa en el último año es mayor o menor que en el primero y describe la diferencia numérica entre ambos valores.
            Tono académico, directo, sin introducciones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 3 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
