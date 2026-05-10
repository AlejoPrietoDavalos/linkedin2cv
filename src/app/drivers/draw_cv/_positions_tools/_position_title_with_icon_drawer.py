from reportlab.lib.styles import StyleSheet1
from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.draw_cv.reportlab_tools import ImageTitleDrawer
from src.core.constants import PATH_PYTHON_ICON
from src.core.entities import ImageTitleDrawCfg, PositionsLayoutDTO
from src.core.entities.config import SpacingConfig
from src.core.hardcoded_config import format_job_title_html


class PositionTitleWithIconDrawer:
    def __init__(self, image_title_drawer: ImageTitleDrawer | None = None) -> None:
        self.image_title_drawer = image_title_drawer or ImageTitleDrawer()

    def draw(
        self,
        *,
        c: Canvas,
        styles: StyleSheet1,
        spacing_config: SpacingConfig,
        layout: PositionsLayoutDTO,
        position_title: str,
        y_cursor: float,
    ) -> float:
        title_cfg = ImageTitleDrawCfg(
            path_img=PATH_PYTHON_ICON,
            title_html=format_job_title_html(title=position_title),
            img_size=layout.icon_size_pt,
            image_to_title_dist=spacing_config.dist_python_icon_to_title,
        )
        y_icon = self.image_title_drawer.draw_title_row_at_cursor(
            c=c,
            cfg=title_cfg,
            style=styles["JobTitle"],
            x=layout.body_x,
            y_cursor=y_cursor,
            available_width=layout.body_width,
            available_height=layout.usable_height,
        )
        return y_icon
