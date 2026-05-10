from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.draw_cv.reportlab_tools import RectDrawer
from src.core.entities import SidebarDrawCfg


class SidebarBackgroundDrawer:
    def __init__(self, rect_drawer: RectDrawer | None = None) -> None:
        self.rect_drawer = rect_drawer or RectDrawer()

    def draw(self, *, c: Canvas, cfg: SidebarDrawCfg) -> None:
        self.rect_drawer.draw(
            c=c,
            color=cfg.sidebar_panel_color,
            x=cfg.sizes_cv.margin_left_pt,
            y=0,
            width=cfg.sizes_cv.column_left_width_pt,
            height=cfg.page_height,
        )
