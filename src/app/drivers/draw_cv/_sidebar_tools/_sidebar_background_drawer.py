from reportlab.pdfgen.canvas import Canvas

from src.core.entities import SidebarDrawCfg


class SidebarBackgroundDrawer:
    def draw(self, *, c: Canvas, cfg: SidebarDrawCfg) -> None:
        c.setFillColor(cfg.style_cv.sidebar_panel)
        c.rect(cfg.sizes_cv.margin_left_pt, 0, cfg.sizes_cv.column_left_width_pt, cfg.page_height, fill=True, stroke=0)
