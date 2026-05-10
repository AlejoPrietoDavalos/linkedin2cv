from typing import Literal, Optional

from pydantic import BaseModel

# Reportlab text alignment constants
Alignment = Literal[
    0,  # TA_LEFT
    1,  # TA_CENTER
    2,  # TA_RIGHT
    4,  # TA_JUSTIFY
]


class ParagraphStyleParams(BaseModel):
    name: str
    font_size: float
    leading: float
    text_color: str
    alignment: Optional[Alignment] = None
    space_after: Optional[float] = None


class StylesConfig(BaseModel):
    sidebar_panel: str
    background: str
    paragraph_styles: list[ParagraphStyleParams]
