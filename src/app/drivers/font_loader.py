"""Adaptador de carga de fuentes para la capa de aplicación."""

import os
import logging
from typing import List
from pathlib import Path
from enum import Enum

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

from src.core.constants import PATH_FONTS
from src.core.drivers.font_loader import CoreFontLoader, FontLoaderConfig, PairNamePathFont

logger = logging.getLogger(__name__)

class FontType(Enum):
    FAMILY = "family"
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    BOLD_ITALIC = "boldItalic"


class FontLoader(CoreFontLoader):
    """Carga fuentes usando la configuración central del core."""
    def __init__(self):
        super().__init__()
        self._font_name: str = None
        self._path_font_folder: Path = None

    @property
    def font_name(self) -> str:
        if self._font_name is None:
            self._font_name = os.getenv("FONT_NAME")
        if not self._font_name:
            raise ValueError("FONT_NAME environment variable is required")
        return self._font_name

    @property
    def path_font_folder(self) -> Path:
        if self._path_font_folder is None:
            self._path_font_folder = PATH_FONTS / self.font_name
        return self._path_font_folder

    def load_font_from_env(self) -> None:
        logger.info(f"==================== Font Loader ====================")
        logger.info(f">>>>> Font folder: {self.path_font_folder}")
        self._load_fonts(FontLoaderConfig(base_name=self.font_name))

    def _load_fonts(self, cfg: FontLoaderConfig) -> None:
        self._register_font_family(cfg)

    def _font_pairs(self, cfg: FontLoaderConfig) -> List[PairNamePathFont]:
        return [
            PairNamePathFont(
                name=cfg.base_name,
                path=None,
                font_type=FontType.FAMILY.value
            ),
            PairNamePathFont(
                name=cfg.base_name,
                path=self.path_font_folder / f"{cfg.base_name}-Regular.ttf",
                font_type=FontType.NORMAL.value
            ),
            PairNamePathFont(
                name=f"{cfg.base_name}-Bold",
                path=self.path_font_folder / f"{cfg.base_name}-Bold.ttf",
                font_type=FontType.BOLD.value
            ),
            PairNamePathFont(
                name=f"{cfg.base_name}-Italic",
                path=self.path_font_folder / f"{cfg.base_name}-Italic.ttf",
                font_type=FontType.ITALIC.value
            ),
            PairNamePathFont(
                name=f"{cfg.base_name}-BoldItalic",
                path=self.path_font_folder / f"{cfg.base_name}-BoldItalic.ttf",
                font_type=FontType.BOLD_ITALIC.value
            ),
        ]

    def _font_family_kwargs(self, cfg: FontLoaderConfig) -> dict:
        return {pair.font_type: pair.name for pair in self._font_pairs(cfg)}

    def _register_font_family(self, cfg: FontLoaderConfig) -> None:
        font_pairs = self._font_pairs(cfg)
        self._raise_if_missing_files(cfg, font_pairs)

        for pair in font_pairs:
            if pair.path:
                pdfmetrics.registerFont(TTFont(pair.name, str(pair.path)))

        registerFontFamily(**self._font_family_kwargs(cfg))

    def _raise_if_missing_files(self, cfg: FontLoaderConfig, font_pairs: List[PairNamePathFont]) -> None:
        missing_files = [pair.path.name for pair in font_pairs if pair.path and not pair.path.exists()]
        if missing_files:
            raise FileNotFoundError(
                f"Missing files | {PATH_FONTS / cfg.base_name} | {', '.join(missing_files)}"
            )
