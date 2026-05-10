"""Interfaz para constructor de CV."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from src.core.entities import BuilderCVConfig, DividerLine, DrawPositionsResult, LinkedInData, PersonalInformation


class CoreBuilderCV(ABC):
    """Interfaz para constructor de CV."""

    @abstractmethod
    def build_and_save(
        self,
        *,
        path_pdf: Path,
        personal_information: PersonalInformation,
        linkedin_data: LinkedInData,
        cfg_builder: Optional[BuilderCVConfig] = None,
    ) -> DrawPositionsResult:
        """Construye y guarda el CV en PDF."""
        pass

    @abstractmethod
    def draw_lines(
        self,
        *,
        path_pdf: Path,
        lines: list[DividerLine],
        color: tuple[float, float, float] = (1, 0, 0),
        width: float = 1.0,
    ) -> None:
        """Dibuja líneas adicionales en el PDF."""
        pass
