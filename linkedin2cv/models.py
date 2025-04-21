from typing import Optional, List, Dict, Any
from pathlib import Path

from pydantic import BaseModel
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.lib.units import mm

ACTUALIDAD = "Actualidad"


class Profile(BaseModel):
    first_name: str
    last_name: str
    headline: str
    summary: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Position(BaseModel):
    company_name: str
    title: str
    description: str
    location: Optional[str]
    started_on: str
    finished_on: Optional[str]

    @property
    def text_title(self) -> str:
        return self.title

    @property
    def text_sub_title(self) -> str:
        return f"{self.company_name} ({self.started_on} ~ {self.finished_on or ACTUALIDAD})"


class Education(BaseModel):
    school_name: str
    start_date: str
    end_date: Optional[str]
    notes: Optional[str]
    degree_name: str
    activities: Optional[str]


class LinkedinData(BaseModel):
    profile: Profile
    positions: List[Position]
    educations: List[Education]


def nan2none(v):
    return None if pd.isna(v) else v

def format_value(v: Optional[str]) -> Optional[str]:
    v = nan2none(v)
    if isinstance(v, str):
        v = v.replace(" ➣", "<br/>➣")
        v = v.replace(" ●", "<br/><br/>●")
        v = v.replace(" ■", "<br/>■")
    return v

def format_row_position(*, row: pd.Series) -> Dict[str, Any]:
    row_dict: Dict[str, Any] = row.to_dict()
    return {k.lower().replace(" ", "_"): format_value(v) for k, v in row_dict.items()}


def load_profile(*, path_folder: Path) -> Profile:
    row = pd.read_csv(path_folder / "Profile.csv").iloc[0]
    return Profile(**format_row_position(row=row))


def load_positions(*, path_folder: Path) -> List[Position]:
    df = pd.read_csv(path_folder / "Positions.csv")
    return [Position(**format_row_position(row=row)) for _, row in df.iterrows()]


def load_educations(*, path_folder: Path) -> List[Education]:
    df = pd.read_csv(path_folder / "Education.csv")
    df["Start Date"] = df["Start Date"].apply(lambda t: None if pd.isna(t) else str(int(t)))
    df["End Date"] = df["End Date"].apply(lambda t: None if pd.isna(t) else str(int(t)))
    return [Education(**format_row_position(row=row)) for _, row in df.iterrows()]


def load_linkedin_data(*, path_folder: Path) -> LinkedinData:
    return LinkedinData(
        profile=load_profile(path_folder=path_folder),
        positions=load_positions(path_folder=path_folder),
        educations=load_educations(path_folder=path_folder)
    )

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1
from reportlab.lib.enums import TA_LEFT, TA_CENTER
FONT = "HackNerdFont"

class StyleCV:
    def __init__(
            self,
            *,
            sidebar_panel: str = "#4d4d4d",
            accent: str = "#2F2F2F",#"#b4ceed",
            text: str = "#4A4A4A",
            background: str = "#dddddd",
            sidebar_text: str = "#dddddd",
    ):
        self.sidebar_panel: Color = colors.HexColor(sidebar_panel)
        self.accent: Color = colors.HexColor(accent)
        self.text: Color = colors.HexColor(text)
        self.background: Color = colors.HexColor(background)
        self.sidebar_text: Color = colors.HexColor(sidebar_text)

    def get_styles(self) -> StyleSheet1:
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="Header", fontName=FONT, fontSize=25, leading=24, alignment=TA_LEFT, textColor=self.accent))
        styles.add(ParagraphStyle(name="SubHeader", fontName=FONT, fontSize=6, leading=16, alignment=TA_LEFT, textColor=self.sidebar_text))
        styles.add(ParagraphStyle(name="JobTitle", fontName=FONT, fontSize=11, leading=14, textColor=self.accent, spaceAfter=4))
        styles.add(ParagraphStyle(name="JobSubTitle", fontName=FONT, fontSize=8, leading=14, textColor=self.accent, spaceAfter=4))
        styles.add(ParagraphStyle(name="JobDesc", fontName=FONT, fontSize=7, leading=12, textColor=self.text))
        styles.add(ParagraphStyle(name="SidebarName", fontName=FONT, fontSize=12, leading=12, textColor=self.sidebar_text, alignment=TA_CENTER))
        styles.add(ParagraphStyle(name="SidebarHeadline", fontName=FONT, fontSize=8, leading=10,textColor=self.sidebar_text, alignment=TA_CENTER, spaceAfter=4))
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
            photo_size: int = 30
    ):
        self.margin = margin * mm
        self.margin_left = margin_left * mm
        self.column_left_wifth = column_left_width * mm
        self.photo_size = photo_size * mm
