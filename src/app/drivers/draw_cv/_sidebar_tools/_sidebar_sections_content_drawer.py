from typing import List

from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import Paragraph, Spacer

from src.app.drivers.draw_cv._sidebar_tools._sidebar_section_text_drawer import SidebarSectionTextDrawer
from src.core.entities import DrawCVConfig, SidebarDrawCfg, SidebarSection, SidebarSections
from src.core.hardcoded_config import (
    SECTION_ABOUT_ME_TEXT,
    SECTION_ABOUT_ME_TITLE,
    SECTION_GOAL_TEXT,
    SECTION_GOAL_TITLE,
    SECTION_PROJECTS_TEXT,
    SECTION_PROJECTS_TITLE,
    SECTION_STACK_TITLE,
    SECTION_TECH_SUMMARY_TITLE,
    SUMMARY_TECH_STACK_LABEL,
)


class SidebarSectionsContentDrawer:
    def __init__(self, section_text_drawer: SidebarSectionTextDrawer | None = None) -> None:
        self.section_text_drawer = section_text_drawer or SidebarSectionTextDrawer()

    def _build_sections(self, *, cfg: SidebarDrawCfg) -> SidebarSections:
        if SUMMARY_TECH_STACK_LABEL not in cfg.linkedin_data.profile.summary:
            raise ValueError(f"El texto '{SUMMARY_TECH_STACK_LABEL}' no está en summary.")
        summary_parts = [p.strip() for p in cfg.linkedin_data.profile.summary.split(SUMMARY_TECH_STACK_LABEL)]
        return SidebarSections(
            items=[
                SidebarSection(title=SECTION_ABOUT_ME_TITLE, text=SECTION_ABOUT_ME_TEXT),
                SidebarSection(title=SECTION_GOAL_TITLE, text=SECTION_GOAL_TEXT),
                SidebarSection(title=SECTION_TECH_SUMMARY_TITLE, text=summary_parts[0]),
                SidebarSection(title=SECTION_PROJECTS_TITLE, text=SECTION_PROJECTS_TEXT),
                SidebarSection(title=SECTION_STACK_TITLE, text=summary_parts[1]),
            ]
        )

    def build(self, *, cfg: SidebarDrawCfg, styles: StyleSheet1, draw_config: DrawCVConfig) -> List[Paragraph | Spacer]:
        content: List[Paragraph | Spacer] = []
        for section in self._build_sections(cfg=cfg).items:
            content.append(Spacer(1, draw_config.dist_between_title_text_sidebar))
            content.extend(
                self.section_text_drawer.build(
                    title=section.title,
                    text=section.text,
                    styles=styles,
                    dist_between_title_sidebar_to_text=draw_config.dist_between_title_sidebar_to_text,
                )
            )
        return content
