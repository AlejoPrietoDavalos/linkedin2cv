"""Post-procesado de LinkedinData en memoria."""

from src.core.drivers.keyword_text_formatter import CoreKeywordTextFormatter
from src.core.entities.linkedin_data import LinkedinData
from src.app.drivers.keyword_text_formatter import KeywordTextFormatter


class FixLinkedinData:
    def __init__(self, formatter: CoreKeywordTextFormatter = None) -> None:
        self.formatter = formatter or KeywordTextFormatter()

    def fix(self, linkedin_data: LinkedinData) -> None:
        keywords = self.formatter.load_keywords()

        linkedin_data.profile.summary = self.formatter.format_text(
            linkedin_data.profile.summary,
            keywords,
        )

        for position in linkedin_data.positions:
            position.description = self.formatter.format_text(
                position.description,
                keywords,
            )
