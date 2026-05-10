"""Ubica una imagen y un titulo a la misma altura, centrado."""

from typing import Tuple

from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from src.app.drivers.draw_cv.reportlab_tools.image_drawer import ImageDrawer
from src.core.entities import ImageDrawCfg, ImageTitleDrawCfg


class ImageTitleDrawer:
    def __init__(self, image_drawer: ImageDrawer | None = None) -> None:
        self.image_drawer = image_drawer or ImageDrawer()

    def _measure_title_row(
        self,
        *,
        cfg: ImageTitleDrawCfg,
        style: ParagraphStyle,
        available_width: float,
        available_height: float,
    ) -> Tuple[Paragraph, float]:
        paragraph = Paragraph(cfg.title_html, style)
        _, text_height = paragraph.wrap(
            available_width - cfg.img_size - cfg.image_to_title_dist,
            available_height,
        )
        row_height = max(text_height, cfg.img_size)
        return paragraph, row_height

    def _draw_title_row(
        self,
        *,
        c: Canvas,
        cfg: ImageTitleDrawCfg,
        paragraph: Paragraph,
        row_height: float,
        x: float,
        y: float,
    ) -> None:
        y_img = (row_height - cfg.img_size) / 2
        self.image_drawer.draw_image(
            c=c,
            cfg=ImageDrawCfg(
                path_img=cfg.path_img,
                x=x,
                y=y + y_img,
                width=cfg.img_size,
                height=cfg.img_size,
            ),
        )
        paragraph.drawOn(
            c,
            x + cfg.img_size + cfg.image_to_title_dist,
            y + (row_height - paragraph.height) / 2,
        )

    def draw_title_row_at_cursor(
        self,
        *,
        c: Canvas,
        cfg: ImageTitleDrawCfg,
        style: ParagraphStyle,
        x: float,
        y_cursor: float,
        available_width: float,
        available_height: float,
    ) -> float:
        paragraph, row_height = self._measure_title_row(
            cfg=cfg,
            style=style,
            available_width=available_width,
            available_height=available_height,
        )
        y_row = y_cursor - row_height
        self._draw_title_row(c=c, cfg=cfg, paragraph=paragraph, row_height=row_height, x=x, y=y_row)
        return y_row
