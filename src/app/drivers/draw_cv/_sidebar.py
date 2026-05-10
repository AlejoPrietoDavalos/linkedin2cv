"""Render de sidebar y foto del CV."""

from typing import List

from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame, Paragraph, Spacer

from src.app.drivers.draw_cv._image import ImageDrawer
from src.app.drivers.draw_cv._shared import SharedDrawUtils
from src.core.entities import DrawCVConfig, ImageDrawCfg, PhotoDrawCfg, SidebarDrawCfg
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

    def _build_photo_image_cfg(self, *, cfg: PhotoDrawCfg, x: float, y: float) -> ImageDrawCfg:
        return ImageDrawCfg(
            path_img=cfg.path_photo,
            x=x,
            y=y,
            width=cfg.sizes_cv.photo_size_pt,
            height=cfg.sizes_cv.photo_size_pt,
            is_circle=cfg.is_photo_circle,
        )

    def _draw_sidebar_background(self, *, c: Canvas, cfg: SidebarDrawCfg) -> None:
        c.setFillColor(cfg.style_cv.sidebar_panel)
        c.rect(cfg.sizes_cv.margin_left_pt, 0, cfg.sizes_cv.column_left_width_pt, cfg.page_height, fill=True, stroke=0)

    def _build_sidebar_header_content(self, *, cfg: SidebarDrawCfg, draw_config: DrawCVConfig) -> List[Paragraph | Spacer]:
        content: List[Paragraph | Spacer] = []
        content.append(Paragraph(cfg.linkedin_data.profile.full_name, cfg.styles["SidebarName"]))
        content.append(Spacer(1, draw_config.dist_full_name_to_headline))
        content.append(Paragraph(cfg.linkedin_data.profile.headline, cfg.styles["SidebarHeadline"]))
        content.append(Spacer(1, draw_config.dist_headline_to_links))
        return content

    @staticmethod
    def _build_sidebar_info_lines(*, cfg: SidebarDrawCfg) -> list[str]:
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
            raise ValueError(
                f"Falta una url - {cfg.personal_information.url_web_es} - {cfg.personal_information.url_web_en}"
            )

        if cfg.personal_information.url_github:
            info_lines.append(format_link_line(label=LABEL_GITHUB, url=cfg.personal_information.url_github))
        if cfg.personal_information.url_linkedin:
            info_lines.append(format_link_line(label=LABEL_LINKEDIN, url=cfg.personal_information.url_linkedin))
        return info_lines

    def _append_sidebar_info_content(
        self,
        *,
        content: List[Paragraph | Spacer],
        cfg: SidebarDrawCfg,
        draw_config: DrawCVConfig,
    ) -> None:
        for line in self._build_sidebar_info_lines(cfg=cfg):
            content.append(Paragraph(line, cfg.styles["SidebarLinks"]))
            content.append(Spacer(1, draw_config.dist_between_links))

    def _build_sidebar_sections(self, *, cfg: SidebarDrawCfg) -> list[tuple[str, str]]:
        if SUMMARY_TECH_STACK_LABEL not in cfg.linkedin_data.profile.summary:
            raise ValueError(f"El texto '{SUMMARY_TECH_STACK_LABEL}' no está en summary.")

        summary_parts = cfg.linkedin_data.profile.summary.split(SUMMARY_TECH_STACK_LABEL)
        summary_parts = [p.strip() for p in summary_parts]
        return [
            (SECTION_ABOUT_ME_TITLE, SECTION_ABOUT_ME_TEXT),
            (SECTION_GOAL_TITLE, SECTION_GOAL_TEXT),
            (SECTION_TECH_SUMMARY_TITLE, self.shared_utils.sanitize_tech_summary(summary_parts[0])),
            (SECTION_PROJECTS_TITLE, SECTION_PROJECTS_TEXT),
            (SECTION_STACK_TITLE, summary_parts[1]),
        ]

    def _append_sidebar_sections_content(
        self,
        *,
        content: List[Paragraph | Spacer],
        cfg: SidebarDrawCfg,
        draw_config: DrawCVConfig,
    ) -> None:
        for title, text in self._build_sidebar_sections(cfg=cfg):
            content.append(Spacer(1, draw_config.dist_between_title_text_sidebar))
            content.extend(
                self.shared_utils.draw_title_text_sidebar(
                    title=title,
                    text=text,
                    styles=cfg.styles,
                    dist_between_title_sidebar_to_text=draw_config.dist_between_title_sidebar_to_text,
                )
            )

    @staticmethod
    def _build_sidebar_frame(
        *,
        cfg: SidebarDrawCfg,
        draw_config: DrawCVConfig,
        sidebar_text_bottom: float,
        sidebar_height: float,
    ) -> Frame:
        return Frame(
            cfg.sizes_cv.margin_left_pt + draw_config.frame_margin_left_mm * mm,
            sidebar_text_bottom,
            cfg.sizes_cv.column_left_width_pt
            - (draw_config.frame_margin_left_mm + draw_config.frame_margin_right_mm) * mm,
            sidebar_height,
            showBoundary=0,
        )

    def draw_photo(
        self,
        *,
        c: Canvas,
        cfg: PhotoDrawCfg,
        draw_config: DrawCVConfig,
    ) -> None:
        if cfg.path_photo and cfg.path_photo.exists():
            x = cfg.sizes_cv.margin_left_pt + (cfg.sizes_cv.column_left_width_pt - cfg.sizes_cv.photo_size_pt) / 2
            y = cfg.page_height - cfg.sizes_cv.photo_size_pt - draw_config.photo_top_padding_mm * mm
            self.image_drawer.draw_image(c=c, cfg=self._build_photo_image_cfg(cfg=cfg, x=x, y=y))

    def draw_sidebar(
        self,
        *,
        c: Canvas,
        cfg: SidebarDrawCfg,
        draw_config: DrawCVConfig,
    ) -> None:
        self._draw_sidebar_background(c=c, cfg=cfg)

        photo_bottom = cfg.page_height - cfg.sizes_cv.photo_size_pt - draw_config.photo_top_padding_mm * mm
        sidebar_text_bottom = cfg.sizes_cv.margin_pt + 5 * mm
        sidebar_height = photo_bottom - sidebar_text_bottom

        content = self._build_sidebar_header_content(cfg=cfg, draw_config=draw_config)
        self._append_sidebar_info_content(content=content, cfg=cfg, draw_config=draw_config)
        self._append_sidebar_sections_content(content=content, cfg=cfg, draw_config=draw_config)

        frame = self._build_sidebar_frame(
            cfg=cfg,
            draw_config=draw_config,
            sidebar_text_bottom=sidebar_text_bottom,
            sidebar_height=sidebar_height,
        )
        frame.addFromList(content, c)
