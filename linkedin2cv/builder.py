from typing import Optional, Tuple
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Frame, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

from linkedin2cv.models import load_linkedin_data, LinkedinData, ColorsCV, SizesCV

DIST_PYTHON_ICON_TO_TITLE = 4
DIST_BETWEEN_LINKS = 1
DIST_FULL_NAME_TO_LINKS = 15
DIST_LINKS_TO_SUMMARY = 15
LEN_PYTHON_ICON = 3

SIDEBAR_TO_BODY_GAP = 0 * mm
PHOTO_TOP_PADDING = 10 * mm
PHOTO_CENTER_OFFSET = 2 * mm        # TODO: No lo uso.
NAME_HEIGHT = 50
INFO_BLOCK_Y_OFFSET = 42
INFO_BLOCK_HEIGHT = 40
SPACER_HEIGHT = 6
FRAME_MARGIN_LEFT = 1 * mm
FRAME_MARGIN_RIGHT = 1 * mm

FONT = "HackNerdFont"


class BuilderCV:
    def __init__(
            self,
            *,
            folder_name: str,
            colors_cv: ColorsCV,
            sizes_cv: SizesCV,
            age: int,
            url_website: Optional[str] = None,
            url_github: Optional[str] = None,
            path_data: Path = Path("data"),
            photo_name: Optional[str] = None,
            page_size: Tuple[float, float] = A4,
            photo_circle: bool = True
    ):
        self.path_data = path_data
        self.path_folder = self.path_data / folder_name
        self.data: LinkedinData = load_linkedin_data(path_folder=self.path_folder)
        self.colors_cv = colors_cv
        self.sizes_cv = sizes_cv
        self.age = age
        self.url_website = url_website
        self.url_github = url_github
        self.page_width, self.page_height = page_size
        self.photo_circle = photo_circle

        self.path_photo = self.path_data / photo_name if photo_name else None
        self.path_pdf = self.path_data / f"{self.path_folder.stem}.pdf"
        self.c = Canvas(str(self.path_pdf), pagesize=page_size)
        self.styles = self._load_styles()

    @property
    def full_name(self) -> str:
        return f"{self.data.profile.first_name} {self.data.profile.last_name}"

    def _load_styles(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="Header", fontName=FONT, fontSize=25, leading=24, alignment=TA_LEFT, textColor=self.colors_cv.accent))
        styles.add(ParagraphStyle(name="SubHeader", fontName=FONT, fontSize=6, leading=16, alignment=TA_LEFT, textColor=self.colors_cv.sidebar_text))
        styles.add(ParagraphStyle(name="JobTitle", fontName=FONT, fontSize=11, leading=14, textColor=self.colors_cv.accent, spaceAfter=4))
        styles.add(ParagraphStyle(name="JobSubTitle", fontName=FONT, fontSize=8, leading=14, textColor=self.colors_cv.accent, spaceAfter=4))
        styles.add(ParagraphStyle(name="JobDesc", fontName=FONT, fontSize=7, leading=12, textColor=self.colors_cv.text))
        styles.add(ParagraphStyle(name="SidebarText", fontName=FONT, fontSize=6, leading=10, textColor=self.colors_cv.sidebar_text, alignment=TA_LEFT))
        styles.add(ParagraphStyle(name="SidebarName", fontName=FONT, fontSize=10, leading=12, textColor=self.colors_cv.sidebar_text, alignment=TA_CENTER))
        styles.add(ParagraphStyle(name="SidebarLinks", fontName=FONT, fontSize=6, leading=9, textColor=self.colors_cv.sidebar_text, alignment=TA_LEFT))
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

    def draw_sidebar(self):
        self.c.setFillColor(self.colors_cv.sidebar_panel)
        self.c.rect(self.sizes_cv.margin_left, 0, self.sizes_cv.column_left_wifth, self.page_height, fill=True, stroke=0)

        photo_bottom = self.page_height - self.sizes_cv.photo_size - PHOTO_TOP_PADDING
        sidebar_text_bottom = self.sizes_cv.margin + 5 * mm
        sidebar_height = photo_bottom - sidebar_text_bottom

        content = []

        # Nombre completo, más chico
        content.append(Paragraph(self.full_name, self.styles["SidebarName"]))
        content.append(Spacer(1, DIST_FULL_NAME_TO_LINKS))

        # Info personal (edad, links)
        info_lines = []
        if self.age:
            info_lines.append(f"Edad: {self.age}")
        if self.url_website:
            info_lines.append(f"Mi página web: <a href='{self.url_website}'>{self.url_website}</a>")
        if self.url_github:
            info_lines.append(f"GitHub: <a href='{self.url_github}'>{self.url_github}</a>")

        for line in info_lines:
            content.append(Paragraph(line, self.styles["SidebarLinks"]))
            content.append(Spacer(1, DIST_BETWEEN_LINKS))

        # Summary del perfil
        content.append(Spacer(1, DIST_LINKS_TO_SUMMARY))
        content.append(Paragraph(self.data.profile.summary, self.styles["SidebarText"]))

        frame = Frame(
            self.sizes_cv.margin_left + FRAME_MARGIN_LEFT,
            sidebar_text_bottom,
            self.sizes_cv.column_left_wifth - FRAME_MARGIN_LEFT - FRAME_MARGIN_RIGHT,
            sidebar_height,
            showBoundary=0
        )

        frame.addFromList(content, self.c)

    def draw_positions(self):
        x = self.sizes_cv.margin + self.sizes_cv.column_left_wifth + SIDEBAR_TO_BODY_GAP
        width = self.page_width - x - self.sizes_cv.margin
        y_start = self.page_height - self.sizes_cv.margin
        bottom_margin = self.sizes_cv.margin
        usable_height = y_start - bottom_margin
        current_y = 0

        story = []
        is_first_page = True


        def flush_story(is_first: bool):
            nonlocal current_y, story
            if not is_first:
                self.c.showPage()
                self.draw_background()
                self.draw_sidebar()
                self.draw_photo()

            Frame(x, bottom_margin, width, usable_height, showBoundary=0).addFromList(story, self.c)
            story.clear()
            current_y = 0

        for position in self.data.positions:
            # Custom flowable para imagen + texto horizontal
            from reportlab.platypus import Flowable

            class IconTitle(Flowable):
                def __init__(self, img_path: Path, text: str, style: ParagraphStyle, img_size: float):
                    super().__init__()
                    self.img_path = img_path
                    self.text = text
                    self.style = style
                    self.img_size = img_size
                    self.p = Paragraph(self.text, self.style)

                def wrap(self, availWidth, availHeight):
                    w, h = self.p.wrap(availWidth - self.img_size - DIST_PYTHON_ICON_TO_TITLE, availHeight)
                    self._p_width = w
                    self._p_height = h
                    return w + self.img_size + 2, max(h, self.img_size)

                def draw(self):
                    y_img = (self._p_height - self.img_size) / 2
                    self.canv.drawImage(
                        str(self.img_path), 0, y_img,
                        width=self.img_size, height=self.img_size,
                        preserveAspectRatio=True, mask='auto'
                    )
                    self.p.drawOn(self.canv, self.img_size + DIST_PYTHON_ICON_TO_TITLE, 0)

            path_icon_py = self.path_data / "python_icon.png"
            icon_size = LEN_PYTHON_ICON * mm
            para_title = IconTitle(path_icon_py, position.text_title, self.styles["JobTitle"], icon_size)
            para_sub_title = Paragraph(f"➤ {position.text_sub_title}", self.styles["JobSubTitle"])
            para_desc = Paragraph(position.description, self.styles["JobDesc"])
            spacer = Spacer(1, SPACER_HEIGHT)

            h_title = para_title.wrap(width, usable_height)[1]
            h_sub_title = para_sub_title.wrap(width, usable_height)[1]
            h_desc = para_desc.wrap(width, usable_height)[1]
            h_spacer = spacer.wrap(width, usable_height)[1]
            total_height = h_title + h_sub_title + h_desc + h_spacer

            if current_y + total_height > usable_height:
                flush_story(is_first_page)
                is_first_page = False

            story.extend([para_title, para_sub_title, para_desc, spacer])
            current_y += total_height

        if story:
            flush_story(is_first_page)

    def build_and_save(self):
        self.draw_background()
        self.draw_sidebar()
        self.draw_photo()
        self.draw_positions()
        self.c.save()
