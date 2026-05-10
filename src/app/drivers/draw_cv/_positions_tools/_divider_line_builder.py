from reportlab.lib.units import mm

from src.core.entities import DividerLine, DrawCVConfig, PositionsDrawCfg, PositionsLayoutDTO


class DividerLineBuilder:
    def build(
        self,
        *,
        cfg: PositionsDrawCfg,
        draw_config: DrawCVConfig,
        layout: PositionsLayoutDTO,
        y_line: float,
    ) -> DividerLine:
        return DividerLine(
            x_start=layout.body_x + draw_config.dist_line_spacing_left_mm * mm,
            y_start=y_line,
            x_end=cfg.page_width - cfg.sizes_cv.margin_pt - draw_config.dist_line_spacing_right_mm * mm,
            y_end=y_line,
        )
