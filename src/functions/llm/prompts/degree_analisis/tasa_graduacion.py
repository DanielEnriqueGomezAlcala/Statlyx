import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptTasaGraduacion(BasePrompt):
    def build(self) -> str:
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
            Redacta una conclusión técnica de EXACTAMENTE 5 líneas siguiendo este orden:
            1. Indica el valor máximo y mínimo registrados, especificando el año de cohorte de cada uno.
            2. Describe la tendencia: si las cohortes más recientes se gradúan a mejor o peor ritmo en el plazo previsto.
            3. Señala si algún año registra una variación brusca y propón una hipótesis (cambio de plan, COVID, etc.).
            4. Contextualiza si la tasa se considera adecuada para el tipo de titulación (grado, máster, rama de conocimiento),
               indicando si se aproxima a los valores previstos en la memoria del título.
            5. Tono académico, directo, sin introducciones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 5 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
