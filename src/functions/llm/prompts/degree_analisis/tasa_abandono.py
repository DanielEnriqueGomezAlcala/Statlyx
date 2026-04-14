"""
Prompt para el análisis de la tasa de abandono a nivel de titulación.
"""

import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptTasaAbandono(BasePrompt):
    """
    Prompt para analizar la evolución temporal de la tasa de abandono.
    """

    def build(self) -> str:
        """
        Genera el prompt para el análisis de la tasa de abandono.
        """
        return textwrap.dedent(f"""\
            <rol>
            Eres un analista experto en calidad educativa universitaria de {self.universidad}.
            </rol>

            <contexto>
            Analiza la evolución temporal de la Tasa de Abandono de la titulación "{self.titulacion}".
            La Tasa de Abandono recoge el porcentaje de estudiantes que interrumpen sus estudios sin
            completar la titulación, siendo un indicador crítico de retención y adaptación curricular.
            </contexto>

            <instrucciones>
            Redacta una conclusión técnica de EXACTAMENTE 3 líneas siguiendo este orden:
            1. Indica el valor máximo y mínimo con su año exacto, y describe si la tendencia es ascendente o descendente.
            2. Identifica si algún año presenta un pico anómalo y propón una hipótesis explicativa.
            3. Indica si la tasa en el último año es mayor o menor que en el primero y describe la diferencia numérica.
            Tono académico, directo, sin introducciones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 3 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
