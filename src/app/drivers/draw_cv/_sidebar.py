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
from src.core.entities.config import LayoutConfig, SpacingConfig
from src.core.entities.linkedin_data import LinkedInData
from src.core.entities.personal_information import PersonalInformation
from src.core.entities.styles_config import StylesConfig


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
        linkedin_data: LinkedInData,
        personal_information: PersonalInformation,
        layout_cfg: LayoutConfig,
        styles_config: StylesConfig,
        styles: StyleSheet1,
        spacing: SpacingConfig,
    ) -> None:
        self.background_drawer.draw(c=c, layout_cfg=layout_cfg, styles_config=styles_config)
        self.photo_drawer.draw(c=c, layout_cfg=layout_cfg, spacing=spacing)
        content: List[Paragraph | Spacer] = []
        content.extend(self.header_content_drawer.build(linkedin_data=linkedin_data, styles=styles, spacing=spacing))
        content.extend(self.personal_info_drawer.build(personal_information=personal_information, styles=styles, spacing=spacing))
        content.extend(self.sections_content_drawer.build(linkedin_data=linkedin_data, styles=styles, spacing=spacing))
        frame = self.frame_builder.build(layout_cfg=layout_cfg, spacing=spacing)
        frame.addFromList(content, c)
