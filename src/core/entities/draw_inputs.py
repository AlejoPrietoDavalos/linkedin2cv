from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from reportlab.lib.units import mm

from src.core.entities.config import DrawCVConfig, SizesCV
from src.core.entities.linkedin_data import LinkedInData
from src.core.entities.personal_information import PersonalInformation
from src.core.entities.styles_config import StylesConfig


class SidebarDrawCfg(BaseModel):
    linkedin_data: LinkedInData
    personal_information: PersonalInformation
    path_photo: Path
    is_photo_circle: bool = True
    sizes_cv: SizesCV
    styles_config: StylesConfig


class PositionsDrawCfg(BaseModel):
    linkedin_data: LinkedInData
    sizes_cv: SizesCV


class PositionsLayoutDTO(BaseModel):
    body_x: float
    line_anchor_x: float
    body_width: float
    body_start_y: float
    usable_height: float
    icon_size_pt: float

    @classmethod
    def from_positions_and_draw_config(cls, *, positions_cfg: PositionsDrawCfg, draw_config: DrawCVConfig) -> "PositionsLayoutDTO":
        body_x = positions_cfg.sizes_cv.margin_left_pt + positions_cfg.sizes_cv.column_left_width_pt + draw_config.sidebar_to_body_gap_mm * mm
        body_start_y = positions_cfg.sizes_cv.page_height - positions_cfg.sizes_cv.margin_pt
        return cls(
            body_x=body_x,
            line_anchor_x=body_x + draw_config.dist_line_spacing_left_mm * mm,
            body_width=positions_cfg.sizes_cv.page_width - body_x - positions_cfg.sizes_cv.margin_pt,
            body_start_y=body_start_y,
            usable_height=body_start_y - positions_cfg.sizes_cv.margin_pt,
            icon_size_pt=draw_config.len_python_icon_mm * mm,
        )


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
