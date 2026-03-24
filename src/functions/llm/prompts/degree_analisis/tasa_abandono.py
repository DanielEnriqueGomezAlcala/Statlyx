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
            Redacta una conclusión técnica de EXACTAMENTE 5 líneas siguiendo este orden:
            1. Indica el valor máximo y mínimo registrado, con el año académico exacto de cada uno.
            2. Describe la tendencia general: si el abandono aumenta, disminuye o se estabiliza a lo largo del periodo.
            3. Identifica si algún año presenta un pico anómalo de abandono y propón una hipótesis explicativa.
            4. Valora si la tasa se sitúa en niveles preocupantes para el tipo de titulación analizado,
               indicando si requiere medidas de retención o si los valores son aceptables.
            5. Tono académico, directo, sin introducciones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 5 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
