from typing import List

from reportlab.platypus import Paragraph, Spacer

from src.core.entities import DrawCVConfig, SidebarDrawCfg
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
    def _build_info_lines(self, *, cfg: SidebarDrawCfg) -> list[str]:
        info_lines: list[str] = []
        if cfg.personal_information.age:
            info_lines.append(format_sidebar_info_line(LABEL_AGE, str(cfg.personal_information.age)))
        if cfg.personal_information.location:
            info_lines.append(format_sidebar_info_line(LABEL_LOCATION, cfg.personal_information.location))
        info_lines.append(format_sidebar_info_line(LABEL_MAIL, str(cfg.personal_information.email)))

        if cfg.personal_information.url_web_es and cfg.personal_information.url_web_en:
            info_lines.append(
                format_website_line(
                    url_es=cfg.personal_information.url_web_es,
                    url_en=cfg.personal_information.url_web_en,
                )
            )
        else:
            raise ValueError(f"Falta una url - {cfg.personal_information.url_web_es} - {cfg.personal_information.url_web_en}")

        if cfg.personal_information.url_github:
            info_lines.append(format_link_line(label=LABEL_GITHUB, url=cfg.personal_information.url_github))
        if cfg.personal_information.url_linkedin:
            info_lines.append(format_link_line(label=LABEL_LINKEDIN, url=cfg.personal_information.url_linkedin))
        return info_lines

    def build(self, *, cfg: SidebarDrawCfg, draw_config: DrawCVConfig) -> List[Paragraph | Spacer]:
        content: List[Paragraph | Spacer] = []
        for line in self._build_info_lines(cfg=cfg):
            content.append(Paragraph(line, cfg.styles["SidebarLinks"]))
            content.append(Spacer(1, draw_config.dist_between_links))
        return content
