from typing import Optional

from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import mm

from .config import StyleCVConfig

FONT = "HackNerdFont"


class StyleCV:
    def __init__(self, config: Optional[StyleCVConfig] = None):
        config = config or StyleCVConfig()
        self.sidebar_panel: Color = colors.HexColor(config.sidebar_panel)
        self.accent: Color = colors.HexColor(config.accent)
        self.text: Color = colors.HexColor(config.text)
        self.background: Color = colors.HexColor(config.background)
        self.sidebar_text: Color = colors.HexColor(config.sidebar_text)

    def get_styles(self) -> StyleSheet1:
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="Header", fontName=FONT, fontSize=25, leading=24, alignment=TA_LEFT, textColor=self.accent))
        styles.add(ParagraphStyle(name="SubHeader", fontName=FONT, fontSize=6, leading=16, alignment=TA_LEFT, textColor=self.sidebar_text))
        styles.add(ParagraphStyle(name="JobTitle", fontName=FONT, fontSize=11, leading=14, textColor=self.accent, spaceAfter=4))
        styles.add(ParagraphStyle(name="JobSubTitle", fontName=FONT, fontSize=8, leading=14, textColor=self.accent, spaceAfter=4))
        styles.add(ParagraphStyle(name="JobDesc", fontName=FONT, fontSize=7, leading=12, textColor=self.text))
        styles.add(ParagraphStyle(name="SidebarName", fontName=FONT, fontSize=15, leading=12, textColor=self.sidebar_text, alignment=TA_CENTER))
        styles.add(ParagraphStyle(name="SidebarHeadline", fontName=FONT, fontSize=7, leading=10, textColor=self.sidebar_text, alignment=TA_CENTER, spaceAfter=4))
        styles.add(ParagraphStyle(name="SidebarTitle", fontName=FONT, fontSize=10, leading=10, textColor=self.sidebar_text, alignment=TA_LEFT))
        styles.add(ParagraphStyle(name="SidebarText", fontName=FONT, fontSize=6, leading=10, textColor=self.sidebar_text, alignment=TA_LEFT))
        styles.add(ParagraphStyle(name="SidebarLinks", fontName=FONT, fontSize=6, leading=9, textColor=self.sidebar_text, alignment=TA_LEFT))
        return styles


class SizesCV:
    def __init__(
        self,
        *,
        margin: int = 5,
        margin_left: int = 5,
        column_left_width: int = 70,
        photo_size: int = 30,
    ):
        self.margin = margin * mm
        self.margin_left = margin_left * mm
        self.column_left_wifth = column_left_width * mm
        self.photo_size = photo_size * mm
