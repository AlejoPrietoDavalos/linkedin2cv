from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.draw_cv.reportlab_tools import ImageDrawer
from src.core.entities import ImageDrawCfg, SidebarDrawCfg


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

    def draw(self, *, c: Canvas, cfg: SidebarDrawCfg) -> None:
        if cfg.path_photo.exists():
            cfg_image = self._build_photo_image_cfg(
                cfg=cfg,
                x=cfg.sizes_cv.photo_x,
                y=cfg.sizes_cv.photo_y
            )
            self.image_drawer.draw_image(c=c, cfg=cfg_image)
