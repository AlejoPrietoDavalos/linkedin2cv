from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.draw_cv.reportlab_tools import ImageDrawer
from src.core.entities import DrawCVConfig, ImageDrawCfg, SidebarDrawCfg


class SidebarPhotoDrawer:
    def __init__(self, image_drawer: ImageDrawer | None = None) -> None:
        self.image_drawer = image_drawer or ImageDrawer()

    def _build_photo_image_cfg(self, *, cfg: SidebarDrawCfg, x: float, y: float) -> ImageDrawCfg:
        return ImageDrawCfg(
            path_img=cfg.path_photo,
            x=x,
            y=y,
            width=cfg.sizes_cv.photo_size_pt,
            height=cfg.sizes_cv.photo_size_pt,
            is_circle=cfg.is_photo_circle,
        )

    def draw(self, *, c: Canvas, cfg: SidebarDrawCfg, draw_config: DrawCVConfig) -> None:
        if cfg.path_photo.exists():
            x = cfg.sizes_cv.margin_left_pt + (cfg.sizes_cv.column_left_width_pt - cfg.sizes_cv.photo_size_pt) / 2
            y = cfg.page_height - cfg.sizes_cv.photo_size_pt - draw_config.photo_top_padding_mm * mm
            self.image_drawer.draw_image(c=c, cfg=self._build_photo_image_cfg(cfg=cfg, x=x, y=y))
