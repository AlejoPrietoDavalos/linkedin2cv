from reportlab.lib.styles import StyleSheet1
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from src.app.drivers.draw_cv.reportlab_tools import ParagraphBlockDrawer
from src.core.entities import PositionsLayoutDTO
from src.core.entities.config import SpacingConfig


class PositionSubtitleDrawer:
    def __init__(self, paragraph_block_drawer: ParagraphBlockDrawer | None = None) -> None:
        self.paragraph_block_drawer = paragraph_block_drawer or ParagraphBlockDrawer()

    def draw(
        self,
        *,
        c: Canvas,
        styles: StyleSheet1,
        spacing_config: SpacingConfig,
        layout: PositionsLayoutDTO,
        text: str,
        y_cursor: float,
    ) -> float:
        paragraph = Paragraph(text, styles["JobSubTitle"])
        y_cursor = self.paragraph_block_drawer.draw(
            c=c,
            paragraph=paragraph,
            x=layout.body_x,
            width=layout.body_width,
            available_height=layout.usable_height,
            y_cursor=y_cursor,
            spacing_after=spacing_config.line_thickness,
        )
        return y_cursor
