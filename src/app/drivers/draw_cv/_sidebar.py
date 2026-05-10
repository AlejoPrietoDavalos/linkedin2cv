"""Render de sidebar y foto del CV."""

from typing import List
from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import Paragraph, Spacer

from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.draw_cv._sidebar_tools import (
    SidebarBackgroundDrawer,
    SidebarFrameBuilder,
    SidebarHeaderContentDrawer,
    SidebarPersonalInfoContentDrawer,
    SidebarPhotoDrawer,
    SidebarSectionsContentDrawer,
)
from src.core.entities import DrawCVConfig, SidebarDrawCfg


class SidebarDrawer:
    def __init__(
        self,
        background_drawer: SidebarBackgroundDrawer | None = None,
        photo_drawer: SidebarPhotoDrawer | None = None,
        header_content_drawer: SidebarHeaderContentDrawer | None = None,
        personal_info_drawer: SidebarPersonalInfoContentDrawer | None = None,
        sections_content_drawer: SidebarSectionsContentDrawer | None = None,
        frame_builder: SidebarFrameBuilder | None = None,
    ) -> None:
        self.background_drawer = background_drawer or SidebarBackgroundDrawer()
        self.photo_drawer = photo_drawer or SidebarPhotoDrawer()
        self.header_content_drawer = header_content_drawer or SidebarHeaderContentDrawer()
        self.personal_info_drawer = personal_info_drawer or SidebarPersonalInfoContentDrawer()
        self.sections_content_drawer = sections_content_drawer or SidebarSectionsContentDrawer()
        self.frame_builder = frame_builder or SidebarFrameBuilder()

    def draw_sidebar(
        self,
        *,
        c: Canvas,
        cfg: SidebarDrawCfg,
        styles: StyleSheet1,
        draw_config: DrawCVConfig,
    ) -> None:
        self.background_drawer.draw(c=c, cfg=cfg)
        self.photo_drawer.draw(c=c, cfg=cfg)
        content: List[Paragraph | Spacer] = []
        content.extend(self.header_content_drawer.build(cfg=cfg, styles=styles, draw_config=draw_config))
        content.extend(self.personal_info_drawer.build(cfg=cfg, styles=styles, draw_config=draw_config))
        content.extend(self.sections_content_drawer.build(cfg=cfg, styles=styles, draw_config=draw_config))
        frame = self.frame_builder.build(cfg=cfg, draw_config=draw_config)
        frame.addFromList(content, c)
