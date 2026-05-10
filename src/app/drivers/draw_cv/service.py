"""Servicio principal de dibujo de CV, compuesto por sub-servicios."""

from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.draw_cv._background import BackgroundDrawer
from src.app.drivers.draw_cv._image import ImageDrawer
from src.app.drivers.draw_cv._image_title import ImageTitleDrawer
from src.app.drivers.draw_cv._positions import PositionsDrawer
from src.app.drivers.draw_cv._sidebar import SidebarDrawer
from src.core.drivers.draw import CoreDrawCVService
from src.core.entities import (
    BackgroundDrawCfg,
    DrawCVConfig,
    DrawPositionsResult,
    PhotoDrawCfg,
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
        image_drawer = ImageDrawer()
        image_title_drawer = ImageTitleDrawer(image_drawer=image_drawer)
        self.background_drawer = background_drawer or BackgroundDrawer()
        self.sidebar_drawer = sidebar_drawer or SidebarDrawer(image_drawer=image_drawer)
        self.positions_drawer = positions_drawer or PositionsDrawer(image_title_drawer=image_title_drawer)

    def draw_background(self, *, c: Canvas, cfg: BackgroundDrawCfg) -> None:
        self.background_drawer.draw_background(c=c, cfg=cfg)

    def draw_photo(self, *, c: Canvas, cfg: PhotoDrawCfg, draw_config: DrawCVConfig) -> None:
        self.sidebar_drawer.draw_photo(c=c, cfg=cfg, draw_config=draw_config)

    def draw_sidebar(self, *, c: Canvas, cfg: SidebarDrawCfg, draw_config: DrawCVConfig) -> None:
        self.sidebar_drawer.draw_sidebar(c=c, cfg=cfg, draw_config=draw_config)

    def draw_positions(self, *, c: Canvas, cfg: PositionsDrawCfg, draw_config: DrawCVConfig) -> DrawPositionsResult:
        return self.positions_drawer.draw_positions(c=c, cfg=cfg, draw_config=draw_config)
