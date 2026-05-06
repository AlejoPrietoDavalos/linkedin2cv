from typing import Optional, List

from pydantic import BaseModel

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
