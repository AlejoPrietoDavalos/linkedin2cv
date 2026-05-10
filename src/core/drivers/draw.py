"""Interfaz para servicio de dibujo de CV."""

from abc import ABC, abstractmethod
from reportlab.lib.styles import StyleSheet1
from reportlab.pdfgen.canvas import Canvas

from src.core.entities import DrawPositionsResult
from src.core.entities.config import LayoutConfig, SpacingConfig
from src.core.entities.linkedin_data import LinkedInData
from src.core.entities.personal_information import PersonalInformation
from src.core.entities.styles_config import StylesConfig


class CoreDrawCVService(ABC):
    """Interfaz para servicio de dibujo de CV."""

    @abstractmethod
    def draw_background(self, *, c: Canvas, styles_config: StylesConfig, layout_cfg: LayoutConfig) -> None:
        """Dibuja el fondo del CV."""
        pass

    @abstractmethod
    def draw_sidebar(
        self,
        *,
        c: Canvas,
        linkedin_data: LinkedInData,
        personal_information: PersonalInformation,
        layout_cfg: LayoutConfig,
        styles_config: StylesConfig,
        styles: StyleSheet1,
        spacing: SpacingConfig,
    ) -> None:
        """Dibuja la barra lateral."""
        pass

    @abstractmethod
    def draw_positions(
        self,
        *,
        c: Canvas,
        linkedin_data: LinkedInData,
        layout_cfg: LayoutConfig,
        styles: StyleSheet1,
        spacing: SpacingConfig,
    ) -> DrawPositionsResult:
        """Dibuja las posiciones laborales."""
        pass
