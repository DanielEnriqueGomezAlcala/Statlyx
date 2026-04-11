import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptTasaGraduacion(BasePrompt):
    def build(self) -> str:
        """
        Genera el prompt para el análisis de la tasa de graduación.
        """
        return textwrap.dedent(f"""\
            <rol>
            Eres un analista experto en calidad educativa universitaria de {self.universidad}.
            </rol>

            <contexto>
            Analiza la evolución temporal de la Tasa de Graduación de la titulación "{self.titulacion}".
            La Tasa de Graduación mide el porcentaje de estudiantes de una cohorte que completan la
            titulación en el tiempo nominal previsto, siendo el indicador de eficacia terminal más
            relevante para la evaluación de la calidad de un título universitario.
            </contexto>

            <instrucciones>
            Redacta una conclusión técnica de EXACTAMENTE 3 líneas siguiendo este orden:
            1. Indica el valor máximo y mínimo con su año de cohorte, y describe la tendencia general.
            2. Señala si algún año registra una variación brusca con hipótesis breve (cambio de plan, COVID, etc.).
            3. Contextualiza si la tasa es adecuada para este tipo de titulación.
            Tono académico, directo, sin introducciones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 3 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
