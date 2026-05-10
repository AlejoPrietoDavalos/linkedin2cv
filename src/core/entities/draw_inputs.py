from pathlib import Path

from pydantic import BaseModel
from reportlab.lib.units import mm

from src.core.entities.config import LayoutConfig, SpacingConfig


class PositionsLayoutDTO(BaseModel):
    body_x: float
    line_anchor_x: float
    body_width: float
    body_start_y: float
    usable_height: float
    icon_size_pt: float

    @classmethod
    def from_config(cls, *, layout_cfg: LayoutConfig, spacing: SpacingConfig) -> "PositionsLayoutDTO":
        body_x = layout_cfg.margin_left_pt + layout_cfg.column_left_width_pt + spacing.sidebar_to_body_gap_mm * mm
        body_start_y = layout_cfg.page_height - layout_cfg.margin_pt
        return cls(
            body_x=body_x,
            line_anchor_x=body_x + spacing.dist_line_spacing_left_mm * mm,
            body_width=layout_cfg.page_width - body_x - layout_cfg.margin_pt,
            body_start_y=body_start_y,
            usable_height=body_start_y - layout_cfg.margin_pt,
            icon_size_pt=spacing.len_python_icon_mm * mm,
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
