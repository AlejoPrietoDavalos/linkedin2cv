"""Render de posiciones/experiencia del CV."""

from reportlab.lib.styles import StyleSheet1
from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.draw_cv._positions_tools import (
    DividerLineBuilder,
    FinalCreditMessageDrawer,
    PositionDescriptionDrawer,
    PositionSubtitleDrawer,
    PositionTitleWithIconDrawer,
)
from src.core.entities import DrawPositionsResult, PositionsLayoutDTO
from src.core.entities.config import LayoutConfig, SpacingConfig
from src.core.entities.linkedin_data import LinkedInData


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
        linkedin_data: LinkedInData,
        layout_cfg: LayoutConfig,
        styles: StyleSheet1,
        spacing: SpacingConfig,
    ) -> DrawPositionsResult:
        positions_layout = PositionsLayoutDTO.from_config(layout_cfg=layout_cfg, spacing=spacing)
        y_cursor = positions_layout.body_start_y
        divider_lines = []

        for idx, position in enumerate(linkedin_data.positions):
            y_icon = self.position_title_with_icon_drawer.draw(
                c=c,
                styles=styles,
                spacing_config=spacing,
                layout=positions_layout,
                position_title=position.text_title,
                y_cursor=y_cursor,
            )
            y_cursor = self.position_subtitle_drawer.draw(
                c=c,
                styles=styles,
                spacing_config=spacing,
                layout=positions_layout,
                text=position.subtitle_html or position.text_sub_title,
                y_cursor=y_icon - spacing.line_thickness,
            )
            y_cursor = self.position_description_drawer.draw(
                c=c,
                styles=styles,
                spacing_config=spacing,
                layout=positions_layout,
                text=position.description,
                y_cursor=y_cursor,
            )

            if idx < len(linkedin_data.positions) - 1:
                divider_line = self.divider_line_builder.build(
                    layout_cfg=layout_cfg,
                    spacing=spacing,
                    positions_layout=positions_layout,
                    y_line=y_icon,
                )
                divider_lines.append(divider_line)

        self.final_credit_message_drawer.draw(
            c=c,
            styles=styles,
            layout=positions_layout,
            y_cursor=y_cursor,
        )

        return DrawPositionsResult(divider_lines=divider_lines, line_anchor_x=positions_layout.line_anchor_x)
