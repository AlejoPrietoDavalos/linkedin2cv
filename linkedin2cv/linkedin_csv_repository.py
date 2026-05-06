from typing import Optional, List, Dict, Any

import pandas as pd

from src.core.entities.linkedin_data import Profile, Position, Education, LinkedinData
from linkedin2cv.constants import (
    PATH_LINKEDIN_PROFILE,
    PATH_LINKEDIN_POSITIONS,
    PATH_LINKEDIN_EDUCATION,
)
from linkedin2cv.hardcoded_config import apply_visible_text_replacements


def _nan2none(v):
    return None if pd.isna(v) else v


def _read_dataframe(path_csv):
    return pd.read_csv(path_csv)


def _format_key_position(key: str) -> str:
    return key.lower().replace(" ", "_")


def _format_value_position(v: Optional[str]) -> Optional[str]:
    v = _nan2none(v)
    return apply_visible_text_replacements(v)


def _format_row_position(*, row: pd.Series) -> Dict[str, Any]:
    row_dict: Dict[str, Any] = row.to_dict()
    return {_format_key_position(k): _format_value_position(v) for k, v in row_dict.items()}


class LinkedinCSVRepository:
    def _load_profile(self) -> Profile:
        row = _read_dataframe(PATH_LINKEDIN_PROFILE).iloc[0]
        return Profile(**_format_row_position(row=row))

    def _load_positions(self) -> List[Position]:
        df = _read_dataframe(PATH_LINKEDIN_POSITIONS)
        return [Position(**_format_row_position(row=row)) for _, row in df.iterrows()]

    def _load_educations(self) -> List[Education]:
        df = _read_dataframe(PATH_LINKEDIN_EDUCATION)
        df["Start Date"] = df["Start Date"].apply(lambda t: None if pd.isna(t) else str(int(t)))
        df["End Date"] = df["End Date"].apply(lambda t: None if pd.isna(t) else str(int(t)))
        return [Education(**_format_row_position(row=row)) for _, row in df.iterrows()]

    def load_linkedin_data(self) -> LinkedinData:
        return LinkedinData(
            profile=self._load_profile(),
            positions=self._load_positions(),
            educations=self._load_educations(),
        )
