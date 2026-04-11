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
            Redacta una conclusión técnica de EXACTAMENTE 3 líneas siguiendo este orden:
            1. Indica el valor máximo y mínimo con su año exacto, y describe la tendencia general.
            2. Identifica años de variación brusca con hipótesis breve (cambio curricular, pandemia, etc.).
            3. Señala si la brecha respecto a la Tasa de Éxito es notable e interprétala.
            Tono académico, directo, sin introducciones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 3 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
