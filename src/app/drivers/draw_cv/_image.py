"""Abstracción para dibujo de imágenes en canvas."""

from reportlab.pdfgen.canvas import Canvas

from src.core.entities import ImageDrawCfg


class ImageDrawer:
    def draw_image(self, *, c: Canvas, cfg: ImageDrawCfg) -> None:
        if cfg.is_circle:
            c.saveState()
            path = c.beginPath()
            path.circle(cfg.center_x, cfg.center_y, cfg.radius)
            c.clipPath(path, stroke=0)

        c.drawImage(
            str(cfg.path_img),
            cfg.x,
            cfg.y,
            width=cfg.width,
            height=cfg.height,
            preserveAspectRatio=True,
            mask="auto",
        )
        if cfg.is_circle:
            c.restoreState()
