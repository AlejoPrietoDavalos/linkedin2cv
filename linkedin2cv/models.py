from typing import Optional, List, Dict, Any
from pathlib import Path
import re

from pydantic import BaseModel
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.lib.units import mm


class Profile(BaseModel):
    first_name: str
    last_name: str
    #maiden_name
    #address
    #birth_date
    headline: str
    summary: str
    #industry
    #zip_code
    #geo_location
    #twitter_handles
    #websites
    #instant_messengers


class Position(BaseModel):
    company_name: str
    title: str
    description: str
    location: Optional[str]
    started_on: str
    finished_on: Optional[str]


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




def clean_multiline_strings(data: BaseModel) -> BaseModel:
    for field_name, value in data.__dict__.items():
        if isinstance(value, str):
            # 1. Limpiar espacios extras al inicio y al final
            cleaned = value.strip()

            # 2. Reemplazar dobles espacios por salto de línea
            cleaned = re.sub(r'  ', ' ', cleaned)

            # 3. Reemplazar "●" y "➣" por saltos de línea (<br/>)
            #cleaned = re.sub(r'●', '<br/>●', cleaned)
            cleaned = re.sub(r'➣', '<br/>➣', cleaned)

            # 4. Reemplazar saltos de línea (\n) por <br/>
            cleaned = re.sub(r'\r?\n', '<br/>', cleaned)

            # 5. Actualizar el valor en el campo
            setattr(data, field_name, cleaned)
        
        # Recursividad para casos donde los valores sean instancias de BaseModel
        elif isinstance(value, BaseModel):
            clean_multiline_strings(value)
        
        # Recursividad para listas que contienen instancias de BaseModel
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, BaseModel):
                    clean_multiline_strings(item)
    
    return data



def nan2none(v):
    return None if pd.isna(v) else v


def format_row_position(*, row: pd.Series) -> Dict[str, Any]:
    row_dict: Dict[str, Any] = row.to_dict()
    return {k.lower().replace(" ", "_"): nan2none(v) for k, v in row_dict.items()}


def load_profile(*, path_folder: Path) -> Profile:
    row = pd.read_csv(path_folder / "Profile.csv").iloc[0]
    return Profile(**format_row_position(row=row))


def load_positions(*, path_folder: Path) -> List[Position]:
    df = pd.read_csv(path_folder / "Positions.csv")
    return [Position(**format_row_position(row=row)) for _, row in df.iterrows()]


def load_educations(*, path_folder: Path) -> List[Education]:
    df = pd.read_csv(path_folder / "Education.csv")
    df["End Date"] = df["End Date"].apply(lambda t: None if pd.isna(t) else str(int(t)))
    return [Education(**format_row_position(row=row)) for _, row in df.iterrows()]


def load_linkedin_data(*, path_folder: Path) -> LinkedinData:
    data = LinkedinData(
        profile=load_profile(path_folder=path_folder),
        positions=load_positions(path_folder=path_folder),
        educations=load_educations(path_folder=path_folder)
    )
    return clean_multiline_strings(data)



class ColorsCV:
    def __init__(
            self,
            *,
            primary: str = "#4A4A4A",
            accent: str = "#7fabeb",
            text: str = "#ccd5e3",
            background: str = "#2F2F2F",
    ):
        self.primary: Color = colors.HexColor(primary)
        self.accent: Color = colors.HexColor(accent)
        self.text: Color = colors.HexColor(text)
        self.background: Color = colors.HexColor(background)

class SizesCV:
    def __init__(
            self,
            *,
            margin: int = 5,
            margin_left: int = 5,
            column_left_width: int = 65,
            photo_size: int = 30
    ):
        self.margin = margin * mm
        self.margin_left = margin_left * mm
        self.column_left_wifth = column_left_width * mm
        self.photo_size = photo_size * mm
