import logging
from dataclasses import dataclass

from src.app.drivers.keyword_text_formatter import KeywordTextFormatter
from src.app.drivers.linkedin_data.fix._core import CoreLinkedinDataFix
from src.app.drivers.linkedin_data.fix._fix_freelance_adjustments_linkedin_data import (
    FixFreelanceAdjustmentsLinkedinData,
)
from src.app.drivers.linkedin_data.fix._fix_keywords_format_linkedin_data import (
    FixKeywordsFormatLinkedinData,
)
from src.app.drivers.linkedin_data.fix._fix_strip_last_position_linkedin_data import (
    FixStripLastPositionLinkedinData,
)
from src.app.drivers.linkedin_data.fix._fix_translate_position_dates_linkedin_data import (
    FixTranslatePositionDatesLinkedinData,
)
from src.core.drivers.keyword_text_formatter import CoreKeywordTextFormatter
from src.core.entities.linkedin_data import LinkedinData

logger = logging.getLogger(__name__)


@dataclass
class FixesPipelineDTO:
    fixes: dict[str, CoreLinkedinDataFix]


class FixLinkedinDataService:
    def __init__(
        self,
        *,
        formatter: CoreKeywordTextFormatter | None = None,
        fixes: dict[str, CoreLinkedinDataFix] | None = None,
    ) -> None:
        formatter = formatter or KeywordTextFormatter()
        self.pipeline = FixesPipelineDTO(
            fixes=fixes
            or {
                "strip_last_position": FixStripLastPositionLinkedinData(),
                "translate_position_dates_to_spanish": FixTranslatePositionDatesLinkedinData(),
                "normalize_freelance_position": FixFreelanceAdjustmentsLinkedinData(formatter=formatter),
                "highlight_keywords_in_text": FixKeywordsFormatLinkedinData(formatter=formatter),
            }
        )

    def fix(self, linkedin_data: LinkedinData) -> LinkedinData:
        logger.info("==================== FIX LinkedIn Data ====================")
        for fix_name, fix in self.pipeline.fixes.items():
            logger.info(f"===== fix.start={fix_name} =====")
            fix.apply(linkedin_data)
        return linkedin_data
