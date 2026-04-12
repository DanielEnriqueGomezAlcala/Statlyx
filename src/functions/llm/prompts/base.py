"""
Modelo base para los prompts del LLM.
"""

from pydantic import BaseModel, field_validator


class BasePrompt(BaseModel):
    """
    Clase base de la que heredan todos los prompts.
    """

    universidad: str
    titulacion: str
    datos: str

    @field_validator("universidad", "titulacion", "datos")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        """
        Valida que los campos no estén vacíos.
        """
        if not v or not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v

    def build(self) -> str:
        """
        Construye el texto del prompt. Debe implementarse en cada subclase.
        """
        raise NotImplementedError
