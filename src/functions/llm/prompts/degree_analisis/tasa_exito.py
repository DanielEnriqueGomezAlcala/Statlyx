import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptTasaExito(BasePrompt):
    def build(self) -> str:
        return textwrap.dedent(f"""\
            <rol>
            Eres un analista experto en calidad educativa universitaria de {self.universidad}.
            </rol>

            <contexto>
            Analiza la evolución temporal de la Tasa de Éxito de la titulación "{self.titulacion}".
            La Tasa de Éxito mide la proporción de estudiantes aprobados sobre el total de presentados
            a evaluación. Un valor alto indica que quienes se presentan superan la materia, pero no
            refleja el abandono o la no presentación previos.
            </contexto>

            <instrucciones>
            Redacta una conclusión técnica de EXACTAMENTE 5 líneas siguiendo este orden:
            1. Indica el valor máximo y mínimo registrados, especificando el año académico exacto de cada uno.
            2. Describe la tendencia general: si la tasa mejora, empeora o permanece estable a lo largo del periodo.
            3. Señala si existe algún año con variación brusca (subida o bajada notable) e interpreta la causa probable.
            4. Evalúa si los niveles de éxito son coherentes con los estándares esperados para esta titulación.
            5. Mantén tono académico, directo y puramente analítico. Sin introducciones ni conclusiones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 5 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
