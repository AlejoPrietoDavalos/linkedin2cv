import re
from typing import Literal

from src.app.drivers.linkedin_data.fix._core import CoreLinkedinDataFix
from src.core.drivers.keyword_text_formatter import CoreKeywordTextFormatter
from src.core.entities.linkedin_data import LinkedinData


class FixFreelanceAdjustmentsLinkedinData(CoreLinkedinDataFix):
    def __init__(self, formatter: CoreKeywordTextFormatter) -> None:
        self.formatter = formatter

    def apply(self, linkedin_data: LinkedinData) -> None:
        idx_freelance = 1
        if len(linkedin_data.positions) <= idx_freelance:
            return

        target = linkedin_data.positions[idx_freelance]
        desc = self._move_bracketed_to_end(target.description)
        desc = self._format_bracketed(desc, formatter="bold")
        target.company_name = "Profesional independiente"
        target.description = desc

    def _format_bracketed(self, text: str, formatter: Literal["bold"]) -> str:
        return self.formatter.format_bracketed(text, formatter)

    @staticmethod
    def _move_bracketed_to_end(text: str) -> str:
        def replacer(line: str) -> str:
            matches = re.findall(r"\[[^\]]+\]", line)
            line_clean = re.sub(r"\[[^\]]+\]", "", line).strip()
            if not matches:
                return line
            bracketed = " ".join(matches)
            if "<br" in line:
                return re.sub(r"(.*?)(<br\s*/?>)", rf"\1 {bracketed}\2", line_clean + "<br/>")
            return f"{line_clean} {bracketed}"

        lines = text.split("<br/>")
        processed = [replacer(line) for line in lines if line.strip()]
        processed = [txt if not txt.startswith("●") else f"<br/>{txt}" for txt in processed]
        return "<br/>".join(processed)
