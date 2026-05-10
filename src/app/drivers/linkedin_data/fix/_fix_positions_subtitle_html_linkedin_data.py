from src.app.drivers.linkedin_data.fix._core import CoreLinkedinDataFix
from src.core.entities.linkedin_data import LinkedinData, Position
from src.core.hardcoded_config import format_job_subtitle_html


class FixPositionsSubtitleHtmlLinkedinData(CoreLinkedinDataFix):
    """Pre-formatea el subtitulo de positions para que el drawer no haga lógica de formato."""

    def apply(self, linkedin_data: LinkedinData) -> None:
        for position in linkedin_data.positions:
            position.subtitle_html = self._format_position_subtitle(position)

    @staticmethod
    def _format_position_subtitle(position: Position) -> str:
        # `text_sub_title` es el subtitulo "crudo" (empresa + fechas). Aquí lo convertimos
        # a HTML para ReportLab Paragraph (negrita + prefijo).
        return format_job_subtitle_html(subtitle=position.text_sub_title)

