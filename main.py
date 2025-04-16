from typing import Optional
from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from linkedin2cv.builder import BuilderCV
from linkedin2cv.models import LinkedinData, ColorsCV, SizesCV
from reportlab.pdfbase.pdfmetrics import registerFontFamily


def load_font():
    path_fonts = Path("fonts")
    pdfmetrics.registerFont(TTFont("HackNerdFont", str(path_fonts / "HackNerdFont-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("HackNerdFont-Bold", str(path_fonts / "HackNerdFont-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("HackNerdFont-Italic", str(path_fonts / "HackNerdFont-Italic.ttf")))
    registerFontFamily(
        "HackNerdFont",
        normal="HackNerdFont",
        bold="HackNerdFont-Bold",
        italic="HackNerdFont-Italic"
    )


def translate_date(date_str: Optional[str]) -> Optional[str]:
    """ Cambia la nomenclatura de linkedin de inglés a español."""
    month_map = {
        "Jan": "Enero", "Feb": "Febrero", "Mar": "Marzo", "Apr": "Abril",
        "May": "Mayo", "Jun": "Junio", "Jul": "Julio", "Aug": "Agosto",
        "Sep": "Septiembre", "Oct": "Octubre", "Nov": "Noviembre", "Dec": "Diciembre"
    }
    if not date_str:
        return None
    parts = date_str.split()
    if len(parts) == 2 and parts[0] in month_map:
        return f"{month_map[parts[0]]} {parts[1]}"
    return date_str



def extra_process_data(*, data: LinkedinData,  in_spanish: bool = True) -> LinkedinData:
    # Saco experiencia dando clases.
    data.positions = data.positions[:-1]

    # Convierto las fechas a español.
    if in_spanish:
        for position in data.positions:
            position.started_on = translate_date(position.started_on)
            position.finished_on = translate_date(position.finished_on)
    return data


def main(*, folder_name: str, photo_name: Optional[str] = None):
    AGE = 30
    URL_WEB = "alejoprietodavalos.github.io/"
    URL_GITHUB = "github.com/AlejoPrietoDavalos/"
    colors_cv = ColorsCV()
    sizes_cv = SizesCV()
    builder_cv = BuilderCV(
        folder_name=folder_name,
        colors_cv=colors_cv,
        sizes_cv=sizes_cv,
        age=AGE,
        url_website=URL_WEB,
        url_github=URL_GITHUB,
        photo_name=photo_name,
        photo_circle=True
    )

    # --> Se hace un procesamiento especial si necesitás
    # --> customizar como vienen los datos de linkedin.
    builder_cv.data = extra_process_data(data=builder_cv.data)
    builder_cv.build_and_save()


if __name__ == "__main__":
    load_font()
    main(
        folder_name="Basic_LinkedInDataExport_04-16-2025",
        photo_name="img_profile.png"
    )
