from typing import Optional, Tuple
from pathlib import Path
from PIL import Image, ImageDraw
from io import BytesIO

import PyPDF2
import fitz
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import StyleSheet1

from linkedin2cv.models import (
    load_linkedin_data,
    LinkedinData,
    StyleCV,
    SizesCV,
    BuilderCVConfig,
)
from linkedin2cv.draw import DrawCVService
from linkedin2cv.constants import (
    PATH_DATA_DIR,
    PATH_ASSETS_DIR,
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
        style_cv: Optional[StyleCV] = None,
        sizes_cv: Optional[SizesCV] = None,
        age: Optional[int] = None,
        location: Optional[str] = None,
        mail: Optional[str] = None,
        url_website_es: Optional[str] = None,
        url_website_en: Optional[str] = None,
        url_github: Optional[str] = None,
        url_linkedin: Optional[str] = None,
        page_size: Tuple[float, float] = A4,
        is_photo_circle: bool = True,
        drawer: Optional[DrawCVService] = None,
        config: Optional[BuilderCVConfig] = None,
    ):
        if config is not None:
            age = config.age
            location = config.location
            mail = config.mail
            url_website_es = config.url_website_es
            url_website_en = config.url_website_en
            url_github = config.url_github
            url_linkedin = config.url_linkedin
            page_size = config.page_size
            is_photo_circle = config.is_photo_circle
            if sizes_cv is None:
                sizes_cv = SizesCV(
                    margin=config.margin_mm,
                    margin_left=config.margin_left_mm,
                    column_left_width=config.column_left_width_mm,
                    photo_size=config.photo_size_mm,
                )

        if age is None or location is None or mail is None:
            raise ValueError("age, location y mail son requeridos")

        self.path_data = PATH_DATA_DIR
        self.path_assets = PATH_ASSETS_DIR
        self.path_python_icon = PATH_PYTHON_ICON
        self.path_folder = PATH_FOLDER_DATA
        self.data: LinkedinData = load_linkedin_data(path_folder=self.path_folder)
        self.style_cv = style_cv or StyleCV()
        self.sizes_cv = sizes_cv or SizesCV()
        self.drawer = drawer or DrawCVService()
        self.age = age
        self.location = location
        self.mail = mail
        self.url_website_es = url_website_es
        self.url_website_en = url_website_en
        self.url_github = url_github
        self.url_linkedin = url_linkedin
        self.page_width, self.page_height = page_size
        self.is_photo_circle = is_photo_circle
        self.lines_to_draw = []
        self.path_photo = PATH_PHOTO
        if not self.path_photo.exists():
            raise FileNotFoundError(f"No existe la foto de perfil: {self.path_photo}")
        self.path_pdf = self.path_data / f"{self.path_folder.stem}{PDF_EXTENSION}"
        self.c = Canvas(str(self.path_pdf), pagesize=page_size)
        self.styles: StyleSheet1 = self.style_cv.get_styles()
        self.xi: int = None

    def add_line(self, x1, y1, x2, y2):
        self.lines_to_draw.append((x1, y1, x2, y2))

    def build_and_save(self) -> None:
        self.drawer.draw_background(
            c=self.c,
            color=self.style_cv.background,
            page_width=self.page_width,
            page_height=self.page_height,
        )
        self.drawer.draw_sidebar(
            c=self.c,
            data=self.data,
            sizes_cv=self.sizes_cv,
            style_cv=self.style_cv,
            styles=self.styles,
            age=self.age,
            location=self.location,
            mail=self.mail,
            page_height=self.page_height,
            url_website_es=self.url_website_es,
            url_website_en=self.url_website_en,
            url_github=self.url_github,
            url_linkedin=self.url_linkedin,
        )
        self.drawer.draw_photo(
            c=self.c,
            path_photo=self.path_photo,
            sizes_cv=self.sizes_cv,
            page_height=self.page_height,
            is_photo_circle=self.is_photo_circle,
        )
        lines_to_draw, x_i = self.drawer.draw_positions(
            c=self.c,
            data=self.data,
            sizes_cv=self.sizes_cv,
            style_cv=self.style_cv,
            styles=self.styles,
            path_python_icon=self.path_python_icon,
            page_width=self.page_width,
            page_height=self.page_height,
            sidebar_args={
                "age": self.age,
                "location": self.location,
                "mail": self.mail,
                "url_website_es": self.url_website_es,
                "url_website_en": self.url_website_en,
                "url_github": self.url_github,
                "url_linkedin": self.url_linkedin,
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
