from typing import Optional
from pathlib import Path
import shutil

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from linkedin2cv.builder import BuilderCV
from linkedin2cv.models import LinkedinData, StyleCV, SizesCV
from reportlab.pdfbase.pdfmetrics import registerFontFamily

FOLDER_NAME = "Basic_LinkedInDataExport_04-21-2025"
PHOTO_NAME = "img_profile.png"
AGE = 30
LOCATION = "Buenos Aires, Argentina"
URL_WEB = "https://alejoprietodavalos.github.io/"
URL_GITHUB = "https://github.com/AlejoPrietoDavalos/"


def load_font() -> None:
    HNF = "HackNerdFont"
    path_fonts = Path("fonts")
    pdfmetrics.registerFont(TTFont(f"{HNF}", str(path_fonts / f"{HNF}-Regular.ttf")))
    pdfmetrics.registerFont(TTFont(f"{HNF}-Bold", str(path_fonts / f"{HNF}-Bold.ttf")))
    pdfmetrics.registerFont(TTFont(f"{HNF}-Italic", str(path_fonts / f"{HNF}-Italic.ttf")))
    pdfmetrics.registerFont(TTFont(f"{HNF}-BoldItalic", str(path_fonts / f"{HNF}-BoldItalic.ttf")))
    registerFontFamily(
        f"{HNF}",
        normal=f"{HNF}",
        bold=f"{HNF}-Bold",
        italic=f"{HNF}-Italic",
        boldItalic="HackNerdFont-BoldItalic"
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

import re
def put_bold_in_brackets(text: str) -> str:
    return re.sub(r"(\[[^\]]+\])", r"<b>\1</b>", text)

def extra_process_data(*, data: LinkedinData,  in_spanish: bool = True) -> LinkedinData:
    # Saco experiencia dando clases.
    data.positions = data.positions[:-1]

    # Convierto las fechas a español.
    if in_spanish:
        for position in data.positions:
            position.started_on = translate_date(position.started_on)
            position.finished_on = translate_date(position.finished_on)
    
    IDX_FREELANCE = 1   # Indice del trabajo freelance dentro del CV.
    data.positions[IDX_FREELANCE].company_name = "Profesional independiente"
    data.positions[IDX_FREELANCE].description = put_bold_in_brackets(data.positions[IDX_FREELANCE].description)
    return data


def main(*, folder_name: str, photo_name: Optional[str] = None) -> None:
    colors_cv = StyleCV()
    sizes_cv = SizesCV()
    builder_cv = BuilderCV(
        folder_name=folder_name,
        style_cv=colors_cv,
        sizes_cv=sizes_cv,
        age=AGE,
        location=LOCATION,
        url_website=URL_WEB,
        url_github=URL_GITHUB,
        photo_name=photo_name,
        is_photo_circle=True
    )

    # --> Se hace un procesamiento especial si necesitás
    # --> customizar como vienen los datos de linkedin.
    builder_cv.data = extra_process_data(data=builder_cv.data)
    builder_cv.build_and_save()
    shutil.copy(builder_cv.path_pdf, builder_cv.path_pdf.with_name(f'Curriculum - {builder_cv.data.profile.full_name}.pdf'))
    


if __name__ == "__main__":
    load_font()
    main(folder_name=FOLDER_NAME, photo_name=PHOTO_NAME)
