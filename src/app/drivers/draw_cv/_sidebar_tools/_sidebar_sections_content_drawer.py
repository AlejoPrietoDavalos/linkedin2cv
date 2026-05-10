from typing import List

from pydantic import BaseModel
from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import Paragraph, Spacer

from src.app.drivers.draw_cv._sidebar_tools._sidebar_section_text_drawer import SidebarSectionTextDrawer
from src.core.entities.config import SpacingConfig
from src.core.entities.linkedin_data import LinkedInData
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


class SidebarSection(BaseModel):
    title: str
    text: str


class SidebarSections(BaseModel):
    items: list[SidebarSection]


class SidebarSectionsContentDrawer:
    def __init__(self, section_text_drawer: SidebarSectionTextDrawer | None = None) -> None:
        self.section_text_drawer = section_text_drawer or SidebarSectionTextDrawer()

    def _build_sections(self, *, linkedin_data: LinkedInData) -> SidebarSections:
        if SUMMARY_TECH_STACK_LABEL not in linkedin_data.profile.summary:
            raise ValueError(f"El texto '{SUMMARY_TECH_STACK_LABEL}' no está en summary.")
        summary_parts = [p.strip() for p in linkedin_data.profile.summary.split(SUMMARY_TECH_STACK_LABEL)]
        return SidebarSections(
            items=[
                SidebarSection(title=SECTION_ABOUT_ME_TITLE, text=SECTION_ABOUT_ME_TEXT),
                SidebarSection(title=SECTION_GOAL_TITLE, text=SECTION_GOAL_TEXT),
                SidebarSection(title=SECTION_TECH_SUMMARY_TITLE, text=summary_parts[0]),
                SidebarSection(title=SECTION_PROJECTS_TITLE, text=SECTION_PROJECTS_TEXT),
                SidebarSection(title=SECTION_STACK_TITLE, text=summary_parts[1]),
            ]
        )

    def build(self, *, linkedin_data: LinkedInData, styles: StyleSheet1, spacing: SpacingConfig) -> List[Paragraph | Spacer]:
        content: List[Paragraph | Spacer] = []
        for section in self._build_sections(linkedin_data=linkedin_data).items:
            content.append(Spacer(1, spacing.dist_between_title_text_sidebar))
            content.extend(
                self.section_text_drawer.build(
                    title=section.title,
                    text=section.text,
                    styles=styles,
                    dist_between_title_sidebar_to_text=spacing.dist_between_title_sidebar_to_text,
                )
            )
        return content
