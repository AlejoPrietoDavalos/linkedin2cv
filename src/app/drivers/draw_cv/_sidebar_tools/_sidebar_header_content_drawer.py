from typing import List

from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import Paragraph, Spacer

from src.core.entities.config import SpacingConfig
from src.core.entities.linkedin_data import LinkedInData


class SidebarHeaderContentDrawer:
    def build(self, *, linkedin_data: LinkedInData, styles: StyleSheet1, spacing: SpacingConfig) -> List[Paragraph | Spacer]:
        content: List[Paragraph | Spacer] = []
        content.append(Paragraph(linkedin_data.profile.full_name, styles["SidebarName"]))
        content.append(Spacer(1, spacing.dist_full_name_to_headline))
        content.append(Paragraph(linkedin_data.profile.headline, styles["SidebarHeadline"]))
        content.append(Spacer(1, spacing.dist_headline_to_links))
        return content
