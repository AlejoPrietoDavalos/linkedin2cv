"""Render del fondo del CV."""

from reportlab.pdfgen.canvas import Canvas

from src.core.entities import BackgroundDrawCfg


class BackgroundDrawer:
    def draw_background(self, *, c: Canvas, cfg: BackgroundDrawCfg) -> None:
        c.setFillColorRGB(*cfg.color)
        c.rect(0, 0, cfg.page_width, cfg.page_height, fill=True, stroke=0)
