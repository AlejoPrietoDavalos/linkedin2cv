import logging
from typing import Literal

from src.app.drivers.linkedin_data.fix._core import CoreLinkedinDataFix
from src.app.drivers.keyword_text_formatter import KeywordTextFormatter
from src.core.drivers.keyword_text_formatter import CoreKeywordTextFormatter
from src.core.entities.linkedin_data import LinkedInData, PositionLinkedInData

logger = logging.getLogger(__name__)

JOB_ID_FREELANCE = "freelance"


class FixFreelanceAdjustmentsLinkedinData(CoreLinkedinDataFix):
    def __init__(self, formatter: CoreKeywordTextFormatter = None) -> None:
        self.formatter = formatter or KeywordTextFormatter()

    def apply(self, linkedin_data: LinkedInData) -> None:
        freelance_position_finded = False
        for position in linkedin_data.positions:
            if position.job_id == JOB_ID_FREELANCE:
                self._format_bracketed(position, formatter="bold")
                freelance_position_finded = True
                break
        if not freelance_position_finded:
            logger.warning(f"No se encontró job_id='{JOB_ID_FREELANCE}'.")

    def _format_bracketed(self, position: PositionLinkedInData, formatter: Literal["bold"]) -> None:
        position.description = self.formatter.format_bracketed(position.description, formatter)
