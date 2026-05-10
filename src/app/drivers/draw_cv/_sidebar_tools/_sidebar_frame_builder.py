from reportlab.lib.units import mm
from reportlab.platypus import Frame

from src.core.entities.config import LayoutConfig, SpacingConfig


class SidebarFrameBuilder:
    def _get_vertical_bounds(self, *, layout_cfg: LayoutConfig) -> tuple[float, float]:
        sidebar_text_bottom = layout_cfg.margin_pt + 5 * mm
        sidebar_height = layout_cfg.photo_y - sidebar_text_bottom
        return sidebar_text_bottom, sidebar_height

    def build(self, *, layout_cfg: LayoutConfig, spacing: SpacingConfig) -> Frame:
        sidebar_text_bottom, sidebar_height = self._get_vertical_bounds(layout_cfg=layout_cfg)
        return Frame(
            layout_cfg.margin_left_pt + spacing.frame_margin_left_mm * mm,
            sidebar_text_bottom,
            layout_cfg.column_left_width_pt - (spacing.frame_margin_left_mm + spacing.frame_margin_right_mm) * mm,
            sidebar_height,
            showBoundary=0,
        )
