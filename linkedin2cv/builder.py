from typing import Optional, Tuple
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import StyleSheet1

from linkedin2cv.models import load_linkedin_data, LinkedinData, StyleCV, SizesCV
from linkedin2cv.draw import _draw_background, _draw_photo, _draw_sidebar, _draw_positions


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

        self.path_photo = self.path_data / photo_name if photo_name else None
        self.path_pdf = self.path_data / f"{self.path_folder.stem}.pdf"
        self.c = Canvas(str(self.path_pdf), pagesize=page_size)
        self.styles: StyleSheet1 = self.style_cv.get_styles()

    def draw_background(self):
        _draw_background(
            c=self.c,
            color=self.style_cv.background,
            page_width=self.page_width,
            page_height=self.page_height
        )

    def draw_photo(self):
        _draw_photo(
            c=self.c,
            path_photo=self.path_photo,
            sizes_cv=self.sizes_cv,
            page_height=self.page_height,
            is_photo_circle=self.is_photo_circle
        )

    def draw_sidebar(self):
        _draw_sidebar(
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
        _draw_positions(
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
        self.draw_background()
        self.draw_sidebar()
        self.draw_photo()
        self.draw_positions()
        self.c.save()
