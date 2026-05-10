from typing import List

from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import Paragraph, Spacer

from src.core.entities import DrawCVConfig, SidebarDrawCfg


class SidebarHeaderContentDrawer:
    def build(self, *, cfg: SidebarDrawCfg, styles: StyleSheet1, draw_config: DrawCVConfig) -> List[Paragraph | Spacer]:
        content: List[Paragraph | Spacer] = []
        content.append(Paragraph(cfg.linkedin_data.profile.full_name, styles["SidebarName"]))
        content.append(Spacer(1, draw_config.dist_full_name_to_headline))
        content.append(Paragraph(cfg.linkedin_data.profile.headline, styles["SidebarHeadline"]))
        content.append(Spacer(1, draw_config.dist_headline_to_links))
        return content
