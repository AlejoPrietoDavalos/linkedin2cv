from typing import Optional, Tuple
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Frame, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

from linkedin2cv.models import load_linkedin_data, LinkedinData, ColorsCV, SizesCV

AGE = 30
URL_WEB = "https://alejoprietodavalos.github.io/"



class BuilderCV:
    def __init__(
            self,
            *,
            folder_name: str,
            colors_cv: ColorsCV,
            sizes_cv: SizesCV,
            path_data: Path = Path("data"),
            photo_name: Optional[str] = None,
            page_size: Tuple[float, float] = A4,
            photo_circle: bool = True
    ):
        self.path_data = path_data
        self.path_folder: Path = self.path_data / folder_name
        self.data: LinkedinData = load_linkedin_data(path_folder=self.path_folder)
        self.colors_cv = colors_cv
        self.sizes_cv = sizes_cv

        self.path_photo = self._get_path_photo(photo_name=photo_name)

        self.page_size = page_size
        self.photo_circle = photo_circle

        self.page_width, self.page_height = A4
        self.path_pdf: Path = self.path_data / f"{self.path_folder.stem}.pdf"
        self.c = Canvas(str(self.path_pdf), pagesize=page_size)
        self.styles = self._load_styles()

    def _get_path_photo(self, *, photo_name: Optional[str]) -> Optional[Path]:
        if photo_name is not None:
            return self.path_data / photo_name
        return None

    def _load_styles(self) -> None:
        styles = getSampleStyleSheet()

        styles.add(ParagraphStyle(
            name="Header",
            fontName="HackNerdFont",
            fontSize=20,
            leading=24,
            alignment=TA_LEFT,
            textColor=self.colors_cv.accent,
        ))

        styles.add(ParagraphStyle(
            name="SubHeader",
            fontName="HackNerdFont",
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            textColor=self.colors_cv.text,
        ))

        styles.add(ParagraphStyle(
            name="JobTitle",
            fontName="HackNerdFont",
            fontSize=11,
            leading=14,
            textColor=self.colors_cv.accent,
            spaceAfter=4,
        ))

        styles.add(ParagraphStyle(
            name="JobDesc",
            fontName="HackNerdFont",
            fontSize=9,
            leading=12,
            textColor=self.colors_cv.text,
        ))
        return styles

    def draw_background(self) -> None:
        self.c.setFillColor(self.colors_cv.background)
        self.c.rect(0, 0, self.page_width, self.page_height, fill=True, stroke=0)

    def draw_photo(self) -> None:
        if self.path_photo is not None and self.path_photo.exists():
            x = self.page_width - self.sizes_cv.margin - self.sizes_cv.photo_size
            y = self.page_height - self.sizes_cv.margin - self.sizes_cv.photo_size

            if self.photo_circle:
                radius = self.sizes_cv.photo_size / 2
                center_x = x + radius
                center_y = y + radius

                self.c.saveState()
                p = self.c.beginPath()
                p.circle(center_x, center_y, radius)
                self.c.clipPath(p, stroke=0)

            self.c.drawImage(
                str(self.path_photo),
                x,
                y,
                width=self.sizes_cv.photo_size,
                height=self.sizes_cv.photo_size,
                preserveAspectRatio=True,
                mask='auto'
            )

            if self.photo_circle:
                self.c.restoreState()

    def draw_header(self) -> None:
        x = self.sizes_cv.margin_left + self.sizes_cv.column_left_wifth + 10 * mm
        frame = Frame(
            x1=x,
            y1=self.page_height - self.sizes_cv.margin - 60,
            width=self.page_width - x - self.sizes_cv.margin - self.sizes_cv.photo_size,
            height=60,
            showBoundary=0
        )
        _NOMBRE_COMPLETO = f"Nombre completo: {self.data.profile.first_name} {self.data.profile.last_name}"
        name = Paragraph(_NOMBRE_COMPLETO, self.styles["Header"])
        age = Paragraph(f"Edad: {AGE}", self.styles["SubHeader"])
        title = Paragraph(self.data.profile.headline, self.styles["SubHeader"])
        frame.addFromList([name, age, title], self.c)

    def draw_sidebar(self) -> None:
        self.c.setFillColor(self.colors_cv.primary)
        self.c.rect(
            self.sizes_cv.margin_left, 0, self.sizes_cv.column_left_wifth,
            self.page_height, fill=True, stroke=0
        )

        stack_text = Paragraph(self.data.profile.summary, self.styles["JobDesc"])

        frame = Frame(
            self.sizes_cv.margin_left + 5 * mm,
            self.sizes_cv.margin + 5 * mm,
            self.sizes_cv.column_left_wifth - 10 * mm,
            self.page_height - 2 * self.sizes_cv.margin - 10 * mm,
            showBoundary=0
        )
        frame.addFromList([stack_text], self.c)

    def draw_positions(self) -> None:
        x = self.sizes_cv.margin + self.sizes_cv.column_left_wifth + 10 * mm
        y = self.page_height - self.sizes_cv.margin - 100
        width = self.page_width - x - self.sizes_cv.margin
        flow = []

        for p in self.data.positions:
            title_text = f"{p.title} — {p.company_name} ({p.started_on} - {p.finished_on})"
            flow.append(Paragraph(title_text, self.styles["JobTitle"]))
            flow.append(Paragraph(p.description.replace("\n", "<br/>"), self.styles["JobDesc"]))
            flow.append(Spacer(1, 6))

        frame = Frame(x, self.sizes_cv.margin, width, y - self.sizes_cv.margin, showBoundary=0)
        frame.addFromList(flow, self.c)

    def build(self):
        self.draw_background()
        self.draw_sidebar()
        self.draw_photo()
        self.draw_header()
        self.draw_positions()

    def save(self) -> None:
        """ Guarda el PDF en el output específicado."""
        self.c.save()

    def build_and_save(self) -> None:
        self.build()
        self.save()

