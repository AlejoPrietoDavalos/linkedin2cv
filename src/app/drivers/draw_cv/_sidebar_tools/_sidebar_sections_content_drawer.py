from typing import List

from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import Paragraph, Spacer

from src.app.drivers.draw_cv._sidebar_tools._sidebar_section_text_drawer import SidebarSectionTextDrawer
from src.app.drivers.keyword_text_formatter import KeywordTextFormatter
from src.app.drivers.linkedin_data.fix._fix_visible_text_format_linkedin_data import FixVisibleTextFormatLinkedinData
from src.app.drivers.styles_repository import SidebarSectionsRepository
from src.core.constants import PATH_SECTIONS_DIR
from src.core.drivers.keyword_text_formatter import CoreKeywordTextFormatter
from src.core.entities.config import SidebarSectionCfg, SidebarSectionsCfg, SpacingConfig
from src.core.entities.linkedin_data import LinkedInData
from src.core.hardcoded_config import format_tech_stack_split_label

# Maps section_id → index in the LinkedIn summary split (tech_summary | tech_stack).
_SUMMARY_SPLIT_IDX: dict[str, int] = {
    "tech_summary": 0,
    "tech_stack": 1,
}


class SidebarSectionsContentDrawer:
    def __init__(
        self,
        section_text_drawer: SidebarSectionTextDrawer | None = None,
        sections_cfg: SidebarSectionsCfg | None = None,
        keyword_formatter: CoreKeywordTextFormatter | None = None,
        visible_text_formatter: FixVisibleTextFormatLinkedinData | None = None,
    ) -> None:
        self.section_text_drawer = section_text_drawer or SidebarSectionTextDrawer()
        self.sections_cfg = sections_cfg or SidebarSectionsRepository.load()
        self.keyword_formatter = keyword_formatter or KeywordTextFormatter()
        self.visible_text_formatter = visible_text_formatter or FixVisibleTextFormatLinkedinData()

    def _load_section_from_file(self, section_id: str) -> str:
        path = PATH_SECTIONS_DIR / f"{section_id}.txt"
        if not path.exists():
            raise FileNotFoundError(f"No se encontró el archivo de sección: {path}")
        text = path.read_text(encoding="utf-8").strip()
        text = text.replace("\n", "<br/>")
        return self.visible_text_formatter.format_visible_text(text)

    def _split_summary_into_tech_sections(self, linkedin_data: LinkedInData) -> dict[str, str]:
        split_label = format_tech_stack_split_label(self.sections_cfg.sections["tech_stack"].title)
        if split_label not in linkedin_data.profile.summary:
            raise ValueError(f"El texto '{split_label}' no está en summary.")
        parts = linkedin_data.profile.summary.split(split_label)
        return {section_id: parts[idx].strip() for section_id, idx in _SUMMARY_SPLIT_IDX.items()}

    def _fill_sections(self, linkedin_data: LinkedInData) -> list[SidebarSectionCfg]:
        linkedin_texts = self._split_summary_into_tech_sections(linkedin_data)
        keywords = self.keyword_formatter.load_keywords()
        sections = []
        for section_id in self.sections_cfg.sections_order:
            section = self.sections_cfg.sections[section_id]
            if section_id in _SUMMARY_SPLIT_IDX:
                text = self.visible_text_formatter.format_visible_text(linkedin_texts[section_id])
            else:
                text = self.keyword_formatter.format_text(
                    self._load_section_from_file(section_id), keywords
                )
            sections.append(SidebarSectionCfg(title=section.title, text=text))
        return sections

    def build(self, *, linkedin_data: LinkedInData, styles: StyleSheet1, spacing: SpacingConfig) -> List[Paragraph | Spacer]:
        content: List[Paragraph | Spacer] = []
        for section in self._fill_sections(linkedin_data):
            content.append(Spacer(1, spacing.dist_between_title_text_sidebar))
            content.extend(
                self.section_text_drawer.build(
                    title=section.title,
                    text=section.text,
                    styles=styles,
                    dist_between_title_sidebar_to_text=spacing.dist_between_title_sidebar_to_text,
                )
            )
        return content
