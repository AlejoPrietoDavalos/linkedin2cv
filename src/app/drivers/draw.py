"""Implementación del servicio de dibujo de CV."""

from typing import Optional, List, Tuple
from pathlib import Path
import re

from pydantic import BaseModel, Field
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Frame, Spacer, Flowable
from reportlab.lib.styles import StyleSheet1, ParagraphStyle

from src.core.entities import LinkedinData, StyleCV, SizesCV, DrawCVConfig
from src.core.constants import PATH_PYTHON_ICON
from src.core.hardcoded_config import (
    SUMMARY_TECH_STACK_LABEL,
    LABEL_AGE,
    LABEL_GITHUB,
    LABEL_LINKEDIN,
    LABEL_LOCATION,
    LABEL_MAIL,
    SECTION_ABOUT_ME_TEXT,
    SECTION_ABOUT_ME_TITLE,
    SECTION_GOAL_TEXT,
    SECTION_GOAL_TITLE,
    SECTION_PROJECTS_TEXT,
    SECTION_PROJECTS_TITLE,
    SECTION_STACK_TITLE,
    SECTION_TECH_SUMMARY_TITLE,
    JOB_DESCRIPTION_FALLBACK,
    JOB_SUBTITLE_PREFIX,
    FINAL_CREDIT_TEXT,
    FINAL_CREDIT_URL,
    format_link_line,
    format_sidebar_info_line,
    format_website_line,
)
from src.core.drivers.draw import CoreDrawCVService


class DrawCVService(CoreDrawCVService):
    """Implementación del servicio de dibujo de CV."""
    
    def __init__(self, config: Optional[DrawCVConfig] = None):
        self.config = config or DrawCVConfig()

    @staticmethod
    def clean_text(text: str) -> str:
        cleaned_text = text.strip()
        cleaned_text = re.sub(r"^<br/>|<br/>$", "", cleaned_text)
        return cleaned_text

    @staticmethod
    def remove_https(url: str) -> str:
        return url.replace("https://", "")

    def draw_background(self, *, c: Canvas, color, page_width: int, page_height: int) -> None:
        c.setFillColor(color)
        c.rect(0, 0, page_width, page_height, fill=True, stroke=0)

    def draw_photo(
        self,
        *,
        c: Canvas,
        path_photo: Optional[Path],
        sizes_cv: SizesCV,
        page_height: int,
        is_photo_circle: bool = True,
    ) -> None:
        if path_photo and path_photo.exists():
            x = sizes_cv.margin_left + (sizes_cv.column_left_wifth - sizes_cv.photo_size) / 2
            y = page_height - sizes_cv.photo_size - self.config.photo_top_padding_mm * mm

            if is_photo_circle:
                radius = sizes_cv.photo_size / 2
                center_x = x + radius
                center_y = y + radius
                c.saveState()
                path = c.beginPath()
                path.circle(center_x, center_y, radius)
                c.clipPath(path, stroke=0)

            c.drawImage(
                str(path_photo),
                x,
                y,
                width=sizes_cv.photo_size,
                height=sizes_cv.photo_size,
                preserveAspectRatio=True,
                mask="auto",
            )

            if is_photo_circle:
                c.restoreState()

    def draw_title_text_sidebar(self, *, title: str, text: str, styles: StyleSheet1) -> List[Paragraph | Spacer]:
        return [
            Paragraph(f"<b>{title}</b>", styles["SidebarTitle"]),
            Spacer(1, self.config.dist_between_title_sidebar_to_text),
            Paragraph(self.clean_text(text), styles["SidebarText"]),
        ]

    def draw_sidebar(
        self,
        *,
        c: Canvas,
        linkedin_data: LinkedinData,
        sizes_cv: SizesCV,
        style_cv: StyleCV,
        styles: StyleSheet1,
        age: int,
        location: str,
        mail: str,
        page_height: int,
        url_website_es: Optional[str] = None,
        url_website_en: Optional[str] = None,
        url_github: Optional[str] = None,
        url_linkedin: Optional[str] = None,
    ) -> None:
        c.setFillColor(style_cv.sidebar_panel)
        c.rect(sizes_cv.margin_left, 0, sizes_cv.column_left_wifth, page_height, fill=True, stroke=0)

        photo_bottom = page_height - sizes_cv.photo_size - self.config.photo_top_padding_mm * mm
        sidebar_text_bottom = sizes_cv.margin + 5 * mm
        sidebar_height = photo_bottom - sidebar_text_bottom

        content = []
        content.append(Paragraph(linkedin_data.profile.full_name, styles["SidebarName"]))
        content.append(Spacer(1, self.config.dist_full_name_to_headline))
        content.append(Paragraph(linkedin_data.profile.headline, styles["SidebarHeadline"]))
        content.append(Spacer(1, self.config.dist_headline_to_links))

        info_lines = []
        if age:
            info_lines.append(format_sidebar_info_line(LABEL_AGE, str(age)))
        if location:
            info_lines.append(format_sidebar_info_line(LABEL_LOCATION, location))

        info_lines.append(format_sidebar_info_line(LABEL_MAIL, mail))

        if url_website_es and url_website_en:
            info_lines.append(format_website_line(url_es=url_website_es, url_en=url_website_en))
        else:
            raise ValueError(f"Falta una url - {url_website_es} - {url_website_en}")

        if url_github:
            info_lines.append(format_link_line(label=LABEL_GITHUB, url=url_github))
        if url_linkedin:
            info_lines.append(format_link_line(label=LABEL_LINKEDIN, url=url_linkedin))

        for line in info_lines:
            content.append(Paragraph(line, styles["SidebarLinks"]))
            content.append(Spacer(1, self.config.dist_between_links))

        if SUMMARY_TECH_STACK_LABEL not in linkedin_data.profile.summary:
            raise ValueError(f"El texto '{SUMMARY_TECH_STACK_LABEL}' no está en summary.")

        summary_parts = linkedin_data.profile.summary.split(SUMMARY_TECH_STACK_LABEL)
        summary_parts = [p.strip() for p in summary_parts]

        class SectionSidebar(BaseModel):
            title: str
            text: str

        class SectionsSidebar(BaseModel):
            sections: List[SectionSidebar] = Field(default_factory=list)

        sections = SectionsSidebar()
        sections.sections.append(
            SectionSidebar(
                title=SECTION_ABOUT_ME_TITLE,
                text=SECTION_ABOUT_ME_TEXT,
            )
        )
        sections.sections.append(
            SectionSidebar(
                title=SECTION_GOAL_TITLE,
                text=SECTION_GOAL_TEXT,
            )
        )
        sections.sections.append(SectionSidebar(title=SECTION_TECH_SUMMARY_TITLE, text=summary_parts[0]))
        sections.sections.append(
            SectionSidebar(
                title=SECTION_PROJECTS_TITLE,
                text=SECTION_PROJECTS_TEXT,
            )
        )
        sections.sections.append(SectionSidebar(title=SECTION_STACK_TITLE, text=summary_parts[1]))

        for section in sections.sections:
            content.append(Spacer(1, self.config.dist_between_title_text_sidebar))
            content.extend(self.draw_title_text_sidebar(title=section.title, text=section.text, styles=styles))

        frame = Frame(
            sizes_cv.margin_left + self.config.frame_margin_left_mm * mm,
            sidebar_text_bottom,
            sizes_cv.column_left_wifth - (self.config.frame_margin_left_mm + self.config.frame_margin_right_mm) * mm,
            sidebar_height,
            showBoundary=0,
        )

        frame.addFromList(content, c)

    def draw_positions(
        self,
        *,
        c: Canvas,
        linkedin_data: LinkedinData,
        sizes_cv: SizesCV,
        style_cv: StyleCV,
        styles: StyleSheet1,
        page_width: float,
        page_height: float,
        sidebar_args: dict,
    ) -> Tuple[List[Tuple[float, float, float, float]], float]:
        class IconTitle(Flowable):
            def __init__(self, img_path: Path, text: str, style: ParagraphStyle, img_size: float, icon_to_title_dist: float) -> None:
                super().__init__()
                self.img_path = img_path
                self.p = Paragraph(text, style)
                self.img_size = img_size
                self._height = 0
                self.icon_to_title_dist = icon_to_title_dist

            def wrap(self, availWidth: float, availHeight: float) -> Tuple[float, float]:
                text_w, text_h = self.p.wrap(
                    availWidth - self.img_size - self.icon_to_title_dist,
                    availHeight,
                )
                self._height = max(text_h, self.img_size)
                return text_w + self.img_size + self.icon_to_title_dist, self._height

            def draw(self) -> None:
                y_img = (self._height - self.img_size) / 2
                self.canv.drawImage(
                    str(self.img_path),
                    0,
                    y_img,
                    width=self.img_size,
                    height=self.img_size,
                    preserveAspectRatio=True,
                    mask="auto",
                )
                self.p.drawOn(
                    self.canv,
                    self.img_size + self.icon_to_title_dist,
                    (self._height - self.p.height) / 2,
                )

        cfg = self.config

        x = sizes_cv.margin_left + sizes_cv.column_left_wifth + cfg.sidebar_to_body_gap_mm * mm
        x_i = x + cfg.dist_line_spacing_left_mm * mm

        width = page_width - x - sizes_cv.margin
        y_cursor = page_height - sizes_cv.margin
        usable_height = y_cursor - sizes_cv.margin

        icon_size = cfg.len_python_icon_mm * mm
        lines: List[Tuple[float, float, float, float]] = []

        for idx, position in enumerate(linkedin_data.positions):
            icon = IconTitle(PATH_PYTHON_ICON, f"<b>{position.text_title}</b>", styles["JobTitle"], icon_size, cfg.dist_python_icon_to_title)
            _, h_icon = icon.wrap(width, usable_height)

            y_icon = y_cursor - h_icon

            subtitle = Paragraph(f"<b>{JOB_SUBTITLE_PREFIX} {position.text_sub_title}</b>", styles["JobSubTitle"])
            _, h_sub = subtitle.wrap(width, usable_height)
            desc = Paragraph(position.description or JOB_DESCRIPTION_FALLBACK, styles["JobDesc"])
            _, h_desc = desc.wrap(width, usable_height)

            block_height = h_icon + h_sub + h_desc + cfg.spacer_height + cfg.line_thickness

            if y_cursor - block_height < sizes_cv.margin:
                c.showPage()
                self.draw_background(c=c, color=style_cv.background, page_width=page_width, page_height=page_height)
                self.draw_sidebar(
                    c=c,
                    linkedin_data=linkedin_data,
                    sizes_cv=sizes_cv,
                    style_cv=style_cv,
                    styles=styles,
                    page_height=page_height,
                    **sidebar_args,
                )
                y_cursor = page_height - sizes_cv.margin
                y_icon = y_cursor - h_icon

            icon.drawOn(c, x, y_icon)
            y_cursor = y_icon - cfg.line_thickness
            subtitle.drawOn(c, x, y_cursor - h_sub)
            y_cursor -= h_sub + cfg.line_thickness
            desc.drawOn(c, x, y_cursor - h_desc)
            y_cursor -= h_desc + cfg.spacer_height

            if idx < len(linkedin_data.positions) - 1:
                y_line = y_icon
                lines.append(
                    (
                        x + cfg.dist_line_spacing_left_mm * mm,
                        y_line,
                        page_width - sizes_cv.margin - cfg.dist_line_spacing_right_mm * mm,
                        y_line,
                    )
                )

        final_text = Paragraph(
            f"""<br/><br/><br/><br/><br/><a href="{FINAL_CREDIT_URL}">\
            <i><b>{FINAL_CREDIT_TEXT}</b></i>\
            </a>""",
            styles["JobDesc"],
        )
        _, h_final = final_text.wrap(width, usable_height)
        final_text.drawOn(c, x, y_cursor - h_final)

        return lines, x_i
