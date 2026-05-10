from typing import Optional

from src.app.drivers.linkedin_data.fix._core import CoreLinkedinDataFix
from src.core.entities.linkedin_data import LinkedinData


class FixTranslatePositionDatesLinkedinData(CoreLinkedinDataFix):
    """Itera en todas las posiciones del LinkedinData y traduce las fechas de inicio y fin al español."""
    def apply(self, linkedin_data: LinkedinData) -> None:
        for position in linkedin_data.positions:
            position.started_on = self._translate_date(position.started_on)
            position.finished_on = self._translate_date(position.finished_on)

    @staticmethod
    def _translate_date(date_str: Optional[str]) -> Optional[str]:
        month_map = {
            "Jan": "Enero",
            "Feb": "Febrero",
            "Mar": "Marzo",
            "Apr": "Abril",
            "May": "Mayo",
            "Jun": "Junio",
            "Jul": "Julio",
            "Aug": "Agosto",
            "Sep": "Septiembre",
            "Oct": "Octubre",
            "Nov": "Noviembre",
            "Dec": "Diciembre",
        }
        if not date_str:
            return None
        parts = date_str.split()
        if len(parts) == 2 and parts[0] in month_map:
            return f"{month_map[parts[0]]} {parts[1]}"
        return date_str
