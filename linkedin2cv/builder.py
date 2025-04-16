from typing import Optional, Tuple
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Frame, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY

from linkedin2cv.models import load_linkedin_data, LinkedinData, ColorsCV, SizesCV

FONT = "HackNerdFont"
SIDEBAR_TO_BODY_GAP = 2 * mm
PHOTO_TOP_PADDING = 10 * mm
PHOTO_CENTER_OFFSET = 2 * mm        # TODO: No lo uso.
NAME_HEIGHT = 50
INFO_BLOCK_Y_OFFSET = 42
INFO_BLOCK_HEIGHT = 40
SPACER_HEIGHT = 6
FRAME_MARGIN_LEFT = 1 * mm
FRAME_MARGIN_RIGHT = 1 * mm


class BuilderCV:
    def __init__(
            self,
            *,
            folder_name: str,
            colors_cv: ColorsCV,
            sizes_cv: SizesCV,
            age: int,
            url_linkedin: str,
            url_github: Optional[str] = None,
            url_website: Optional[str] = None,
            path_data: Path = Path("data"),
            photo_name: Optional[str] = None,
            page_size: Tuple[float, float] = A4,
            photo_circle: bool = True
    ):
        self.path_folder = path_data / folder_name
        self.data: LinkedinData = load_linkedin_data(path_folder=self.path_folder)
        self.colors_cv = colors_cv
        self.sizes_cv = sizes_cv
        self.age = age
        self.url_linkedin = url_linkedin
        self.url_github = url_github
        self.url_website = url_website
        self.page_width, self.page_height = page_size
        self.photo_circle = photo_circle

        self.path_photo = path_data / photo_name if photo_name else None
        self.path_pdf = path_data / f"{self.path_folder.stem}.pdf"
        self.c = Canvas(str(self.path_pdf), pagesize=page_size)
        self.styles = self._load_styles()

    @property
    def full_name(self) -> str:
        return f"{self.data.profile.first_name} {self.data.profile.last_name}"

    def _load_styles(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="Header", fontName=FONT, fontSize=25, leading=24,
                                  alignment=TA_LEFT, textColor=self.colors_cv.accent))
        styles.add(ParagraphStyle(name="SubHeader", fontName=FONT, fontSize=6, leading=16,
                                  alignment=TA_LEFT, textColor=self.colors_cv.text))
        styles.add(ParagraphStyle(name="JobTitle", fontName=FONT, fontSize=11, leading=14,
                                  textColor=self.colors_cv.accent, spaceAfter=4))
        styles.add(ParagraphStyle(name="JobDesc", fontName=FONT, fontSize=7, leading=12,
                                  textColor=self.colors_cv.text))
        styles.add(ParagraphStyle(name="SidebarText", fontName=FONT, fontSize=6, leading=10,
                                  textColor=self.colors_cv.text, alignment=TA_LEFT))
        return styles

    def draw_background(self):
        self.c.setFillColor(self.colors_cv.background)
        self.c.rect(0, 0, self.page_width, self.page_height, fill=True, stroke=0)

    def draw_photo(self):
        if self.path_photo and self.path_photo.exists():
            x = self.sizes_cv.margin_left + (self.sizes_cv.column_left_wifth - self.sizes_cv.photo_size) / 2
            y = self.page_height - self.sizes_cv.photo_size - PHOTO_TOP_PADDING

            if self.photo_circle:
                radius = self.sizes_cv.photo_size / 2
                center_x = x + radius
                center_y = y + radius
                self.c.saveState()
                path = self.c.beginPath()
                path.circle(center_x, center_y, radius)
                self.c.clipPath(path, stroke=0)

            self.c.drawImage(str(self.path_photo), x, y,
                             width=self.sizes_cv.photo_size, height=self.sizes_cv.photo_size,
                             preserveAspectRatio=True, mask='auto')

            if self.photo_circle:
                self.c.restoreState()

    def draw_header(self):
        x = self.sizes_cv.margin_left + self.sizes_cv.column_left_wifth + SIDEBAR_TO_BODY_GAP
        max_width = self.page_width - x - self.sizes_cv.margin

        name_y = self.page_height - self.sizes_cv.margin - NAME_HEIGHT
        name_frame = Frame(x, name_y, max_width, NAME_HEIGHT, showBoundary=0)
        name_frame.addFromList([Paragraph(self.full_name, self.styles["Header"])], self.c)

        info = []
        if self.age:
            info.append(f"Edad: {self.age}")
        if self.url_website:
            info.append(f"Mi página web: <a href='{self.url_website}'>{self.url_website}</a>")
        if self.url_github:
            info.append(f"GitHub: <a href='{self.url_github}'>{self.url_github}</a>")
        if self.url_linkedin:
            info.append(f"LinkedIn: <a href='{self.url_linkedin}'>{self.url_linkedin}</a>")

        style_subheader = ParagraphStyle(name="SubHeaderCompact", parent=self.styles["SubHeader"], leading=10, spaceAfter=2)
        info_paragraphs = [Paragraph(i, style_subheader) for i in info]

        Frame(x, name_y - INFO_BLOCK_Y_OFFSET, max_width, INFO_BLOCK_HEIGHT, showBoundary=0).addFromList(info_paragraphs, self.c)

    def draw_sidebar(self):
        self.c.setFillColor(self.colors_cv.primary)
        self.c.rect(self.sizes_cv.margin_left, 0, self.sizes_cv.column_left_wifth, self.page_height, fill=True, stroke=0)
        photo_bottom = self.page_height - self.sizes_cv.photo_size - PHOTO_TOP_PADDING
        sidebar_text_bottom = self.sizes_cv.margin + 5 * mm
        sidebar_height = photo_bottom - sidebar_text_bottom

        frame = Frame(
            self.sizes_cv.margin_left + FRAME_MARGIN_LEFT,
            sidebar_text_bottom,
            self.sizes_cv.column_left_wifth - FRAME_MARGIN_LEFT - FRAME_MARGIN_RIGHT,
            sidebar_height,
            showBoundary=0
        )

        frame.addFromList([Paragraph(self.data.profile.summary, self.styles["SidebarText"])], self.c)

    def draw_positions(self):
        x = self.sizes_cv.margin + self.sizes_cv.column_left_wifth + SIDEBAR_TO_BODY_GAP
        width = self.page_width - x - self.sizes_cv.margin
        y_start = self.page_height - self.sizes_cv.margin - 100
        bottom_margin = self.sizes_cv.margin
        usable_height = y_start - bottom_margin
        current_y = 0

        story = []
        first_page = True

        def flush_story():
            nonlocal current_y, story
            self.draw_background()
            if first_page:
                self.draw_sidebar()
                self.draw_photo()
                self.draw_header()
            Frame(x, bottom_margin, width, usable_height, showBoundary=0).addFromList(story, self.c)
            self.c.showPage()
            current_y = 0
            story.clear()

        for p in self.data.positions:
            title = f"{p.title} — {p.company_name} ({p.started_on} - {p.finished_on or 'Presente'})"
            para_title = Paragraph(title, self.styles["JobTitle"])
            para_desc = Paragraph(p.description.replace("\n", "<br/>"), self.styles["JobDesc"])
            spacer = Spacer(1, SPACER_HEIGHT)
            h_title = para_title.wrap(width, usable_height)[1]
            h_desc = para_desc.wrap(width, usable_height)[1]
            h_spacer = spacer.wrap(width, usable_height)[1]
            total_height = h_title + h_desc + h_spacer

            if current_y + total_height > usable_height:
                flush_story()
                first_page = False

            story.extend([para_title, para_desc, spacer])
            current_y += total_height

        if story:
            self.draw_background()
            Frame(x, bottom_margin, width, usable_height, showBoundary=0).addFromList(story, self.c)

    def build_and_save(self):
        self.draw_background()
        self.draw_sidebar()
        self.draw_photo()
        self.draw_header()
        self.draw_positions()
        self.c.save()
