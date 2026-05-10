"""Render de posiciones/experiencia del CV."""

from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from src.app.drivers.draw_cv._image_title import ImageTitleDrawer
from src.core.constants import PATH_PYTHON_ICON
from src.core.entities import (
    DividerLine,
    DrawCVConfig,
    DrawPositionsResult,
    ImageTitleDrawCfg,
    PositionsDrawCfg,
    PositionsLayoutDTO,
)
from src.core.hardcoded_config import (
    JOB_DESCRIPTION_FALLBACK,
    format_final_credit_html,
    format_job_subtitle_html,
    format_job_title_html,
)


class _PositionTitleWithIconDrawer:
    def __init__(self, image_title_drawer: ImageTitleDrawer | None = None) -> None:
        self.image_title_drawer = image_title_drawer or ImageTitleDrawer()

    def draw(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        draw_config: DrawCVConfig,
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
            image_to_title_dist=draw_config.dist_python_icon_to_title,
        )
        return self.image_title_drawer.draw_title_row_at_cursor(
            c=c,
            cfg=title_cfg,
            style=cfg.styles["JobTitle"],
            x=x,
            y_cursor=y_cursor,
            available_width=width,
            available_height=usable_height,
        )


class _PositionSubtitleDrawer:
    def draw(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        draw_config: DrawCVConfig,
        subtitle_text: str,
        x: float,
        y_cursor: float,
        width: float,
        usable_height: float,
    ) -> float:
        subtitle = Paragraph(format_job_subtitle_html(subtitle=subtitle_text), cfg.styles["JobSubTitle"])
        _, subtitle_height = subtitle.wrap(width, usable_height)
        subtitle.drawOn(c, x, y_cursor - subtitle_height)
        return y_cursor - subtitle_height - draw_config.line_thickness


class _PositionDescriptionDrawer:
    def draw(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        draw_config: DrawCVConfig,
        description_text: str,
        x: float,
        y_cursor: float,
        width: float,
        usable_height: float,
    ) -> float:
        desc = Paragraph(description_text or JOB_DESCRIPTION_FALLBACK, cfg.styles["JobDesc"])
        _, desc_height = desc.wrap(width, usable_height)
        desc.drawOn(c, x, y_cursor - desc_height)
        return y_cursor - desc_height - draw_config.spacer_height


class _FinalCreditMessageDrawer:
    def draw(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        x: float,
        y_cursor: float,
        width: float,
        usable_height: float,
    ) -> None:
        final_text = Paragraph(format_final_credit_html(), cfg.styles["JobDesc"])
        _, h_final = final_text.wrap(width, usable_height)
        final_text.drawOn(c, x, y_cursor - h_final)


class PositionsDrawer:
    def __init__(
        self,
        position_title_with_icon_drawer: _PositionTitleWithIconDrawer | None = None,
        position_subtitle_drawer: _PositionSubtitleDrawer | None = None,
        position_description_drawer: _PositionDescriptionDrawer | None = None,
        final_credit_message_drawer: _FinalCreditMessageDrawer | None = None,
    ) -> None:
        self.position_title_with_icon_drawer = position_title_with_icon_drawer or _PositionTitleWithIconDrawer()
        self.position_subtitle_drawer = position_subtitle_drawer or _PositionSubtitleDrawer()
        self.position_description_drawer = position_description_drawer or _PositionDescriptionDrawer()
        self.final_credit_message_drawer = final_credit_message_drawer or _FinalCreditMessageDrawer()

    def _draw_position_title_with_icon(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        draw_config: DrawCVConfig,
        position_title: str,
        x: float,
        y_cursor: float,
        width: float,
        usable_height: float,
        icon_size: float,
    ) -> float:
        return self.position_title_with_icon_drawer.draw(
            c=c,
            cfg=cfg,
            draw_config=draw_config,
            position_title=position_title,
            x=x,
            y_cursor=y_cursor,
            width=width,
            usable_height=usable_height,
            icon_size=icon_size,
        )

    def _draw_position_subtitle(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        draw_config: DrawCVConfig,
        subtitle_text: str,
        x: float,
        y_icon: float,
        width: float,
        usable_height: float,
    ) -> float:
        return self.position_subtitle_drawer.draw(
            c=c,
            cfg=cfg,
            draw_config=draw_config,
            subtitle_text=subtitle_text,
            x=x,
            y_cursor=y_icon - draw_config.line_thickness,
            width=width,
            usable_height=usable_height,
        )

    def _draw_position_description(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        draw_config: DrawCVConfig,
        description_text: str,
        x: float,
        y_cursor: float,
        width: float,
        usable_height: float,
    ) -> float:
        return self.position_description_drawer.draw(
            c=c,
            cfg=cfg,
            draw_config=draw_config,
            description_text=description_text,
            x=x,
            y_cursor=y_cursor,
            width=width,
            usable_height=usable_height,
        )

    def _build_divider_line(self, *, cfg: PositionsDrawCfg, draw_config: DrawCVConfig, x: float, y_line: float) -> DividerLine:
        return DividerLine(
            x_start=x + draw_config.dist_line_spacing_left_mm * mm,
            y_start=y_line,
            x_end=cfg.page_width - cfg.sizes_cv.margin_pt - draw_config.dist_line_spacing_right_mm * mm,
            y_end=y_line,
        )

    def _draw_final_credit_message(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        x: float,
        y_cursor: float,
        width: float,
        usable_height: float,
    ) -> None:
        self.final_credit_message_drawer.draw(
            c=c,
            cfg=cfg,
            x=x,
            y_cursor=y_cursor,
            width=width,
            usable_height=usable_height,
        )

    def draw_positions(
        self,
        *,
        c: Canvas,
        cfg: PositionsDrawCfg,
        draw_config: DrawCVConfig,
    ) -> DrawPositionsResult:
        layout = PositionsLayoutDTO.from_positions_and_draw_config(
            positions_cfg=cfg,
            draw_config=draw_config,
        )
        y_cursor = layout.body_start_y
        lines: list[DividerLine] = []

        for idx, position in enumerate(cfg.linkedin_data.positions):
            y_icon = self._draw_position_title_with_icon(
                c=c,
                cfg=cfg,
                draw_config=draw_config,
                position_title=position.text_title,
                x=layout.body_x,
                y_cursor=y_cursor,
                width=layout.body_width,
                usable_height=layout.usable_height,
                icon_size=layout.icon_size_pt,
            )
            y_cursor = self._draw_position_subtitle(
                c=c,
                cfg=cfg,
                draw_config=draw_config,
                subtitle_text=position.text_sub_title,
                x=layout.body_x,
                y_icon=y_icon,
                width=layout.body_width,
                usable_height=layout.usable_height,
            )
            y_cursor = self._draw_position_description(
                c=c,
                cfg=cfg,
                draw_config=draw_config,
                description_text=position.description,
                x=layout.body_x,
                y_cursor=y_cursor,
                width=layout.body_width,
                usable_height=layout.usable_height,
            )

            if idx < len(cfg.linkedin_data.positions) - 1:
                # FIXME: Estas líneas son el input que luego consume BuildCVService.draw_lines()
                # para dibujar divisores con fitz sobre el PDF final.
                lines.append(self._build_divider_line(cfg=cfg, draw_config=draw_config, x=layout.body_x, y_line=y_icon))

        self._draw_final_credit_message(
            c=c,
            cfg=cfg,
            x=layout.body_x,
            y_cursor=y_cursor,
            width=layout.body_width,
            usable_height=layout.usable_height,
        )

        return DrawPositionsResult(divider_lines=lines, line_anchor_x=layout.line_anchor_x)
