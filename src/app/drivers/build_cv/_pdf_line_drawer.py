"""Responsabilidad de dibujar líneas sobre una página del PDF."""

import fitz

from src.core.entities import DividerLine


class PDFLineDrawer:
    def draw_lines(
        self,
        *,
        page: fitz.Page,
        lines: list[DividerLine],
        color: tuple[float, float, float] = (1, 0, 0),
        width: float = 1.0,
    ) -> None:
        for line in lines:
            page.draw_line(
                p1=line.p1,
                p2=line.p2,
                color=color,
                width=width,
            )
