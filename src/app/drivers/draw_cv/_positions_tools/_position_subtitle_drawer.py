from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from src.core.entities import DrawCVConfig, PositionsDrawCfg, PositionsLayoutDTO
from src.core.hardcoded_config import format_job_subtitle_html


class PositionSubtitleDrawer:
    def draw(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        draw_config: DrawCVConfig,
        layout: PositionsLayoutDTO,
        subtitle_text: str,
        y_cursor: float,
    ) -> float:
        subtitle = Paragraph(format_job_subtitle_html(subtitle=subtitle_text), cfg.styles["JobSubTitle"])
        _, subtitle_height = subtitle.wrap(layout.body_width, layout.usable_height)
        subtitle.drawOn(c, layout.body_x, y_cursor - subtitle_height)
        return y_cursor - subtitle_height - draw_config.line_thickness
