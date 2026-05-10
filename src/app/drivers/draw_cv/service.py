"""Servicio principal de dibujo de CV, compuesto por sub-servicios."""

from reportlab.lib.styles import StyleSheet1
from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.draw_cv._background import BackgroundDrawer
from src.app.drivers.draw_cv._positions import PositionsDrawer
from src.app.drivers.draw_cv._sidebar import SidebarDrawer
from src.core.drivers.draw import CoreDrawCVService
from src.core.entities import DrawPositionsResult
from src.core.entities.config import LayoutConfig, SpacingConfig
from src.core.entities.linkedin_data import LinkedInData
from src.core.entities.personal_information import PersonalInformation
from src.core.entities.styles_config import StylesConfig


class DrawCVService(CoreDrawCVService):
    """Fachada de dibujo que delega responsabilidades por sección."""

    def __init__(
        self,
        background_drawer: BackgroundDrawer | None = None,
        sidebar_drawer: SidebarDrawer | None = None,
        positions_drawer: PositionsDrawer | None = None,
    ) -> None:
        self.background_drawer = background_drawer or BackgroundDrawer()
        self.sidebar_drawer = sidebar_drawer or SidebarDrawer()
        self.positions_drawer = positions_drawer or PositionsDrawer()

    def draw_background(self, *, c: Canvas, styles_config: StylesConfig, layout_cfg: LayoutConfig) -> None:
        self.background_drawer.draw_background(c=c, styles_config=styles_config, layout_cfg=layout_cfg)

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
        self.sidebar_drawer.draw_sidebar(
            c=c,
            linkedin_data=linkedin_data,
            personal_information=personal_information,
            layout_cfg=layout_cfg,
            styles_config=styles_config,
            styles=styles,
            spacing=spacing,
        )

    def draw_positions(
        self,
        *,
        c: Canvas,
        linkedin_data: LinkedInData,
        layout_cfg: LayoutConfig,
        styles: StyleSheet1,
        spacing: SpacingConfig,
    ) -> DrawPositionsResult:
        return self.positions_drawer.draw_positions(
            c=c,
            linkedin_data=linkedin_data,
            layout_cfg=layout_cfg,
            styles=styles,
            spacing=spacing,
        )
