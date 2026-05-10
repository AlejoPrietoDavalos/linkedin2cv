"""Render de posiciones/experiencia del CV."""

from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.draw_cv._positions_tools import (
    DividerLineBuilder,
    FinalCreditMessageDrawer,
    PositionDescriptionDrawer,
    PositionSubtitleDrawer,
    PositionTitleWithIconDrawer,
)
from src.core.entities import DrawCVConfig, DrawPositionsResult, PositionsDrawCfg, PositionsLayoutDTO


class PositionsDrawer:
    def __init__(
        self,
        position_title_with_icon_drawer: PositionTitleWithIconDrawer | None = None,
        position_subtitle_drawer: PositionSubtitleDrawer | None = None,
        position_description_drawer: PositionDescriptionDrawer | None = None,
        final_credit_message_drawer: FinalCreditMessageDrawer | None = None,
        divider_line_builder: DividerLineBuilder | None = None,
    ) -> None:
        self.position_title_with_icon_drawer = position_title_with_icon_drawer or PositionTitleWithIconDrawer()
        self.position_subtitle_drawer = position_subtitle_drawer or PositionSubtitleDrawer()
        self.position_description_drawer = position_description_drawer or PositionDescriptionDrawer()
        self.final_credit_message_drawer = final_credit_message_drawer or FinalCreditMessageDrawer()
        self.divider_line_builder = divider_line_builder or DividerLineBuilder()

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
        divider_lines = []

        for idx, position in enumerate(cfg.linkedin_data.positions):
            y_icon = self.position_title_with_icon_drawer.draw(
                c=c,
                cfg=cfg,
                draw_config=draw_config,
                layout=layout,
                position_title=position.text_title,
                y_cursor=y_cursor,
            )
            y_cursor = self.position_subtitle_drawer.draw(
                c=c,
                cfg=cfg,
                draw_config=draw_config,
                layout=layout,
                subtitle_text=position.text_sub_title,
                y_cursor=y_icon - draw_config.line_thickness,
            )
            y_cursor = self.position_description_drawer.draw(
                c=c,
                cfg=cfg,
                draw_config=draw_config,
                layout=layout,
                description_text=position.description,
                y_cursor=y_cursor,
            )

            if idx < len(cfg.linkedin_data.positions) - 1:
                divider_line = self.divider_line_builder.build(
                    cfg=cfg,
                    draw_config=draw_config,
                    layout=layout,
                    y_line=y_icon,
                )
                divider_lines.append(divider_line)

        self.final_credit_message_drawer.draw(
            c=c,
            cfg=cfg,
            layout=layout,
            y_cursor=y_cursor,
        )

        return DrawPositionsResult(divider_lines=divider_lines, line_anchor_x=layout.line_anchor_x)
