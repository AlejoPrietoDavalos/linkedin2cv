from src.app.drivers.keyword_text_formatter import KeywordTextFormatter
from src.app.drivers.linkedin_data.fix._core import CoreLinkedinDataFix
from src.core.drivers.keyword_text_formatter import CoreKeywordTextFormatter
from src.core.entities.linkedin_data import LinkedInData


class FixKeywordsFormatLinkedinData(CoreLinkedinDataFix):
    def __init__(self, formatter: CoreKeywordTextFormatter = None) -> None:
        self.formatter = formatter or KeywordTextFormatter()

    def apply(self, linkedin_data: LinkedInData) -> None:
        keywords = self.formatter.load_keywords()

        linkedin_data.profile.summary = self.formatter.format_text(
            linkedin_data.profile.summary,
            keywords,
        )

        for position in linkedin_data.positions:
            position.description = self.formatter.format_text(position.description, keywords)
