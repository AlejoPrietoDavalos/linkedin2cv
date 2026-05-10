from typing import Optional, List, Dict, Any, Type
import logging

import pandas as pd

from src.core.entities.linkedin_data import Profile, Position, Education, LinkedinData
from src.core.constants import (
    PATH_LINKEDIN_PROFILE,
    PATH_LINKEDIN_POSITIONS,
    PATH_LINKEDIN_EDUCATION,
)
from src.core.drivers.linkedin_csv_repository import CoreLinkedinCSVRepository
from src.core.hardcoded_config import (
    REPLACE_BULLET_ARROW,
    REPLACE_BULLET_DOT,
    REPLACE_BULLET_SQUARE,
)

logger = logging.getLogger(__name__)


def _nan2none(v):
    return None if pd.isna(v) else v


def _read_dataframe(path_csv):
    return pd.read_csv(path_csv)


def _apply_visible_text_replacements(value: Optional[str]) -> Optional[str]:
    if not isinstance(value, str):
        return value
    value = value.replace(*REPLACE_BULLET_ARROW)
    value = value.replace(*REPLACE_BULLET_DOT)
    value = value.replace(*REPLACE_BULLET_SQUARE)
    return value


class _LinkedinRowFormatter:
    @staticmethod
    def format_key(key: str) -> str:
        return key.lower().replace(" ", "_")

    @staticmethod
    def format_value(v: Optional[str]) -> Optional[str]:
        v = _nan2none(v)
        return _apply_visible_text_replacements(v)

    @staticmethod
    def format_row(*, row: pd.Series) -> Dict[str, Any]:
        row_dict: Dict[str, Any] = row.to_dict()
        return {
            _LinkedinRowFormatter.format_key(k): _LinkedinRowFormatter.format_value(v)
            for k, v in row_dict.items()
        }


def _pick_model_fields(data: Dict[str, Any], model_cls: Type) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if k in model_cls.model_fields}


class LinkedinCSVRepository(CoreLinkedinCSVRepository):
    def __init__(self) -> None:
        ...

    def _load_profile(self) -> Profile:
        row = _read_dataframe(PATH_LINKEDIN_PROFILE).iloc[0]
        data = _LinkedinRowFormatter.format_row(row=row)
        return Profile(**_pick_model_fields(data, Profile))

    def _load_positions(self) -> List[Position]:
        df = _read_dataframe(PATH_LINKEDIN_POSITIONS)
        return [
            Position(**_pick_model_fields(_LinkedinRowFormatter.format_row(row=row), Position))
            for _, row in df.iterrows()
        ]

    def _load_educations(self) -> List[Education]:
        df = _read_dataframe(PATH_LINKEDIN_EDUCATION)
        df["Start Date"] = df["Start Date"].apply(lambda t: None if pd.isna(t) else str(int(t)))
        df["End Date"] = df["End Date"].apply(lambda t: None if pd.isna(t) else str(int(t)))
        return [
            Education(**_pick_model_fields(_LinkedinRowFormatter.format_row(row=row), Education))
            for _, row in df.iterrows()
        ]

    def load_linkedin_data(self) -> LinkedinData:
        linkedin_data = LinkedinData(
            profile=self._load_profile(),
            positions=self._load_positions(),
            educations=self._load_educations(),
        )
        logger.info("==================== LinkedIn Data ====================")
        logger.info(f"~ positions={len(linkedin_data.positions)}")
        logger.info(f"~ educations={len(linkedin_data.educations)}")
        return linkedin_data
