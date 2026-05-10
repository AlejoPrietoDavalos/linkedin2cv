from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.draw_cv.reportlab_tools import ImageDrawer
from src.core.constants import PATH_PHOTO
from src.core.entities.config import LayoutConfig, SpacingConfig
from src.core.entities.draw_inputs import ImageDrawCfg


class SidebarPhotoDrawer:
    def __init__(self, image_drawer: ImageDrawer | None = None) -> None:
        self.image_drawer = image_drawer or ImageDrawer()

    def draw(self, *, c: Canvas, layout_cfg: LayoutConfig, spacing: SpacingConfig) -> None:
        if PATH_PHOTO.exists():
            cfg_image = ImageDrawCfg(
                path_img=PATH_PHOTO,
                x=layout_cfg.photo_x,
                y=layout_cfg.photo_y,
                width=layout_cfg.photo_size_pt,
                height=layout_cfg.photo_size_pt,
                is_circle=spacing.is_photo_circle,
            )
            self.image_drawer.draw_image(c=c, cfg=cfg_image)
