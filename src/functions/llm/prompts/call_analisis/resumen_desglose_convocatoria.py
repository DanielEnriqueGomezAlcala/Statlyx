import textwrap
from functions.llm.prompts.base import BasePrompt


class PromptResumenDesgloseConvocatoria(BasePrompt):
    def build(self) -> str:
        """
        Genera el prompt para el análisis del resumen de las tasas de eficiencia y éxito por convocatoria.
        """
        return textwrap.dedent(f"""\
            <rol>
            Eres un analista experto en calidad educativa universitaria de {self.universidad}.
            </rol>

            <contexto>
            Analiza el rendimiento académico por convocatoria de la titulación "{self.titulacion}".
            Los datos muestran la media de Tasa de Eficiencia y Tasa de Éxito por Curso.
            La Tasa de Éxito mide aprobados sobre presentados; la Tasa de Eficiencia relaciona
            los créditos superados con los créditos matriculados totales.
            Las convocatorias son: Enero (extraordinaria), Marzo, Mayo (ordinaria) y Julio (extraordinaria).
            </contexto>

            <instrucciones>
            Redacta una conclusión técnica de EXACTAMENTE 4 líneas siguiendo este orden:
            1. Identifica el curso con las tasas más bajas y más altas globalmente.
            2. Compara convocatorias ordinarias (Mayo) frente a extraordinarias (Enero, Julio).
            3. Señala la mayor brecha entre Tasa de Eficiencia y Tasa de Éxito e interprétala.
            4. Valora si el patrón refleja dificultad estructural o presentación diferida del alumnado.
            Tono académico, directo, sin introducciones ni conclusiones genéricas.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente 4 líneas de texto continuo, sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
