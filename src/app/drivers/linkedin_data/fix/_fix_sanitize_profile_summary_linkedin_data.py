import re

from src.app.drivers.linkedin_data.fix._fix_common import LinkedinDataFixCommon
from src.app.drivers.linkedin_data.fix._core import CoreLinkedinDataFix
from src.core.entities.linkedin_data import LinkedinData


class FixSanitizeProfileSummaryLinkedinData(CoreLinkedinDataFix):
    """Limpia manualmente el bloque de "Mi página web" del summary de LinkedIn.

    Este fix existe porque el export de LinkedIn trae esa línea embebida dentro de
    `profile.summary`, pero en el CV la URL del portfolio se renderiza en la sección
    de links del sidebar. Por eso removemos ese texto aquí, en la capa de datos.
    """

    _PROFILE_WEBSITE_PATTERN = re.compile(
        r"(?:^|\s)➤\s*Mi página web\s*➤\s*https?://\S+",
        flags=re.IGNORECASE,
    )

    def __init__(self, common: LinkedinDataFixCommon = None) -> None:
        self.common = common or LinkedinDataFixCommon()

    def apply(self, linkedin_data: LinkedinData) -> None:
        summary = linkedin_data.profile.summary
        summary, replaced_count = self._PROFILE_WEBSITE_PATTERN.subn(" ", summary)
        if replaced_count == 0:
            raise ValueError(
                "No se encontró el patrón esperado de 'Mi página web' en profile.summary."
            )
        linkedin_data.profile.summary = self.common.trim_html_break_edges(summary)
