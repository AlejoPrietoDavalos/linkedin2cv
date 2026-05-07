"""Adaptador de carga de fuentes para la capa de aplicación."""

from typing import List

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

from src.core.constants import PATH_FONTS
from src.core.drivers.font_loader import CoreFontLoader, FontLoaderConfig, PairNamePathFont


class FontLoader(CoreFontLoader):
    """Carga fuentes usando la configuración central del core."""

    def load_fonts(self, cfg: FontLoaderConfig) -> None:
        self._register_font_family(cfg)

    def _font_pairs(self, cfg: FontLoaderConfig) -> List[PairNamePathFont]:
        folder = PATH_FONTS / cfg.base_name
        return [
            PairNamePathFont(name=cfg.base_name, path=None, font_type="family"),
            PairNamePathFont(name=cfg.base_name, path=folder / f"{cfg.base_name}-Regular.ttf", font_type="normal"),
            PairNamePathFont(name=f"{cfg.base_name}-Bold", path=folder / f"{cfg.base_name}-Bold.ttf", font_type="bold"),
            PairNamePathFont(name=f"{cfg.base_name}-Italic", path=folder / f"{cfg.base_name}-Italic.ttf", font_type="italic"),
            PairNamePathFont(name=f"{cfg.base_name}-BoldItalic", path=folder / f"{cfg.base_name}-BoldItalic.ttf", font_type="boldItalic"),
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
