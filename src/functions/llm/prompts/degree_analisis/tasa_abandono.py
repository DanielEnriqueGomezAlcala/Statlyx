import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptTasaAbandono(BasePrompt):
    def build(self) -> str:
        return textwrap.dedent(f"""\
            <rol>
            Eres un analista experto en calidad educativa universitaria de {self.universidad}.
            </rol>

            <contexto>
            Analiza la evolución temporal de la Tasa de Abandono de la titulación "{self.titulacion}".
            La Tasa de Abandono recoge el porcentaje de estudiantes que interrumpen sus estudios sin
            completar la titulación, siendo un indicador crítico de retención y adaptación curricular.
            Una tendencia decreciente es deseable e indica mejora en la retención del alumnado.
            </contexto>

            <instrucciones>
            Redacta una conclusión técnica de EXACTAMENTE 3 líneas siguiendo este orden:
            1. Indica el valor máximo y mínimo con su año exacto, y describe la tendencia general.
            2. Identifica si algún año presenta un pico anómalo y propón una hipótesis explicativa.
            3. Valora si la tasa es preocupante e indica si requiere medidas de retención.
            Tono académico, directo, sin introducciones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 3 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
