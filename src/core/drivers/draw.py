"""Interfaz para servicio de dibujo de CV."""

from abc import ABC, abstractmethod
from reportlab.pdfgen.canvas import Canvas

from src.core.entities import (
    BackgroundDrawCfg,
    DrawCVConfig,
    DrawPositionsResult,
    PhotoDrawCfg,
    SidebarDrawCfg,
    PositionsDrawCfg,
)


class CoreDrawCVService(ABC):
    """Interfaz para servicio de dibujo de CV."""
    
    @abstractmethod
    def draw_background(self, *, c: Canvas, cfg: BackgroundDrawCfg) -> None:
        """Dibuja el fondo del CV."""
        pass
    
    @abstractmethod
    def draw_photo(
        self,
        *,
        c: Canvas,
        cfg: PhotoDrawCfg,
        draw_config: DrawCVConfig,
    ) -> None:
        """Dibuja la foto de perfil."""
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
