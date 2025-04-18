from typing import Optional, Tuple
from pathlib import Path
import shutil

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import StyleSheet1
from reportlab.lib.colors import Color

from linkedin2cv.models import load_linkedin_data, LinkedinData, StyleCV, SizesCV
from linkedin2cv.draw import LINE_THICKNESS, draw_background, draw_photo, draw_sidebar, draw_positions

from PIL import Image, ImageDraw
import PyPDF2
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter


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
        self.lines_to_draw = draw_positions(
            c=self.c,
            data=self.data,
            sizes_cv=self.sizes_cv,
            style_cv=self.style_cv,
            styles=self.styles,
            path_python_icon=self.path_python_icon,
            page_width=self.page_width,
            page_height=self.page_height
        )

    def build_and_save(self):
        # Primero, generar el PDF base
        self.draw_background()
        self.draw_sidebar()
        self.draw_photo()
        self.draw_positions()

        # Guardar el PDF sin las líneas
        self.c.save()

        # Crear un nuevo Canvas para dibujar las líneas
        output_pdf_path = self.path_data / f"{self.path_folder.stem}_with_lines.pdf"
        c_lines = Canvas(str(output_pdf_path), pagesize=(self.page_width, self.page_height))

        # Crear la imagen con las líneas
        image_with_lines = create_image_with_lines(self.lines_to_draw, self.page_width, self.page_height)

        # Convertir la imagen con las líneas en PDF
        img_byte_array = BytesIO()
        image_with_lines.save(img_byte_array, format='PDF')
        img_byte_array.seek(0)

        # Leer el PDF base y el PDF con las líneas
        with open(self.path_pdf, "rb") as base_pdf_file:
            base_pdf_reader = PdfReader(base_pdf_file)
            base_pdf_writer = PdfWriter()

            # Copiar las páginas del PDF base
            for page_num in range(len(base_pdf_reader.pages)):
                page = base_pdf_reader.pages[page_num]
                base_pdf_writer.add_page(page)

            # Leer el PDF con las líneas
            img_pdf_reader = PdfReader(img_byte_array)

            # Fusionar la imagen con las líneas con el PDF base
            base_pdf_writer.pages[0].merge_page(img_pdf_reader.pages[0])

            # Guardar el archivo final con líneas
            with open(output_pdf_path, "wb") as final_output_file:
                base_pdf_writer.write(final_output_file)

        print(f"PDF con líneas guardado en: {output_pdf_path}")
