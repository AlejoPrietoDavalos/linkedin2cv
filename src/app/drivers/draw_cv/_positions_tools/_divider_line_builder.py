from reportlab.lib.units import mm

from src.core.entities.config import LayoutConfig, SpacingConfig
from src.core.entities.draw_inputs import DividerLine, PositionsLayoutDTO


class DividerLineBuilder:
    def build(
        self,
        *,
        layout_cfg: LayoutConfig,
        spacing: SpacingConfig,
        positions_layout: PositionsLayoutDTO,
        y_line: float,
    ) -> DividerLine:
        return DividerLine(
            x_start=positions_layout.body_x + spacing.dist_line_spacing_left_mm * mm,
            y_start=y_line,
            x_end=layout_cfg.page_width - layout_cfg.margin_pt - spacing.dist_line_spacing_right_mm * mm,
            y_end=y_line,
        )
