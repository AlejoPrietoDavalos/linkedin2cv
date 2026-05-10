from typing import Optional, List, Dict, Any
import re
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


class _HardcodedLinkedinDataProcessor:
    """Processor for hardcoded LinkedIn data fixes.

    - Elimina la última posición de la lista.
    - Traduce las fechas de inicio de inglés a español.
    - Ajusta el trabajo freelance con nombre y formato especial.
    - Mantiene la modificación in-place, sin crear nuevos objetos.
    """

    def __init__(self, in_spanish: bool = True):
        self.in_spanish = in_spanish

    def process(self, linkedin_data: LinkedinData) -> None:
        self._strip_last_position(linkedin_data)
        self._translate_dates(linkedin_data)
        self._apply_freelance_adjustments(linkedin_data)

    def _strip_last_position(self, linkedin_data: LinkedinData) -> None:
        # FIXME: Recontra hardcodeado
        linkedin_data.positions = linkedin_data.positions[:-1]

    def _translate_dates(self, linkedin_data: LinkedinData) -> None:
        if not self.in_spanish:
            return
        for position in linkedin_data.positions:
            position.started_on = self._translate_date(position.started_on)
            position.finished_on = self._translate_date(position.finished_on)

    def _apply_freelance_adjustments(self, linkedin_data: LinkedinData) -> None:
        IDX_FREELANCE = 1
        if len(linkedin_data.positions) <= IDX_FREELANCE:
            return
        linkedin_data.positions[IDX_FREELANCE].company_name = "Profesional independiente"
        desc = self._move_bracketed_to_end(linkedin_data.positions[IDX_FREELANCE].description)
        desc = self._put_bold_in_brackets(desc)
        linkedin_data.positions[IDX_FREELANCE].description = desc

    @staticmethod
    def _translate_date(date_str: Optional[str]) -> Optional[str]:
        month_map = {
            "Jan": "Enero",
            "Feb": "Febrero",
            "Mar": "Marzo",
            "Apr": "Abril",
            "May": "Mayo",
            "Jun": "Junio",
            "Jul": "Julio",
            "Aug": "Agosto",
            "Sep": "Septiembre",
            "Oct": "Octubre",
            "Nov": "Noviembre",
            "Dec": "Diciembre",
        }
        if not date_str:
            return None
        parts = date_str.split()
        if len(parts) == 2 and parts[0] in month_map:
            return f"{month_map[parts[0]]} {parts[1]}"
        return date_str

    @staticmethod
    def _put_bold_in_brackets(text: str) -> str:
        return re.sub(r"(\[[^\]]+\])", r"<b>\1</b>", text)

    @staticmethod
    def _move_bracketed_to_end(text: str) -> str:
        def replacer(line: str) -> str:
            matches = re.findall(r"\[[^\]]+\]", line)
            line_clean = re.sub(r"\[[^\]]+\]", "", line).strip()
            if not matches:
                return line
            bracketed = " ".join(matches)
            if "<br" in line:
                return re.sub(r"(.*?)(<br\s*/?>)", rf"\1 {bracketed}\2", line_clean + "<br/>")
            return f"{line_clean} {bracketed}"

        lines = text.split("<br/>")
        processed = [replacer(line) for line in lines if line.strip()]
        processed = [txt if not txt.startswith("●") else f"<br/>{txt}" for txt in processed]
        return "<br/>".join(processed)


class LinkedinCSVRepository(CoreLinkedinCSVRepository):
    def __init__(self) -> None:
        ...

    def _load_profile(self) -> Profile:
        row = _read_dataframe(PATH_LINKEDIN_PROFILE).iloc[0]
        return Profile(**_LinkedinRowFormatter.format_row(row=row))

    def _load_positions(self) -> List[Position]:
        df = _read_dataframe(PATH_LINKEDIN_POSITIONS)
        return [Position(**_LinkedinRowFormatter.format_row(row=row)) for _, row in df.iterrows()]

    def _load_educations(self) -> List[Education]:
        df = _read_dataframe(PATH_LINKEDIN_EDUCATION)
        df["Start Date"] = df["Start Date"].apply(lambda t: None if pd.isna(t) else str(int(t)))
        df["End Date"] = df["End Date"].apply(lambda t: None if pd.isna(t) else str(int(t)))
        return [Education(**_LinkedinRowFormatter.format_row(row=row)) for _, row in df.iterrows()]

    def load_linkedin_data(self) -> LinkedinData:
        linkedin_data = LinkedinData(
            profile=self._load_profile(),
            positions=self._load_positions(),
            educations=self._load_educations(),
        )
        _HardcodedLinkedinDataProcessor().process(linkedin_data)
        logger.info("==================== LinkedIn Data ====================")
        logger.info(f"~ positions={len(linkedin_data.positions)}")
        logger.info(f"~ educations={len(linkedin_data.educations)}")
        return linkedin_data
