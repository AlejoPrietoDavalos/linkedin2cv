"""Modelos y contrato para la carga de fuentes."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel


class PairNamePathFont(BaseModel):
    name: str
    path: Optional[Path]
    font_type: Literal["family", "normal", "bold", "italic", "boldItalic"]


class FontLoaderConfig(BaseModel):
    base_name: Literal["HackNerdFont"]


class CoreFontLoader(ABC):
    """Interfaz para cargar fuentes requeridas por el sistema."""

    @abstractmethod
    def load_font_from_env(self) -> str:
        """Carga las fuentes definidas en la configuración."""
        pass
