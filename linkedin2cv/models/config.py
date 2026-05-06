from typing import Tuple

from pydantic import BaseModel, Field
from reportlab.lib.pagesizes import A4


class StyleCVConfig(BaseModel):
    sidebar_panel: str = "#4d4d4d"
    accent: str = "#2F2F2F"
    text: str = "#4A4A4A"
    background: str = "#dddddd"
    sidebar_text: str = "#dddddd"


class BuilderCVConfig(BaseModel):
    page_size: Tuple[float, float] = A4
    is_photo_circle: bool = True


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
    photo_top_padding_mm: int = 10
    spacer_height: int = 15
    frame_margin_left_mm: int = 1
    frame_margin_right_mm: int = 1


class LinkedinDataToCVConfig(BaseModel):
    style: StyleCVConfig = Field(default_factory=StyleCVConfig)
    builder: BuilderCVConfig
    draw: DrawCVConfig = Field(default_factory=DrawCVConfig)
