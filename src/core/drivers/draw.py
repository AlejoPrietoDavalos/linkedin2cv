"""Interfaz para servicio de dibujo de CV."""

from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from pathlib import Path

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import StyleSheet1

from src.core.entities import LinkedinData, StyleCV, SizesCV, DrawCVConfig


class CoreDrawCVService(ABC):
    """Interfaz para servicio de dibujo de CV."""
    
    @abstractmethod
    def draw_background(self, *, c: Canvas, color, page_width: int, page_height: int) -> None:
        """Dibuja el fondo del CV."""
        pass
    
    @abstractmethod
    def draw_photo(
        self,
        *,
        c: Canvas,
        path_photo: Optional[Path],
        sizes_cv: SizesCV,
        page_height: int,
        is_photo_circle: bool = False,
    ) -> None:
        """Dibuja la foto de perfil."""
        pass
    
    @abstractmethod
    def draw_sidebar(
        self,
        *,
        c: Canvas,
        linkedin_data: LinkedinData,
        sizes_cv: SizesCV,
        style_cv: StyleCV,
        styles: StyleSheet1,
        age: int,
        location: str,
        mail: str,
        page_height: int,
        url_website_es: str,
        url_website_en: str,
        url_github: str,
        url_linkedin: str,
    ) -> None:
        """Dibuja la barra lateral."""
        pass
    
    @abstractmethod
    def draw_positions(
        self,
        *,
        c: Canvas,
        linkedin_data: LinkedinData,
        sizes_cv: SizesCV,
        style_cv: StyleCV,
        styles: StyleSheet1,
        page_width: int,
        page_height: int,
        sidebar_args: dict,
    ) -> Tuple[List[Tuple[float, float, float, float]], int]:
        """Dibuja las posiciones laborales."""
        pass
