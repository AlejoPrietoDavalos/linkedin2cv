from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ConfigDict
from reportlab.lib.styles import StyleSheet1
from reportlab.lib.units import mm

from src.core.entities.config import DrawCVConfig, SizesCV
from src.core.entities.linkedin_data import LinkedinData
from src.core.entities.personal_information import PersonalInformation


class BackgroundDrawCfg(BaseModel):
    color: tuple[float, float, float]
    page_width: float
    page_height: float


class SidebarDrawCfg(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    linkedin_data: LinkedinData
    personal_information: PersonalInformation
    path_photo: Path
    is_photo_circle: bool = True
    sizes_cv: SizesCV
    sidebar_panel_color: tuple[float, float, float]
    styles: StyleSheet1
    page_height: float


class PositionsDrawCfg(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    linkedin_data: LinkedinData
    sizes_cv: SizesCV
    styles: StyleSheet1
    page_width: float
    page_height: float


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
        body_start_y = positions_cfg.page_height - positions_cfg.sizes_cv.margin_pt
        return cls(
            body_x=body_x,
            line_anchor_x=body_x + draw_config.dist_line_spacing_left_mm * mm,
            body_width=positions_cfg.page_width - body_x - positions_cfg.sizes_cv.margin_pt,
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
