from reportlab.pdfgen.canvas import Canvas


class RectDrawer:
    def draw(
        self,
        *,
        c: Canvas,
        color: tuple[float, float, float],
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> None:
        c.setFillColorRGB(*color)
        c.rect(x, y, width, height, fill=True, stroke=0)
