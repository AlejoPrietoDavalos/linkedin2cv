from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.draw_cv.reportlab_tools import RectDrawer
from src.app.drivers.styles_repository import _hex_to_rgb
from src.core.entities.config import LayoutConfig
from src.core.entities.styles_config import StylesConfig


class SidebarBackgroundDrawer:
    def __init__(self, rect_drawer: RectDrawer | None = None) -> None:
        self.rect_drawer = rect_drawer or RectDrawer()

    def draw(self, *, c: Canvas, layout_cfg: LayoutConfig, styles_config: StylesConfig) -> None:
        self.rect_drawer.draw(
            c=c,
            color=_hex_to_rgb(styles_config.sidebar_panel),
            x=layout_cfg.margin_left_pt,
            y=0,
            width=layout_cfg.column_left_width_pt,
            height=layout_cfg.page_height,
        )
