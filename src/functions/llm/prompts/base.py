from pydantic import BaseModel, field_validator


class BasePrompt(BaseModel):
    universidad: str
    titulacion: str
    datos: str

    @field_validator("universidad", "titulacion", "datos")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v

    def build(self) -> str:
        raise NotImplementedError
