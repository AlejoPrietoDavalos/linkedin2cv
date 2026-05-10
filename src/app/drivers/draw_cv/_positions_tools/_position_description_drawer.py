from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from src.app.drivers.draw_cv.reportlab_tools import ParagraphBlockDrawer
from src.core.entities import DrawCVConfig, PositionsDrawCfg, PositionsLayoutDTO


class PositionDescriptionDrawer:
    def __init__(self, paragraph_block_drawer: ParagraphBlockDrawer | None = None) -> None:
        self.paragraph_block_drawer = paragraph_block_drawer or ParagraphBlockDrawer()

    def draw(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        draw_config: DrawCVConfig,
        layout: PositionsLayoutDTO,
        text: str,
        y_cursor: float,
    ) -> float:
        paragraph = Paragraph(text, cfg.styles["JobDesc"])
        y_cursor = self.paragraph_block_drawer.draw(
            c=c,
            paragraph=paragraph,
            x=layout.body_x,
            width=layout.body_width,
            available_height=layout.usable_height,
            y_cursor=y_cursor,
            spacing_after=draw_config.spacer_height,
        )
        return y_cursor
