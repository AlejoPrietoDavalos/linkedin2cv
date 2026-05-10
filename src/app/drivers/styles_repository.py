from reportlab.lib.colors import Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1
from pydantic import BaseModel

from src.core.constants import ensure_runtime_config_file
from src.core.entities.styles_config import Alignment, StylesConfig


class _ParagraphStyleKwargs(BaseModel):
    name: str
    fontName: str
    fontSize: float
    leading: float
    textColor: tuple[float, float, float]
    alignment: Alignment | None = None
    spaceAfter: float | None = None

    def to_kwargs(self) -> dict:
        data = self.model_dump(exclude_none=True)
        data["textColor"] = Color(*data["textColor"])
        return data


class StylesRepository:
    @staticmethod
    def load() -> StylesConfig:
        path = ensure_runtime_config_file("styles.json")
        return StylesConfig.model_validate_json(path.read_text())

    @staticmethod
    def build_stylesheet(config: StylesConfig) -> StyleSheet1:
        styles = getSampleStyleSheet()
        for style in config.paragraph_styles:
            kwargs = _ParagraphStyleKwargs(
                name=style.name,
                fontName=config.font_name,
                fontSize=style.font_size,
                leading=style.leading,
                textColor=style.text_color,
                alignment=style.alignment,
                spaceAfter=style.space_after,
            )
            styles.add(ParagraphStyle(**kwargs.to_kwargs()))
        return styles
