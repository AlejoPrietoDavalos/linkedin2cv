from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from src.core.entities import DrawCVConfig, PositionsDrawCfg, PositionsLayoutDTO
from src.core.hardcoded_config import JOB_DESCRIPTION_FALLBACK


class PositionDescriptionDrawer:
    def draw(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        draw_config: DrawCVConfig,
        layout: PositionsLayoutDTO,
        description_text: str,
        y_cursor: float,
    ) -> float:
        desc = Paragraph(description_text or JOB_DESCRIPTION_FALLBACK, cfg.styles["JobDesc"])
        _, desc_height = desc.wrap(layout.body_width, layout.usable_height)
        desc.drawOn(c, layout.body_x, y_cursor - desc_height)
        return y_cursor - desc_height - draw_config.spacer_height
