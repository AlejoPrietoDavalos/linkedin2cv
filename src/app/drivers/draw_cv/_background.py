from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.draw_cv.reportlab_tools import RectDrawer
from src.core.entities import BackgroundDrawCfg


class BackgroundDrawer:
    def __init__(self, rect_drawer: RectDrawer | None = None) -> None:
        self.rect_drawer = rect_drawer or RectDrawer()

    def draw_background(self, *, c: Canvas, cfg: BackgroundDrawCfg) -> None:
        self.rect_drawer.draw(c=c, color=cfg.color, x=0, y=0, width=cfg.page_width, height=cfg.page_height)
