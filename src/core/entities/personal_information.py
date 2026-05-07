from typing import Optional

from pydantic import ConfigDict, EmailStr
from pydantic_settings import BaseSettings


class PersonalInformation(BaseSettings):
    age: int
    location: str
    email: EmailStr
    url_web_es: Optional[str] = None
    url_web_en: Optional[str] = None
    url_github: Optional[str] = None
    url_linkedin: Optional[str] = None

    model_config = ConfigDict(
        env_prefix="",
        str_strip_whitespace=True,
    )
