from typing import Optional, Tuple

from pydantic import BaseModel, Field
from linkedin2cv.hardcoded_config import SUMMARY_TECH_STACK_LABEL


class StyleCVConfig(BaseModel):
    sidebar_panel: str = "#4d4d4d"
    accent: str = "#2F2F2F"
    text: str = "#4A4A4A"
    background: str = "#dddddd"
    sidebar_text: str = "#dddddd"


class BuilderCVConfig(BaseModel):
    age: int
    location: str
    mail: str
    url_website_es: Optional[str] = None
    url_website_en: Optional[str] = None
    url_github: Optional[str] = None
    url_linkedin: Optional[str] = None
    page_size: Tuple[float, float] = (595.2755905511812, 841.8897637795277)
    is_photo_circle: bool = True
    margin_mm: int = 5
    margin_left_mm: int = 5
    column_left_width_mm: int = 70
    photo_size_mm: int = 30


class DrawCVConfig(BaseModel):
    tech_stack_label: str = SUMMARY_TECH_STACK_LABEL
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
