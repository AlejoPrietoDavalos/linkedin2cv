from typing import Optional
import os

from pydantic import BaseModel, EmailStr


class PersonalInformation(BaseModel):
    age: int
    location: str
    email: EmailStr
    url_web_es: Optional[str] = None
    url_web_en: Optional[str] = None
    url_github: Optional[str] = None
    url_linkedin: Optional[str] = None

    @classmethod
    def from_env(cls) -> "PersonalInformation":
        return cls(
            age=os.getenv("AGE"),
            location=os.getenv("LOCATION"),
            email=os.getenv("EMAIL"),
            url_web_es=os.getenv("URL_WEB_ES"),
            url_web_en=os.getenv("URL_WEB_EN"),
            url_github=os.getenv("URL_GITHUB"),
            url_linkedin=os.getenv("URL_LINKEDIN"),
        )
