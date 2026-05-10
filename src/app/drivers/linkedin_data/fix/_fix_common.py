import re


class LinkedinDataFixCommon:
    def trim_html_break_edges(self, text: str) -> str:
        return re.sub(r"^<br/>|<br/>$", "", text.strip())
