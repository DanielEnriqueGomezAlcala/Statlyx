import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptResumenDesgloseTipologia(BasePrompt):
    def build(self) -> str:
        return textwrap.dedent(f"""\
            <rol>
            Eres un analista experto en calidad educativa universitaria de {self.universidad}.
            </rol>

            <contexto>
            Analiza el rendimiento académico por Tipología de asignatura en la titulación "{self.titulacion}".
            Las tipologías contempladas son: Formación Básica, Obligatoria, Optativa, Prácticas Externas y
            Trabajo Fin de Grado. Los datos muestran la media de Tasa de Éxito y Tasa de Rendimiento por
            cada tipología. La Tasa de Éxito mide aprobados sobre presentados; la de Rendimiento, aprobados
            sobre matriculados totales.
            </contexto>

            <instrucciones>
            Redacta una conclusión técnica de EXACTAMENTE 7 líneas siguiendo este orden:
            1. Identifica la tipología con mejores y peores resultados globales en ambas tasas.
            2. Contrasta el desempeño entre Formación Básica y Obligatoria frente a las Optativas,
               argumentando si la diferencia responde a mayor motivación o especialización del alumnado.
            3. Interpreta los resultados de Prácticas Externas y TFG en términos de su naturaleza evaluativa
               diferenciada respecto al resto de tipologías.
            4. Señala la mayor brecha entre Tasa de Éxito y Tasa de Rendimiento por tipología,
               vinculándola con el volumen de estudiantes no presentados o abandono de esa categoría.
            5. Identifica si alguna tipología muestra un comportamiento anómalo respecto al patrón esperado.
            6. Valora si la distribución del rendimiento entre tipologías refleja un diseño curricular equilibrado
               que facilita la adquisición progresiva de competencias.
            7. Mantén tono académico, directo, puramente analítico, sin introducciones ni conclusiones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 7 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
