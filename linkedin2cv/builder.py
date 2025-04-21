from typing import Optional, Tuple
from pathlib import Path
from PIL import Image, ImageDraw
from io import BytesIO

import PyPDF2
import fitz
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import StyleSheet1

from linkedin2cv.models import load_linkedin_data, LinkedinData, StyleCV, SizesCV
from linkedin2cv.draw import draw_background, draw_photo, draw_sidebar, draw_positions


def add_line_to_pdf(
    page: fitz.Page,
    start: Tuple[float, float],         # FIXME: Cambiar a x1, y1, x2, y2.
    end: Tuple[float, float],           # FIXME: Cambiar a x1, y1, x2, y2.
    color: Tuple[float, float, float] = (0, 0, 0),
    width: float = 1.0
) -> None:
    """
    Draws a line on a given PDF page.

    Args:
        page (fitz.Page): The PDF page to modify.
        start (Tuple[float, float]): Starting point (x0, y0).
        end (Tuple[float, float]): Ending point (x1, y1).
        color (Tuple[float, float, float], optional): RGB color values (0-1).
        width (float, optional): Line width in points.
    """
    page.draw_line(p1=start, p2=end, color=color, width=width)



# Función para crear una imagen con líneas
def create_image_with_lines(lines: list[tuple[float, float, float, float]], width: int, height: int) -> Image:
    # Crear una imagen en blanco
    img = Image.new("RGB", (int(width), int(height)), color="white")
    draw = ImageDraw.Draw(img)

    # Dibujar las líneas en la imagen
    for (x1, y1, x2, y2) in lines:
        draw.line((x1, y1, x2, y2), fill="black", width=2)

    return img


# Función para agregar una imagen a un PDF existente
def add_image_to_pdf(input_pdf_path: Path, output_pdf_path: Path, image: Image) -> None:
    # Convertir la imagen a un formato adecuado para PyPDF2
    img_byte_array = BytesIO()
    image.save(img_byte_array, format='PDF')
    img_byte_array.seek(0)

    # Leer el PDF original
    with open(input_pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()

        # Crear un PDF con la imagen
        img_pdf = PyPDF2.PdfReader(img_byte_array)

        # Copiar las páginas del PDF original
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

        # Fusionar la imagen en el PDF
        pdf_writer.pages[0].merge_page(img_pdf.pages[0])

        # Guardar el archivo final
        with open(output_pdf_path, "wb") as output_file:
            pdf_writer.write(output_file)


class BuilderCV:
    def __init__(
            self,
            *,
            folder_name: str,
            style_cv: StyleCV,
            sizes_cv: SizesCV,
            age: int,
            location: str,
            url_website: Optional[str] = None,
            url_github: Optional[str] = None,
            path_data: Path = Path("data"),
            photo_name: Optional[str] = None,
            page_size: Tuple[float, float] = A4,
            is_photo_circle: bool = True
    ):
        self.path_data = path_data
        self.path_python_icon = self.path_data / "python_icon.png"
        self.path_folder = self.path_data / folder_name
        self.data: LinkedinData = load_linkedin_data(path_folder=self.path_folder)
        self.style_cv = style_cv
        self.sizes_cv = sizes_cv
        self.age = age
        self.location = location
        self.url_website = url_website
        self.url_github = url_github
        self.page_width, self.page_height = page_size
        self.is_photo_circle = is_photo_circle
        self.lines_to_draw = []  # Lista de tuplas (x1, y1, x2, y2)

        self.path_photo = self.path_data / photo_name if photo_name else None
        self.path_pdf = self.path_data / f"{self.path_folder.stem}.pdf"
        self.c = Canvas(str(self.path_pdf), pagesize=page_size)
        self.styles: StyleSheet1 = self.style_cv.get_styles()
        self.xi: int = None

    def add_line(self, x1, y1, x2, y2):
        self.lines_to_draw.append((x1, y1, x2, y2))

    def draw_background(self):
        draw_background(
            c=self.c,
            color=self.style_cv.background,
            page_width=self.page_width,
            page_height=self.page_height
        )

    def draw_photo(self):
        draw_photo(
            c=self.c,
            path_photo=self.path_photo,
            sizes_cv=self.sizes_cv,
            page_height=self.page_height,
            is_photo_circle=self.is_photo_circle
        )

    def draw_sidebar(self):
        draw_sidebar(
            c=self.c,
            data=self.data,
            sizes_cv=self.sizes_cv,
            style_cv=self.style_cv,
            styles=self.styles,
            age=self.age,
            location=self.location,
            page_height=self.page_height,
            url_website=self.url_website,
            url_github=self.url_github
        )

    def draw_positions(self):
        lines_to_draw, x_i = draw_positions(
            c=self.c,
            data=self.data,
            sizes_cv=self.sizes_cv,
            style_cv=self.style_cv,
            styles=self.styles,
            path_python_icon=self.path_python_icon,
            page_width=self.page_width,
            page_height=self.page_height
        )
        self.lines_to_draw = lines_to_draw
        self.x_i = x_i  # Posición inicial del puesto. En x.

    def build_and_save(self) -> None:
        self.draw_background()
        self.draw_sidebar()
        self.draw_photo()
        self.draw_positions()
        self.c.save()
        #self.draw_lines()
        self.draw_last_text()

    def draw_last_text(self) -> None:
        ...

    def draw_lines(self) -> None:
        doc = fitz.open(self.path_pdf)
        page = doc[0]
        for line_to_draw in self.lines_to_draw:
            x1, y1, x2, y2 = line_to_draw
            add_line_to_pdf(page, start=(x1, y1), end=(x2, y2), color=(1, 0, 0))  # red line
        doc.save(self.path_pdf)
        doc.close()
