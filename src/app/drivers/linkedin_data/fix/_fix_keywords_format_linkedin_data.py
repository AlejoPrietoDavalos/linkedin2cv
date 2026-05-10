from src.app.drivers.linkedin_data.fix._core import CoreLinkedinDataFix
from src.core.drivers.keyword_text_formatter import CoreKeywordTextFormatter
from src.core.entities.linkedin_data import LinkedinData


class FixKeywordsFormatLinkedinData(CoreLinkedinDataFix):
    def __init__(self, formatter: CoreKeywordTextFormatter) -> None:
        self.formatter = formatter

    def apply(self, linkedin_data: LinkedinData) -> None:
        keywords = self.formatter.load_keywords()

        linkedin_data.profile.summary = self.formatter.format_text(
            linkedin_data.profile.summary,
            keywords,
        )

        for position in linkedin_data.positions:
            position.description = self.formatter.format_text(position.description, keywords)
