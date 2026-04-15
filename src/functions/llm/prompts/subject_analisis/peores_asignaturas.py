"""
Prompt para el análisis de las asignaturas con peores tasas.
"""

import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptPeoresAsignaturas(BasePrompt):
    """
    Prompt para generar una conclusión y recomendaciones de mejora
    """

    def build(self) -> str:
        """
        Genera el prompt
        """
        return textwrap.dedent(f"""\
            <rol>
            Eres un analista experto en calidad educativa universitaria de {self.universidad}.
            </rol>

            <contexto>
            Analiza las asignaturas con peores resultados académicos de la titulación "{self.titulacion}".
            Los datos muestran la media histórica de Tasa de Éxito (aprobados sobre presentados)
            y Tasa de Rendimiento (aprobados sobre matriculados) de cada asignatura.
            Estas son las asignaturas con menor Tasa de Éxito media, excluyendo años sin actividad.
            </contexto>

            <instrucciones>
            Analiza los datos y genera:
            1. Un párrafo de conclusión técnica (2-3 frases) que identifique patrones comunes entre
               estas asignaturas, señale si comparten curso, cuatrimestre o tipología, e interprete
               las posibles causas del bajo rendimiento.
            2. Entre 2 y 4 recomendaciones concretas y accionables de mejora respaldadas por los datos.
            Tono académico, directo, sin introducciones ni cierres genéricos.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura, sin texto adicional:
            {{
              "conclusion": "párrafo de conclusión técnica en texto continuo",
              "recomendaciones": ["recomendación 1", "recomendación 2", "recomendación 3"]
            }}
            </formato_respuesta>
        """)
