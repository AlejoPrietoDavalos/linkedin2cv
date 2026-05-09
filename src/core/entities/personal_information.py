from datetime import date
from typing import Optional

from pydantic import ConfigDict, EmailStr, Field
from pydantic_settings import BaseSettings


class PersonalInformation(BaseSettings):
    birthday_yyyy_mm_dd: date = Field(validation_alias="BIRTHDAY")
    location: str
    email: EmailStr
    url_web_es: Optional[str] = None
    url_web_en: Optional[str] = None
    url_github: Optional[str] = None
    url_linkedin: Optional[str] = None

    @property
    def age(self) -> int:
        today = date.today()
        years = today.year - self.birthday_yyyy_mm_dd.year
        has_had_birthday = (today.month, today.day) >= (
            self.birthday_yyyy_mm_dd.month,
            self.birthday_yyyy_mm_dd.day,
        )
        return years if has_had_birthday else years - 1

    model_config = ConfigDict(
        env_prefix="",
        str_strip_whitespace=True,
    )
