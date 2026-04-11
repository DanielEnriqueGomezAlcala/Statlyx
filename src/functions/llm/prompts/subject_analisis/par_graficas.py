import textwrap
from typing import Optional
from functions.llm.prompts.base import BasePrompt


class PromptAnalisisPar(BasePrompt):
    contexto_grupo: str
    tasa_nombre: str
    objetivo: Optional[float] = None
    limite: Optional[float] = None

    def build(self) -> str:
        umbrales = []
        if self.objetivo is not None:
            umbrales.append(f"- Objetivo (línea verde): {self.objetivo}%")
        if self.limite is not None:
            umbrales.append(f"- Límite mínimo (línea roja): {self.limite}%")
        umbrales_str = "\n".join(umbrales) if umbrales else "No se han definido umbrales de referencia."

        hay_umbrales = bool(umbrales)
        lineas = "3" if hay_umbrales else "2"

        if hay_umbrales:
            instrucciones = (
                "1. Nombra la asignatura con el valor más alto y la más baja en el último año con sus valores exactos, "
                "indicando cuáles superan el objetivo y cuáles no alcanzan el límite.\n"
                "2. Señala una observación destacada: tendencia de mejora/caída o brecha significativa entre la mejor y la peor asignatura."
            )
        else:
            instrucciones = (
                "1. Nombra la asignatura con el valor más alto y la de valor más bajo en el último año, "
                "citando sus valores exactos y señalando una tendencia o brecha significativa destacada."
            )

        return textwrap.dedent(f"""\
            <rol>
            Eres un analista experto en calidad educativa universitaria de {self.universidad}.
            </rol>

            <contexto>
            Analiza el rendimiento de las asignaturas del grupo "{self.contexto_grupo}" de la titulación "{self.titulacion}" usando la {self.tasa_nombre}.
            Umbrales de referencia:
            {umbrales_str}
            </contexto>

            <instrucciones>
            Redacta exactamente {lineas} líneas siguiendo este orden:
            {instrucciones}
            Nunca uses introducciones, títulos ni conclusiones genéricas. Tono académico, directo, impersonal.
            </instrucciones>

            <datos>
            {self.datos}
            </datos>

            <formato_respuesta>
            Exactamente {lineas} {"línea" if lineas == "1" else "líneas"} de texto continuo. Sin numeración, sin guiones, sin encabezados.
            </formato_respuesta>
        """)
