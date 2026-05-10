from pydantic import BaseModel


class SidebarSection(BaseModel):
    title: str
    text: str


class SidebarSections(BaseModel):
    items: list[SidebarSection]
