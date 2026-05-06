from pathlib import Path
from typing import Optional, List, Dict, Any

import pandas as pd

from linkedin2cv.models.linkedin_data import Profile, Position, Education, LinkedinData
from linkedin2cv.constants import (
    PATH_LINKEDIN_PROFILE,
    PATH_LINKEDIN_POSITIONS,
    PATH_LINKEDIN_EDUCATION,
)
from linkedin2cv.hardcoded_config import apply_visible_text_replacements


def nan2none(v):
    return None if pd.isna(v) else v


def format_value(v: Optional[str]) -> Optional[str]:
    v = nan2none(v)
    return apply_visible_text_replacements(v)


def format_row_position(*, row: pd.Series) -> Dict[str, Any]:
    row_dict: Dict[str, Any] = row.to_dict()
    return {k.lower().replace(" ", "_"): format_value(v) for k, v in row_dict.items()}


def load_profile(*, path_folder: Path) -> Profile:
    path_profile = path_folder / PATH_LINKEDIN_PROFILE
    row = pd.read_csv(path_profile).iloc[0]
    return Profile(**format_row_position(row=row))


def load_positions(*, path_folder: Path) -> List[Position]:
    path_positions = path_folder / PATH_LINKEDIN_POSITIONS
    df = pd.read_csv(path_positions)
    return [Position(**format_row_position(row=row)) for _, row in df.iterrows()]


def load_educations(*, path_folder: Path) -> List[Education]:
    path_education = path_folder / PATH_LINKEDIN_EDUCATION
    df = pd.read_csv(path_education)
    df["Start Date"] = df["Start Date"].apply(lambda t: None if pd.isna(t) else str(int(t)))
    df["End Date"] = df["End Date"].apply(lambda t: None if pd.isna(t) else str(int(t)))
    return [Education(**format_row_position(row=row)) for _, row in df.iterrows()]


def load_linkedin_data(*, path_folder: Path) -> LinkedinData:
    return LinkedinData(
        profile=load_profile(path_folder=path_folder),
        positions=load_positions(path_folder=path_folder),
        educations=load_educations(path_folder=path_folder),
    )
