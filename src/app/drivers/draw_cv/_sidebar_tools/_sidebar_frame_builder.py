from reportlab.lib.units import mm
from reportlab.platypus import Frame

from src.core.entities import DrawCVConfig, SidebarDrawCfg


class SidebarFrameBuilder:
    def _get_vertical_bounds(self, *, cfg: SidebarDrawCfg) -> tuple[float, float]:
        sidebar_text_bottom = cfg.sizes_cv.margin_pt + 5 * mm
        sidebar_height = cfg.sizes_cv.photo_y - sidebar_text_bottom
        return sidebar_text_bottom, sidebar_height

    def build(self, *, cfg: SidebarDrawCfg, draw_config: DrawCVConfig) -> Frame:
        sidebar_text_bottom, sidebar_height = self._get_vertical_bounds(cfg=cfg)
        return Frame(
            cfg.sizes_cv.margin_left_pt + draw_config.frame_margin_left_mm * mm,
            sidebar_text_bottom,
            cfg.sizes_cv.column_left_width_pt - (draw_config.frame_margin_left_mm + draw_config.frame_margin_right_mm) * mm,
            sidebar_height,
            showBoundary=0,
        )
