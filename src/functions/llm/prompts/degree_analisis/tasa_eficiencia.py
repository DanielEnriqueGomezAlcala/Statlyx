import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptTasaEficiencia(BasePrompt):
    def build(self) -> str:
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
            Redacta una conclusión técnica de EXACTAMENTE 5 líneas siguiendo este orden:
            1. Indica el valor máximo y mínimo registrados, con el año académico exacto de cada uno.
            2. Describe si la eficiencia mejora o empeora: si los graduados más recientes repiten menos créditos.
            3. Señala si algún año presenta una caída o subida brusca y propón una hipótesis explicativa.
            4. Interpreta si el nivel de eficiencia es coherente con la dificultad esperada de la titulación,
               valorando el impacto del sobrecoste académico en los graduados.
            5. Tono académico, directo, sin introducciones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 5 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
