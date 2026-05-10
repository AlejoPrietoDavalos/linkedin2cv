from typing import List

from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import Paragraph, Spacer

from src.core.entities.config import SpacingConfig
from src.core.entities.personal_information import PersonalInformation
from src.core.hardcoded_config import (
    LABEL_AGE,
    LABEL_GITHUB,
    LABEL_LINKEDIN,
    LABEL_LOCATION,
    LABEL_MAIL,
    format_link_line,
    format_sidebar_info_line,
    format_website_line,
)


class SidebarPersonalInfoContentDrawer:
    def _build_info_lines(self, *, personal_information: PersonalInformation) -> list[str]:
        info_lines: list[str] = []
        if personal_information.age:
            info_lines.append(format_sidebar_info_line(LABEL_AGE, str(personal_information.age)))
        if personal_information.location:
            info_lines.append(format_sidebar_info_line(LABEL_LOCATION, personal_information.location))
        info_lines.append(format_sidebar_info_line(LABEL_MAIL, str(personal_information.email)))

        if personal_information.url_web_es and personal_information.url_web_en:
            info_lines.append(
                format_website_line(
                    url_es=personal_information.url_web_es,
                    url_en=personal_information.url_web_en,
                )
            )
        else:
            raise ValueError(f"Falta una url - {personal_information.url_web_es} - {personal_information.url_web_en}")

        if personal_information.url_github:
            info_lines.append(format_link_line(label=LABEL_GITHUB, url=personal_information.url_github))
        if personal_information.url_linkedin:
            info_lines.append(format_link_line(label=LABEL_LINKEDIN, url=personal_information.url_linkedin))
        return info_lines

    def build(self, *, personal_information: PersonalInformation, styles: StyleSheet1, spacing: SpacingConfig) -> List[Paragraph | Spacer]:
        content: List[Paragraph | Spacer] = []
        for line in self._build_info_lines(personal_information=personal_information):
            content.append(Paragraph(line, styles["SidebarLinks"]))
            content.append(Spacer(1, spacing.dist_between_links))
        return content
