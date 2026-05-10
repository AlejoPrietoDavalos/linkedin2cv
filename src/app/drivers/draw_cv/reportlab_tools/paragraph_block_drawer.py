from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


class ParagraphBlockDrawer:
    def draw(
        self,
        *,
        c: Canvas,
        paragraph: Paragraph,
        x: float,
        width: float,
        available_height: float,
        y_cursor: float,
        spacing_after: float,
    ) -> float:
        _, paragraph_height = paragraph.wrap(width, available_height)
        paragraph.drawOn(c, x, y_cursor - paragraph_height)
        y_cursor = y_cursor - paragraph_height - spacing_after
        return y_cursor
