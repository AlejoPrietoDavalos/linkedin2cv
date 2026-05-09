"""Interfaz para constructor de CV."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from src.core.entities import BuilderCVConfig, LinkedinData, PersonalInformation, SizesCV, StyleCV


class CoreBuilderCV(ABC):
    """Interfaz para constructor de CV."""
    
    @abstractmethod
    def build_and_save(
        self,
        *,
        path_pdf: Path,
        personal_information: PersonalInformation,
        linkedin_data: LinkedinData,
        style_cv: Optional[StyleCV] = None,
        sizes_cv: Optional[SizesCV] = None,
        cfg_builder: Optional[BuilderCVConfig] = None,
    ) -> None:
        """Construye y guarda el CV en PDF."""
        pass
    
    @abstractmethod
    def draw_lines(
        self,
        *,
        path_pdf: Path,
        color: tuple[float, float, float] = (1, 0, 0),
        width: float = 1.0,
    ) -> None:
        """Dibuja líneas adicionales en el PDF."""
        pass
