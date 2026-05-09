from typing import Optional, List

from pydantic import BaseModel
from src.core.hardcoded_config import format_full_name, format_full_name_inverted, format_position_subtitle


class Profile(BaseModel):
    first_name: str
    last_name: str
    headline: str
    summary: str

    @property
    def full_name(self) -> str:
        return format_full_name(first_name=self.first_name, last_name=self.last_name)

    @property
    def full_name_inverted(self) -> str:
        return format_full_name_inverted(first_name=self.first_name, last_name=self.last_name)


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
        return format_position_subtitle(
            company_name=self.company_name,
            started_on=self.started_on,
            finished_on=self.finished_on,
        )


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
