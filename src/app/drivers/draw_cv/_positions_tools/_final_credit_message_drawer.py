from reportlab.lib.styles import StyleSheet1
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from src.app.drivers.draw_cv.reportlab_tools import ParagraphBlockDrawer
from src.core.entities import PositionsLayoutDTO
from src.core.hardcoded_config import format_final_credit_html


class FinalCreditMessageDrawer:
    def __init__(self, paragraph_block_drawer: ParagraphBlockDrawer | None = None) -> None:
        self.paragraph_block_drawer = paragraph_block_drawer or ParagraphBlockDrawer()

    def draw(
        self,
        *,
        c: Canvas,
        styles: StyleSheet1,
        layout: PositionsLayoutDTO,
        y_cursor: float,
    ) -> None:
        final_text = Paragraph(format_final_credit_html(), styles["JobDesc"])
        self.paragraph_block_drawer.draw(
            c=c,
            paragraph=final_text,
            x=layout.body_x,
            width=layout.body_width,
            available_height=layout.usable_height,
            y_cursor=y_cursor,
            spacing_after=0,
        )
