from reportlab.lib.colors import Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1
from pydantic import BaseModel, ConfigDict, Field

from src.core.constants import ensure_runtime_config_file
from src.core.entities.config import LayoutConfig, SidebarSectionsCfg, SpacingConfig
from src.core.entities.styles_config import Alignment, StylesConfig


def _hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255
    g = int(hex_color[2:4], 16) / 255
    b = int(hex_color[4:6], 16) / 255
    return (r, g, b)


class _ParagraphStyleKwargs(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    font_name: str = Field(alias="fontName")
    font_size: float = Field(alias="fontSize")
    leading: float
    text_color: tuple[float, float, float] = Field(alias="textColor")
    alignment: Alignment | None = None
    space_after: float | None = Field(None, alias="spaceAfter")

    def to_kwargs(self) -> dict:
        data = self.model_dump(by_alias=True, exclude_none=True)
        data["textColor"] = Color(*data["textColor"])
        return data


class StylesRepository:
    @staticmethod
    def load() -> StylesConfig:
        path = ensure_runtime_config_file("styles.json")
        return StylesConfig.model_validate_json(path.read_text())

    @staticmethod
    def build_stylesheet(config: StylesConfig, font_name: str) -> StyleSheet1:
        styles = getSampleStyleSheet()
        for style in config.paragraph_styles:
            kwargs = _ParagraphStyleKwargs(
                name=style.name,
                fontName=font_name,
                fontSize=style.font_size,
                leading=style.leading,
                textColor=_hex_to_rgb(style.text_color),
                alignment=style.alignment,
                spaceAfter=style.space_after,
            )
            styles.add(ParagraphStyle(**kwargs.to_kwargs()))
        return styles


class LayoutRepository:
    @staticmethod
    def load() -> LayoutConfig:
        path = ensure_runtime_config_file("layout.json")
        return LayoutConfig.model_validate_json(path.read_text())


class SpacingRepository:
    @staticmethod
    def load() -> SpacingConfig:
        path = ensure_runtime_config_file("spacing.json")
        return SpacingConfig.model_validate_json(path.read_text())


class SidebarSectionsRepository:
    @staticmethod
    def load() -> SidebarSectionsCfg:
        path = ensure_runtime_config_file("sidebar_sections.json")
        return SidebarSectionsCfg.model_validate_json(path.read_text())
