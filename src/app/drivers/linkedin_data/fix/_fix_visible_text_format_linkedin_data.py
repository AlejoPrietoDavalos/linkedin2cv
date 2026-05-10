from src.app.drivers.linkedin_data.fix._fix_common import LinkedinDataFixCommon
from src.app.drivers.linkedin_data.fix._core import CoreLinkedinDataFix
from src.core.entities.linkedin_data import LinkedInData
from src.core.hardcoded_config import (
    REPLACE_BULLET_ARROW,
    REPLACE_BULLET_DOT,
    REPLACE_BULLET_SQUARE,
)


class FixVisibleTextFormatLinkedinData(CoreLinkedinDataFix):
    def __init__(self, common: LinkedinDataFixCommon = None) -> None:
        self.common = common or LinkedinDataFixCommon()

    def _format_visible_text(self, text: str) -> str:
        text = text.replace(*REPLACE_BULLET_ARROW)
        text = text.replace(*REPLACE_BULLET_DOT)
        text = text.replace(*REPLACE_BULLET_SQUARE)
        return self.common.trim_html_break_edges(text)

    def apply(self, linkedin_data: LinkedInData) -> None:
        linkedin_data.profile.summary = self._format_visible_text(linkedin_data.profile.summary)

        for position in linkedin_data.positions:
            position.description = self._format_visible_text(position.description)
