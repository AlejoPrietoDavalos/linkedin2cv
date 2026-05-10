from typing import Tuple

from pydantic import BaseModel, Field
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm


class DrawCVConfig(BaseModel):
    dist_between_title_sidebar_to_text: int = 5
    dist_python_icon_to_title: int = 4
    dist_between_links: int = 1
    dist_full_name_to_headline: int = 8
    dist_headline_to_links: int = 4
    dist_line_spacing_left_mm: int = 3
    dist_line_spacing_right_mm: int = 3
    line_thickness: float = 0.5
    dist_between_title_text_sidebar: int = 9
    len_python_icon_mm: int = 3
    sidebar_to_body_gap_mm: int = 2
    spacer_height: int = 15
    frame_margin_left_mm: int = 1
    frame_margin_right_mm: int = 1
    is_photo_circle: bool = True


class SizesCV(BaseModel):
    page_size: Tuple[float, float] = A4
    margin: int = 5
    margin_left: int = 5
    column_left_width: int = 70
    photo_size: int = 30
    photo_top_padding_mm: int = 10

    @property
    def page_width(self) -> float:
        return self.page_size[0]

    @property
    def page_height(self) -> float:
        return self.page_size[1]

    @property
    def margin_pt(self) -> float:
        return self.margin * mm

    @property
    def margin_left_pt(self) -> float:
        return self.margin_left * mm

    @property
    def column_left_width_pt(self) -> float:
        return self.column_left_width * mm

    @property
    def photo_size_pt(self) -> float:
        return self.photo_size * mm

    @property
    def photo_x(self) -> float:
        return self.margin_left_pt + (self.column_left_width_pt - self.photo_size_pt) / 2

    @property
    def photo_y(self) -> float:
        return self.page_height - self.photo_size_pt - self.photo_top_padding_mm * mm


class BuilderCVConfig(BaseModel):
    draw: DrawCVConfig = Field(default_factory=DrawCVConfig)
    sizes: SizesCV = Field(default_factory=SizesCV)
