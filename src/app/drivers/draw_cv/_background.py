from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.draw_cv.reportlab_tools import RectDrawer
from src.app.drivers.styles_repository import _hex_to_rgb
from src.core.entities.config import SizesCV
from src.core.entities.styles_config import StylesConfig


class BackgroundDrawer:
    def __init__(self, rect_drawer: RectDrawer | None = None) -> None:
        self.rect_drawer = rect_drawer or RectDrawer()

    def draw_background(self, *, c: Canvas, styles_config: StylesConfig, sizes_cv: SizesCV) -> None:
        self.rect_drawer.draw(
            c=c,
            color=_hex_to_rgb(styles_config.background),
            x=0, y=0,
            width=sizes_cv.page_width,
            height=sizes_cv.page_height,
        )
