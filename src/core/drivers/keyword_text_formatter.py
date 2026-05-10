"""Interfaz para formatear texto a partir de keywords."""

from abc import ABC, abstractmethod
from typing import List, Literal

from pydantic import BaseModel, Field

_KeywordFormatter = Literal["bold"]

class KeywordFormat(BaseModel):
    keyword: str
    formatter: _KeywordFormatter = "bold"


class KeywordsConfig(BaseModel):
    keywords: List[KeywordFormat] = Field(default_factory=list)


class CoreKeywordTextFormatter(ABC):
    @abstractmethod
    def load_keywords(self) -> KeywordsConfig:
        """Carga keywords desde la fuente configurada."""
        ...

    @abstractmethod
    def format_text(self, text: str, keywords: KeywordsConfig) -> str:
        """Aplica formato al texto usando las keywords provistas."""
        ...

    @abstractmethod
    def format_bracketed(self, text: str, formatter: _KeywordFormatter) -> str:
        """Aplica formato a bloques entre corchetes, p. ej. [texto]."""
        ...
