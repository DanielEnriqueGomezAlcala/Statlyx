import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptTasaRendimiento(BasePrompt):
    def build(self) -> str:
        return textwrap.dedent(f"""\
            <rol>
            Eres un analista experto en calidad educativa universitaria de {self.universidad}.
            </rol>

            <contexto>
            Analiza la evolución temporal de la Tasa de Rendimiento de la titulación "{self.titulacion}".
            La Tasa de Rendimiento mide aprobados sobre el total de matriculados, capturando tanto el
            abandono como el suspenso: es el indicador más exigente y representativo del desempeño global
            del alumnado, puesto que penaliza tanto la no presentación como el fracaso en la evaluación.
            </contexto>

            <instrucciones>
            Redacta una conclusión técnica de EXACTAMENTE 5 líneas siguiendo este orden:
            1. Indica el valor máximo y mínimo registrados, con el año académico exacto de cada uno.
            2. Describe la tendencia general: mejora, deterioro o estabilidad a lo largo del periodo.
            3. Identifica años de variación brusca y propón hipótesis breves (cambio curricular, pandemia, etc.).
            4. Señala si la brecha respecto a la Tasa de Éxito es notable, interpretando esto como indicador
               de un volumen relevante de estudiantes no presentados o con abandono temprano de la materia.
            5. Tono académico, directo, sin introducciones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 5 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
