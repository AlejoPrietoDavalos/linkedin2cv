from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageDraw
from io import BytesIO

import PyPDF2
import fitz
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import StyleSheet1

from linkedin2cv.models import (
    LinkedinData,
    StyleCV,
    SizesCV,
    BuilderCVConfig,
    PersonalInformation,
)
from linkedin2cv.draw import DrawCVService
from linkedin2cv.constants import (
    PATH_DATA_DIR,
    PATH_FOLDER_DATA,
    PATH_PHOTO,
    PATH_PYTHON_ICON,
    PDF_EXTENSION,
)


def add_line_to_pdf(
    page: fitz.Page,
    start: Tuple[float, float],
    end: Tuple[float, float],
    color: Tuple[float, float, float] = (0, 0, 0),
    width: float = 1.0,
) -> None:
    page.draw_line(p1=start, p2=end, color=color, width=width)


def create_image_with_lines(lines: list[tuple[float, float, float, float]], width: int, height: int) -> Image:
    img = Image.new("RGB", (int(width), int(height)), color="white")
    draw = ImageDraw.Draw(img)
    for (x1, y1, x2, y2) in lines:
        draw.line((x1, y1, x2, y2), fill="black", width=2)
    return img


def add_image_to_pdf(input_pdf_path: Path, output_pdf_path: Path, image: Image) -> None:
    img_byte_array = BytesIO()
    image.save(img_byte_array, format="PDF")
    img_byte_array.seek(0)

    with open(input_pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()
        img_pdf = PyPDF2.PdfReader(img_byte_array)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

        pdf_writer.pages[0].merge_page(img_pdf.pages[0])

        with open(output_pdf_path, "wb") as output_file:
            pdf_writer.write(output_file)


class BuilderCV:
    def __init__(
        self,
        *,
        personal_information: PersonalInformation,
        linkedin_data: LinkedinData,
        style_cv: Optional[StyleCV] = None,
        sizes_cv: Optional[SizesCV] = None,
        draw_cv_service: Optional[DrawCVService] = None,
        cfg_builder: Optional[BuilderCVConfig] = None,
    ):
        self.personal_information = personal_information
        self.style_cv = style_cv or StyleCV()
        self.draw_cv_service = draw_cv_service or DrawCVService()
        self.cfg_builder = cfg_builder or BuilderCVConfig()

        self.sizes_cv = sizes_cv or SizesCV()

        self.linkedin_data: LinkedinData = linkedin_data
        self.page_width, self.page_height = self.cfg_builder.page_size
        self.is_photo_circle = self.cfg_builder.is_photo_circle
        self.lines_to_draw = []
        if not PATH_PHOTO.exists():
            raise FileNotFoundError(f"No existe la foto de perfil: {PATH_PHOTO}")
        self.path_pdf = PATH_DATA_DIR / f"{PATH_FOLDER_DATA.stem}{PDF_EXTENSION}"
        self.c = Canvas(str(self.path_pdf), pagesize=self.cfg_builder.page_size)
        self.styles: StyleSheet1 = self.style_cv.get_styles()
        self.xi: int = None

    def add_line(self, x1, y1, x2, y2):
        self.lines_to_draw.append((x1, y1, x2, y2))

    def build_and_save(self) -> None:
        self.draw_cv_service.draw_background(
            c=self.c,
            color=self.style_cv.background,
            page_width=self.page_width,
            page_height=self.page_height,
        )
        self.draw_cv_service.draw_sidebar(
            c=self.c,
            linkedin_data=self.linkedin_data,
            sizes_cv=self.sizes_cv,
            style_cv=self.style_cv,
            styles=self.styles,
            age=self.personal_information.age,
            location=self.personal_information.location,
            mail=str(self.personal_information.email),
            page_height=self.page_height,
            url_website_es=self.personal_information.url_web_es,
            url_website_en=self.personal_information.url_web_en,
            url_github=self.personal_information.url_github,
            url_linkedin=self.personal_information.url_linkedin,
        )
        self.draw_cv_service.draw_photo(
            c=self.c,
            path_photo=PATH_PHOTO,
            sizes_cv=self.sizes_cv,
            page_height=self.page_height,
            is_photo_circle=self.is_photo_circle,
        )
        lines_to_draw, x_i = self.draw_cv_service.draw_positions(
            c=self.c,
            linkedin_data=self.linkedin_data,
            sizes_cv=self.sizes_cv,
            style_cv=self.style_cv,
            styles=self.styles,
            page_width=self.page_width,
            page_height=self.page_height,
            sidebar_args={
                "age": self.personal_information.age,
                "location": self.personal_information.location,
                "mail": str(self.personal_information.email),
                "url_website_es": self.personal_information.url_web_es,
                "url_website_en": self.personal_information.url_web_en,
                "url_github": self.personal_information.url_github,
                "url_linkedin": self.personal_information.url_linkedin,
            },
        )
        self.lines_to_draw = lines_to_draw
        self.x_i = x_i

        self.c.save()
        self.draw_last_text()

    def draw_last_text(self) -> None:
        ...

    def draw_lines(self) -> None:
        doc = fitz.open(self.path_pdf)
        page = doc[0]
        for line_to_draw in self.lines_to_draw:
            x1, y1, x2, y2 = line_to_draw
            add_line_to_pdf(page, start=(x1, y1), end=(x2, y2), color=(1, 0, 0))
        doc.save(self.path_pdf)
        doc.close()
