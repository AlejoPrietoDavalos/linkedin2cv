"""Render de posiciones/experiencia del CV."""

from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from src.app.drivers.draw_cv._image_title import ImageTitleDrawer
from src.core.constants import PATH_PYTHON_ICON
from src.core.entities import DividerLine, DrawPositionsResult, ImageTitleDrawCfg, PositionsDrawCfg
from src.core.hardcoded_config import (
    JOB_DESCRIPTION_FALLBACK,
    format_final_credit_html,
    format_job_subtitle_html,
    format_job_title_html,
)


class PositionsDrawer:
    def __init__(self, image_title_drawer: ImageTitleDrawer) -> None:
        self.image_title_drawer = image_title_drawer

    def _draw_position_title(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        position_title: str,
        x: float,
        y_cursor: float,
        width: float,
        usable_height: float,
        icon_size: float,
    ) -> float:
        title_cfg = ImageTitleDrawCfg(
            path_img=PATH_PYTHON_ICON,
            title_html=format_job_title_html(title=position_title),
            img_size=icon_size,
            image_to_title_dist=cfg.draw_config.dist_python_icon_to_title,
        )
        title_paragraph, h_icon = self.image_title_drawer.measure_title_row(
            cfg=title_cfg,
            style=cfg.styles["JobTitle"],
            available_width=width,
            available_height=usable_height,
        )
        y_icon = y_cursor - h_icon
        c.saveState()
        c.translate(x, y_icon)
        self.image_title_drawer.draw_title_row(c=c, cfg=title_cfg, paragraph=title_paragraph, row_height=h_icon)
        c.restoreState()
        return y_icon

    def _draw_subtitle_and_description(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        subtitle_text: str,
        description_text: str,
        x: float,
        y_icon: float,
        width: float,
        usable_height: float,
    ) -> float:
        subtitle = Paragraph(format_job_subtitle_html(subtitle=subtitle_text), cfg.styles["JobSubTitle"])
        _, h_sub = subtitle.wrap(width, usable_height)
        desc = Paragraph(description_text or JOB_DESCRIPTION_FALLBACK, cfg.styles["JobDesc"])
        _, h_desc = desc.wrap(width, usable_height)

        y_cursor = y_icon - cfg.draw_config.line_thickness
        subtitle.drawOn(c, x, y_cursor - h_sub)
        y_cursor -= h_sub + cfg.draw_config.line_thickness
        desc.drawOn(c, x, y_cursor - h_desc)
        y_cursor -= h_desc + cfg.draw_config.spacer_height
        return y_cursor

    def _build_divider_line(self, *, cfg: PositionsDrawCfg, x: float, y_line: float) -> DividerLine:
        return DividerLine(
            x_start=x + cfg.draw_config.dist_line_spacing_left_mm * mm,
            y_start=y_line,
            x_end=cfg.page_width - cfg.sizes_cv.margin_pt - cfg.draw_config.dist_line_spacing_right_mm * mm,
            y_end=y_line,
        )

    def _draw_final_credit(self, *, c: Canvas, cfg: PositionsDrawCfg, x: float, y_cursor: float, width: float, usable_height: float) -> None:
        final_text = Paragraph(format_final_credit_html(), cfg.styles["JobDesc"])
        _, h_final = final_text.wrap(width, usable_height)
        final_text.drawOn(c, x, y_cursor - h_final)

    def draw_positions(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
    ) -> DrawPositionsResult:
        y_cursor = cfg.body_start_y
        lines: list[DividerLine] = []

        for idx, position in enumerate(cfg.linkedin_data.positions):
            y_icon = self._draw_position_title(
                c=c,
                cfg=cfg,
                position_title=position.text_title,
                x=cfg.body_x,
                y_cursor=y_cursor,
                width=cfg.body_width,
                usable_height=cfg.usable_height,
                icon_size=cfg.icon_size_pt,
            )
            y_cursor = self._draw_subtitle_and_description(
                c=c,
                cfg=cfg,
                subtitle_text=position.text_sub_title,
                description_text=position.description,
                x=cfg.body_x,
                y_icon=y_icon,
                width=cfg.body_width,
                usable_height=cfg.usable_height,
            )

            if idx < len(cfg.linkedin_data.positions) - 1:
                # FIXME: Estas líneas son el input que luego consume BuildCVService.draw_lines()
                # para dibujar divisores con fitz sobre el PDF final.
                lines.append(self._build_divider_line(cfg=cfg, x=cfg.body_x, y_line=y_icon))

        self._draw_final_credit(
            c=c,
            cfg=cfg,
            x=cfg.body_x,
            y_cursor=y_cursor,
            width=cfg.body_width,
            usable_height=cfg.usable_height,
        )

        return DrawPositionsResult(divider_lines=lines, line_anchor_x=cfg.line_anchor_x)
