from typing import List

from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import Paragraph, Spacer


class SidebarSectionTextDrawer:
    def build(
        self,
        *,
        title: str,
        text: str,
        styles: StyleSheet1,
        dist_between_title_sidebar_to_text: int,
    ) -> List[Paragraph | Spacer]:
        return [
            Paragraph(f"<b>{title}</b>", styles["SidebarTitle"]),
            Spacer(1, dist_between_title_sidebar_to_text),
            Paragraph(text, styles["SidebarText"]),
        ]
