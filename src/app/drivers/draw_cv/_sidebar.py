"""Render de sidebar y foto del CV."""

from typing import List

from pydantic import BaseModel, Field
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame, Paragraph, Spacer

from src.app.drivers.draw_cv._image import ImageDrawer
from src.app.drivers.draw_cv._shared import SharedDrawUtils
from src.core.entities import ImageDrawCfg, PhotoDrawCfg, SidebarDrawCfg
from src.core.hardcoded_config import (
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
    SUMMARY_TECH_STACK_LABEL,
    format_link_line,
    format_sidebar_info_line,
    format_website_line,
)


class SidebarDrawer:
    def __init__(self, shared_utils: SharedDrawUtils, image_drawer: ImageDrawer) -> None:
        self.shared_utils = shared_utils
        self.image_drawer = image_drawer

    def draw_photo(
        self,
        *,
        c: Canvas,
        cfg: PhotoDrawCfg,
    ) -> None:
        if cfg.path_photo and cfg.path_photo.exists():
            x = cfg.sizes_cv.margin_left_pt + (cfg.sizes_cv.column_left_width_pt - cfg.sizes_cv.photo_size_pt) / 2
            y = cfg.page_height - cfg.sizes_cv.photo_size_pt - cfg.draw_config.photo_top_padding_mm * mm

            if cfg.is_photo_circle:
                self.image_drawer.draw_image(
                    c=c,
                    cfg=ImageDrawCfg(
                        path_img=cfg.path_photo,
                        x=x,
                        y=y,
                        width=cfg.sizes_cv.photo_size_pt,
                        height=cfg.sizes_cv.photo_size_pt,
                        is_circle=True,
                    ),
                )
            else:
                self.image_drawer.draw_image(
                    c=c,
                    cfg=ImageDrawCfg(
                        path_img=cfg.path_photo,
                        x=x,
                        y=y,
                        width=cfg.sizes_cv.photo_size_pt,
                        height=cfg.sizes_cv.photo_size_pt,
                    ),
                )

    def draw_sidebar(
        self,
        *,
        c: Canvas,
        cfg: SidebarDrawCfg,
    ) -> None:
        c.setFillColor(cfg.style_cv.sidebar_panel)
        c.rect(cfg.sizes_cv.margin_left_pt, 0, cfg.sizes_cv.column_left_width_pt, cfg.page_height, fill=True, stroke=0)

        photo_bottom = cfg.page_height - cfg.sizes_cv.photo_size_pt - cfg.draw_config.photo_top_padding_mm * mm
        sidebar_text_bottom = cfg.sizes_cv.margin_pt + 5 * mm
        sidebar_height = photo_bottom - sidebar_text_bottom

        content: List[Paragraph | Spacer] = []
        content.append(Paragraph(cfg.linkedin_data.profile.full_name, cfg.styles["SidebarName"]))
        content.append(Spacer(1, cfg.draw_config.dist_full_name_to_headline))
        content.append(Paragraph(cfg.linkedin_data.profile.headline, cfg.styles["SidebarHeadline"]))
        content.append(Spacer(1, cfg.draw_config.dist_headline_to_links))

        info_lines = []
        if cfg.personal_information.age:
            info_lines.append(format_sidebar_info_line(LABEL_AGE, str(cfg.personal_information.age)))
        if cfg.personal_information.location:
            info_lines.append(format_sidebar_info_line(LABEL_LOCATION, cfg.personal_information.location))

        info_lines.append(format_sidebar_info_line(LABEL_MAIL, str(cfg.personal_information.email)))

        if cfg.personal_information.url_web_es and cfg.personal_information.url_web_en:
            info_lines.append(format_website_line(url_es=cfg.personal_information.url_web_es, url_en=cfg.personal_information.url_web_en))
        else:
            raise ValueError(
                f"Falta una url - {cfg.personal_information.url_web_es} - {cfg.personal_information.url_web_en}"
            )

        if cfg.personal_information.url_github:
            info_lines.append(format_link_line(label=LABEL_GITHUB, url=cfg.personal_information.url_github))
        if cfg.personal_information.url_linkedin:
            info_lines.append(format_link_line(label=LABEL_LINKEDIN, url=cfg.personal_information.url_linkedin))

        for line in info_lines:
            content.append(Paragraph(line, cfg.styles["SidebarLinks"]))
            content.append(Spacer(1, cfg.draw_config.dist_between_links))

        if SUMMARY_TECH_STACK_LABEL not in cfg.linkedin_data.profile.summary:
            raise ValueError(f"El texto '{SUMMARY_TECH_STACK_LABEL}' no está en summary.")

        summary_parts = cfg.linkedin_data.profile.summary.split(SUMMARY_TECH_STACK_LABEL)
        summary_parts = [p.strip() for p in summary_parts]

        class SectionSidebar(BaseModel):
            title: str
            text: str

        class SectionsSidebar(BaseModel):
            sections: List[SectionSidebar] = Field(default_factory=list)

        sections = SectionsSidebar()
        sections.sections.append(SectionSidebar(title=SECTION_ABOUT_ME_TITLE, text=SECTION_ABOUT_ME_TEXT))
        sections.sections.append(SectionSidebar(title=SECTION_GOAL_TITLE, text=SECTION_GOAL_TEXT))
        sections.sections.append(
            SectionSidebar(
                title=SECTION_TECH_SUMMARY_TITLE,
                text=self.shared_utils.sanitize_tech_summary(summary_parts[0]),
            )
        )
        sections.sections.append(SectionSidebar(title=SECTION_PROJECTS_TITLE, text=SECTION_PROJECTS_TEXT))
        sections.sections.append(SectionSidebar(title=SECTION_STACK_TITLE, text=summary_parts[1]))

        for section in sections.sections:
            content.append(Spacer(1, cfg.draw_config.dist_between_title_text_sidebar))
            content.extend(
                self.shared_utils.draw_title_text_sidebar(
                    title=section.title,
                    text=section.text,
                    styles=cfg.styles,
                    dist_between_title_sidebar_to_text=cfg.draw_config.dist_between_title_sidebar_to_text,
                )
            )

        frame = Frame(
            cfg.sizes_cv.margin_left_pt + cfg.draw_config.frame_margin_left_mm * mm,
            sidebar_text_bottom,
            cfg.sizes_cv.column_left_width_pt
            - (cfg.draw_config.frame_margin_left_mm + cfg.draw_config.frame_margin_right_mm) * mm,
            sidebar_height,
            showBoundary=0,
        )
        frame.addFromList(content, c)
