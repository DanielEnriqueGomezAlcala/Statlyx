import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptTasaExito(BasePrompt):
    def build(self) -> str:
        """
        Genera el prompt para el análisis de la tasa de éxito.
        """
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
            Redacta una conclusión técnica de EXACTAMENTE 3 líneas siguiendo este orden:
            1. Indica el valor máximo y mínimo registrados con su año académico exacto, y describe la tendencia general.
            2. Señala si existe algún año con variación brusca e interpreta la causa probable.
            3. Indica si la tasa en el último año es mayor o menor que en el primero y describe la diferencia numérica entre ambos valores.
            Tono académico, directo, sin introducciones ni conclusiones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 3 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
