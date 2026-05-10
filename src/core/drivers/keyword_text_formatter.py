"""Interfaz para formatear texto a partir de keywords."""

from abc import ABC, abstractmethod
from typing import List, Literal

from pydantic import BaseModel, Field


class KeywordFormat(BaseModel):
    keyword: str
    formatter: Literal["bold"] = "bold"


class KeywordsConfig(BaseModel):
    keywords: List[KeywordFormat] = Field(default_factory=list)


class CoreKeywordTextFormatter(ABC):
    @abstractmethod
    def load_keywords(self) -> KeywordsConfig:
        """Carga keywords desde la fuente configurada."""
        raise NotImplementedError

    @abstractmethod
    def format_text(self, text: str, keywords: KeywordsConfig) -> str:
        """Aplica formato al texto usando las keywords provistas."""
        raise NotImplementedError
