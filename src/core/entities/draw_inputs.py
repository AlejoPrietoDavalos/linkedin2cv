from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from reportlab.lib.styles import StyleSheet1
from reportlab.lib.units import mm

from src.core.entities.config import DrawCVConfig, SizesCV
from src.core.entities.linkedin_data import LinkedinData
from src.core.entities.personal_information import PersonalInformation
from src.core.entities.style import StyleCV


class BackgroundDrawCfg(BaseModel):
    color: tuple[float, float, float]
    page_width: float
    page_height: float


class PhotoDrawCfg(BaseModel):
    path_photo: Optional[Path]
    sizes_cv: SizesCV
    page_height: float
    is_photo_circle: bool = True
    draw_config: DrawCVConfig = Field(default_factory=DrawCVConfig)


class SidebarDrawCfg(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    linkedin_data: LinkedinData
    personal_information: PersonalInformation
    sizes_cv: SizesCV
    style_cv: StyleCV
    styles: StyleSheet1
    page_height: float
    draw_config: DrawCVConfig = Field(default_factory=DrawCVConfig)


class PositionsDrawCfg(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    linkedin_data: LinkedinData
    sizes_cv: SizesCV
    styles: StyleSheet1
    page_width: float
    page_height: float
    draw_config: DrawCVConfig = Field(default_factory=DrawCVConfig)

    @property
    def body_x(self) -> float:
        return self.sizes_cv.margin_left_pt + self.sizes_cv.column_left_width_pt + self.draw_config.sidebar_to_body_gap_mm * mm

    @property
    def line_anchor_x(self) -> float:
        return self.body_x + self.draw_config.dist_line_spacing_left_mm * mm

    @property
    def body_width(self) -> float:
        return self.page_width - self.body_x - self.sizes_cv.margin_pt

    @property
    def body_start_y(self) -> float:
        return self.page_height - self.sizes_cv.margin_pt

    @property
    def usable_height(self) -> float:
        return self.body_start_y - self.sizes_cv.margin_pt

    @property
    def icon_size_pt(self) -> float:
        return self.draw_config.len_python_icon_mm * mm


class DividerLine(BaseModel):
    x_start: float
    y_start: float
    x_end: float
    y_end: float

    @property
    def p1(self) -> tuple[float, float]:
        return self.x_start, self.y_start

    @property
    def p2(self) -> tuple[float, float]:
        return self.x_end, self.y_end


class DrawPositionsResult(BaseModel):
    divider_lines: list[DividerLine]
    line_anchor_x: float


class ImageDrawCfg(BaseModel):
    path_img: Path
    x: float
    y: float
    width: float
    height: float
    is_circle: bool = False

    @property
    def radius(self) -> float:
        return min(self.width, self.height) / 2

    @property
    def center_x(self) -> float:
        return self.x + (self.width / 2)

    @property
    def center_y(self) -> float:
        return self.y + (self.height / 2)


class ImageTitleDrawCfg(BaseModel):
    path_img: Path
    title_html: str
    img_size: float
    image_to_title_dist: float
