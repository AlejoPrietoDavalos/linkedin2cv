"""Formatter de texto por keywords."""

import json
import re
from typing import Literal

from src.core.constants import PATH_KEYWORDS, ensure_runtime_config_file
from src.core.drivers.keyword_text_formatter import (
    CoreKeywordTextFormatter,
    KeywordsConfig,
)


class KeywordTextFormatter(CoreKeywordTextFormatter):
    def load_keywords(self) -> KeywordsConfig:
        path_keywords = ensure_runtime_config_file(PATH_KEYWORDS.name)
        raw = json.loads(path_keywords.read_text(encoding="utf-8"))
        return KeywordsConfig.model_validate(raw)

    def format_text(self, text: str, keywords: KeywordsConfig) -> str:
        if not text or not keywords.keywords:
            return text

        out = text
        for keyword_cfg in sorted(keywords.keywords, key=lambda item: len(item.keyword), reverse=True):
            pattern = re.compile(rf"(?<!\w)({re.escape(keyword_cfg.keyword)})(?!\w)")

            if keyword_cfg.formatter == "bold":
                out = pattern.sub(lambda m: f"<b>{m.group(1)}</b>", out)

        return out

    def format_bracketed(self, text: str, formatter: Literal["bold"]) -> str:
        if formatter != "bold":
            raise ValueError(f"Formatter no soportado: {formatter}")
        return re.sub(r"(\[[^\]]+\])", r"<b>\1</b>", text)
