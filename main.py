from typing import Optional
import shutil
import re

from dotenv import load_dotenv
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

load_dotenv()

from src.app.drivers.builder import BuilderCV
from src.app.drivers.ghostscript import GhostScript
from src.core.constants import PATH_FONTS
from src.core.entities import LinkedinData, PersonalInformation
from src.app.drivers.linkedin_csv_repository import LinkedinCSVRepository


def load_fonts() -> None:
    HNF = "HackNerdFont"
    pdfmetrics.registerFont(TTFont(f"{HNF}", str(PATH_FONTS / f"{HNF}-Regular.ttf")))
    pdfmetrics.registerFont(TTFont(f"{HNF}-Bold", str(PATH_FONTS / f"{HNF}-Bold.ttf")))
    pdfmetrics.registerFont(TTFont(f"{HNF}-Italic", str(PATH_FONTS / f"{HNF}-Italic.ttf")))
    pdfmetrics.registerFont(TTFont(f"{HNF}-BoldItalic", str(PATH_FONTS / f"{HNF}-BoldItalic.ttf")))
    registerFontFamily(
        f"{HNF}",
        normal=f"{HNF}",
        bold=f"{HNF}-Bold",
        italic=f"{HNF}-Italic",
        boldItalic=f"{HNF}-BoldItalic"
    )


def translate_date(date_str: Optional[str]) -> Optional[str]:
    """ Cambia la nomenclatura de linkedin de inglés a español."""
    month_map = {
        "Jan": "Enero",
        "Feb": "Febrero",
        "Mar": "Marzo",
        "Apr": "Abril",
        "May": "Mayo",
        "Jun": "Junio",
        "Jul": "Julio",
        "Aug": "Agosto",
        "Sep": "Septiembre",
        "Oct": "Octubre",
        "Nov": "Noviembre",
        "Dec": "Diciembre"
    }
    if not date_str:
        return None
    parts = date_str.split()
    if len(parts) == 2 and parts[0] in month_map:
        return f"{month_map[parts[0]]} {parts[1]}"
    return date_str


def put_bold_in_brackets(text: str) -> str:
    return re.sub(r"(\[[^\]]+\])", r"<b>\1</b>", text)

def move_bracketed_to_end(text: str) -> str:
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


def extra_process_data(*, linkedin_data: LinkedinData,  in_spanish: bool = True) -> LinkedinData:
    """FIXME: Recontra hardcodeado"""
    # Saco experiencia dando clases.
    linkedin_data.positions = linkedin_data.positions[:-1]

    # Convierto las fechas a español.
    if in_spanish:
        for position in linkedin_data.positions:
            position.started_on = translate_date(position.started_on)
    
    # Indice del trabajo freelance dentro del CV.
    IDX_FREELANCE = 1
    linkedin_data.positions[IDX_FREELANCE].company_name = "Profesional independiente"
    desc = move_bracketed_to_end(linkedin_data.positions[IDX_FREELANCE].description)
    desc = put_bold_in_brackets(desc)
    linkedin_data.positions[IDX_FREELANCE].description = desc
    return linkedin_data


def main(*, personal_information: PersonalInformation) -> None:
    linkedin_data_repository = LinkedinCSVRepository()
    linkedin_data = linkedin_data_repository.load_linkedin_data()
    linkedin_data = extra_process_data(linkedin_data=linkedin_data)

    builder_cv = BuilderCV(
        personal_information=personal_information,
        linkedin_data=linkedin_data,
    )
    builder_cv.build_and_save()

    path_pdf_final = builder_cv.path_pdf.with_name(f'Curriculum - {builder_cv.linkedin_data.profile.full_name}.pdf')
    shutil.copy(builder_cv.path_pdf, path_pdf_final)

    ghostscript = GhostScript()
    ghostscript.compress_pdf(path_pdf_final)


if __name__ == "__main__":
    load_fonts()

    personal_information = PersonalInformation()
    main(personal_information=personal_information)
