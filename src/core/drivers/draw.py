"""Interfaz para servicio de dibujo de CV."""

from abc import ABC, abstractmethod
from reportlab.pdfgen.canvas import Canvas

from src.core.entities import (
    DrawCVConfig,
    DrawPositionsResult,
    SidebarDrawCfg,
    PositionsDrawCfg,
)
from src.core.entities.config import SizesCV
from src.core.entities.styles_config import StylesConfig


class CoreDrawCVService(ABC):
    """Interfaz para servicio de dibujo de CV."""

    @abstractmethod
    def draw_background(self, *, c: Canvas, styles_config: StylesConfig, sizes_cv: SizesCV) -> None:
        """Dibuja el fondo del CV."""
        pass
    
    @abstractmethod
    def draw_sidebar(
        self,
        *,
        c: Canvas,
        cfg: SidebarDrawCfg,
        draw_config: DrawCVConfig,
    ) -> None:
        """Dibuja la barra lateral."""
        pass
    
    @abstractmethod
    def draw_positions(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        draw_config: DrawCVConfig,
    ) -> DrawPositionsResult:
        """Dibuja las posiciones laborales."""
        pass
