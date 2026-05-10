"""Render de sidebar y foto del CV."""
from typing import List

from reportlab.lib.units import mm
from reportlab.lib.styles import StyleSheet1
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame, Paragraph, Spacer

from src.app.drivers.draw_cv._image import ImageDrawer
from src.core.entities import DrawCVConfig, ImageDrawCfg, PhotoDrawCfg, SidebarDrawCfg, SidebarSection, SidebarSections
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


class _SidebarBackgroundDrawer:
    def draw(self, *, c: Canvas, cfg: SidebarDrawCfg) -> None:
        c.setFillColor(cfg.style_cv.sidebar_panel)
        c.rect(cfg.sizes_cv.margin_left_pt, 0, cfg.sizes_cv.column_left_width_pt, cfg.page_height, fill=True, stroke=0)


class _SidebarHeaderContentDrawer:
    def build(self, *, cfg: SidebarDrawCfg, draw_config: DrawCVConfig) -> List[Paragraph | Spacer]:
        content: List[Paragraph | Spacer] = []
        content.append(Paragraph(cfg.linkedin_data.profile.full_name, cfg.styles["SidebarName"]))
        content.append(Spacer(1, draw_config.dist_full_name_to_headline))
        content.append(Paragraph(cfg.linkedin_data.profile.headline, cfg.styles["SidebarHeadline"]))
        content.append(Spacer(1, draw_config.dist_headline_to_links))
        return content


class _SidebarPersonalInfoContentDrawer:
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


class _SidebarSectionTextDrawer:
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


class _SidebarSectionsContentDrawer:
    def __init__(self, section_text_drawer: _SidebarSectionTextDrawer) -> None:
        self.section_text_drawer = section_text_drawer

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

    def build(self, *, cfg: SidebarDrawCfg, draw_config: DrawCVConfig) -> List[Paragraph | Spacer]:
        content: List[Paragraph | Spacer] = []
        for section in self._build_sections(cfg=cfg).items:
            content.append(Spacer(1, draw_config.dist_between_title_text_sidebar))
            content.extend(
                self.section_text_drawer.build(
                    title=section.title,
                    text=section.text,
                    styles=cfg.styles,
                    dist_between_title_sidebar_to_text=draw_config.dist_between_title_sidebar_to_text,
                )
            )
        return content


class _SidebarFrameBuilder:
    def _get_vertical_bounds(self, *, cfg: SidebarDrawCfg, draw_config: DrawCVConfig) -> tuple[float, float]:
        photo_bottom = cfg.page_height - cfg.sizes_cv.photo_size_pt - draw_config.photo_top_padding_mm * mm
        sidebar_text_bottom = cfg.sizes_cv.margin_pt + 5 * mm
        sidebar_height = photo_bottom - sidebar_text_bottom
        return sidebar_text_bottom, sidebar_height

    def build(self, *, cfg: SidebarDrawCfg, draw_config: DrawCVConfig) -> Frame:
        sidebar_text_bottom, sidebar_height = self._get_vertical_bounds(cfg=cfg, draw_config=draw_config)
        return Frame(
            cfg.sizes_cv.margin_left_pt + draw_config.frame_margin_left_mm * mm,
            sidebar_text_bottom,
            cfg.sizes_cv.column_left_width_pt - (draw_config.frame_margin_left_mm + draw_config.frame_margin_right_mm) * mm,
            sidebar_height,
            showBoundary=0,
        )


class SidebarDrawer:

    def __init__(
        self,
        image_drawer: ImageDrawer,
        background_drawer: _SidebarBackgroundDrawer | None = None,
        header_content_drawer: _SidebarHeaderContentDrawer | None = None,
        personal_info_drawer: _SidebarPersonalInfoContentDrawer | None = None,
        sections_content_drawer: _SidebarSectionsContentDrawer | None = None,
        frame_builder: _SidebarFrameBuilder | None = None,
    ) -> None:
        self.image_drawer = image_drawer
        self.background_drawer = background_drawer or _SidebarBackgroundDrawer()
        self.header_content_drawer = header_content_drawer or _SidebarHeaderContentDrawer()
        self.personal_info_drawer = personal_info_drawer or _SidebarPersonalInfoContentDrawer()
        self.sections_content_drawer = sections_content_drawer or _SidebarSectionsContentDrawer(
            section_text_drawer=_SidebarSectionTextDrawer()
        )
        self.frame_builder = frame_builder or _SidebarFrameBuilder()

    def _build_photo_image_cfg(self, *, cfg: PhotoDrawCfg, x: float, y: float) -> ImageDrawCfg:
        return ImageDrawCfg(
            path_img=cfg.path_photo,
            x=x,
            y=y,
            width=cfg.sizes_cv.photo_size_pt,
            height=cfg.sizes_cv.photo_size_pt,
            is_circle=cfg.is_photo_circle,
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
        self.background_drawer.draw(c=c, cfg=cfg)
        content = self.header_content_drawer.build(cfg=cfg, draw_config=draw_config)
        content.extend(self.personal_info_drawer.build(cfg=cfg, draw_config=draw_config))
        content.extend(self.sections_content_drawer.build(cfg=cfg, draw_config=draw_config))
        frame = self.frame_builder.build(cfg=cfg, draw_config=draw_config)
        frame.addFromList(content, c)
