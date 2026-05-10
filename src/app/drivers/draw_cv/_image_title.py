"""Ubica una imagen y un titulo a la misma altura, centrado."""

from typing import Tuple

from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from src.app.drivers.draw_cv._image import ImageDrawer
from src.core.entities import ImageDrawCfg, ImageTitleDrawCfg


class ImageTitleDrawer:
    def __init__(self, image_drawer: ImageDrawer) -> None:
        self.image_drawer = image_drawer

    def measure_title_row(
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

    def draw_title_row(self, *, c: Canvas, cfg: ImageTitleDrawCfg, paragraph: Paragraph, row_height: float) -> None:
        y_img = (row_height - cfg.img_size) / 2
        self.image_drawer.draw_image(
            c=c,
            cfg=ImageDrawCfg(
                path_img=cfg.path_img,
                x=0,
                y=y_img,
                width=cfg.img_size,
                height=cfg.img_size,
            ),
        )
        paragraph.drawOn(
            c,
            cfg.img_size + cfg.image_to_title_dist,
            (row_height - paragraph.height) / 2,
        )
