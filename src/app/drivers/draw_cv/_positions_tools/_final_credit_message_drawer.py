from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from src.core.entities import PositionsDrawCfg, PositionsLayoutDTO
from src.core.hardcoded_config import format_final_credit_html


class FinalCreditMessageDrawer:
    def draw(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        layout: PositionsLayoutDTO,
        y_cursor: float,
    ) -> None:
        final_text = Paragraph(format_final_credit_html(), cfg.styles["JobDesc"])
        _, h_final = final_text.wrap(layout.body_width, layout.usable_height)
        final_text.drawOn(c, layout.body_x, y_cursor - h_final)
