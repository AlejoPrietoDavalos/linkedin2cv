"""Servicio principal de dibujo de CV, compuesto por sub-servicios."""

from reportlab.lib.styles import StyleSheet1
from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.draw_cv._background import BackgroundDrawer
from src.app.drivers.draw_cv._positions import PositionsDrawer
from src.app.drivers.draw_cv._sidebar import SidebarDrawer
from src.core.drivers.draw import CoreDrawCVService
from src.core.entities import (
    BackgroundDrawCfg,
    DrawCVConfig,
    DrawPositionsResult,
    PositionsDrawCfg,
    SidebarDrawCfg,
)


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

    def draw_background(self, *, c: Canvas, cfg: BackgroundDrawCfg) -> None:
        self.background_drawer.draw_background(c=c, cfg=cfg)

    def draw_sidebar(self, *, c: Canvas, cfg: SidebarDrawCfg, styles: StyleSheet1, draw_config: DrawCVConfig) -> None:
        self.sidebar_drawer.draw_sidebar(c=c, cfg=cfg, styles=styles, draw_config=draw_config)

    def draw_positions(self, *, c: Canvas, cfg: PositionsDrawCfg, styles: StyleSheet1, draw_config: DrawCVConfig) -> DrawPositionsResult:
        return self.positions_drawer.draw_positions(c=c, cfg=cfg, styles=styles, draw_config=draw_config)
