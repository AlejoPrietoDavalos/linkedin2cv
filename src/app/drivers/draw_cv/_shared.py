"""Funciones y utilidades compartidas del servicio de dibujo."""

import re
from typing import List

from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import StyleSheet1


class SharedDrawUtils:
    def clean_text(self, text: str) -> str:
        cleaned_text = text.strip()
        cleaned_text = re.sub(r"^<br/>|<br/>$", "", cleaned_text)
        return cleaned_text

    def remove_https(self, url: str) -> str:
        return url.replace("https://", "")

    def sanitize_tech_summary(self, text: str) -> str:
        lines = [line.strip() for line in text.split("<br/>")]
        filtered: List[str] = []
        for line in lines:
            lower_line = line.lower()
            if not line:
                continue
            if "mi página web" in lower_line or "porfolio de proyectos" in lower_line:
                continue
            if "alejoprietodavalos.github.io/portfolio-es" in lower_line:
                continue
            filtered.append(line)
        return "<br/>".join(filtered)

    def draw_title_text_sidebar(
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
            Paragraph(self.clean_text(text), styles["SidebarText"]),
        ]
