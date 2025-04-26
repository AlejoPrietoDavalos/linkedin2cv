from typing import Optional
from pathlib import Path
import shutil
import re
import subprocess
import os

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

from linkedin2cv.builder import BuilderCV
from linkedin2cv.models import LinkedinData, StyleCV, SizesCV

FOLDER_NAME = "Basic_LinkedInDataExport_04-21-2025"
PHOTO_NAME = "img_profile.png"
AGE = 30
LOCATION = "Buenos Aires, Argentina"
MAIL = "alejoprietodavalos@gmail.com"
URL_WEB = "https://alejoprietodavalos.github.io/"
URL_GITHUB = "https://github.com/AlejoPrietoDavalos/"
URL_LINKEDIN = "https://linkedin.com/in/alejoprietodavalos/"


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
    desc = move_bracketed_to_end(data.positions[IDX_FREELANCE].description)
    desc = put_bold_in_brackets(desc)
    data.positions[IDX_FREELANCE].description = desc
    return data


def comprimir_pdf_con_ghostscript(path_pdf: str) -> None:
    temp_path = path_pdf.replace(".pdf", "_temp.pdf")
    subprocess.run([
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/printer",  # Mejor calidad, ideal para imágenes
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        "-dDownsampleColorImages=true",  # Habilitar submuestreo de imágenes
        "-dColorImageResolution=300",  # Resolución de imágenes (ajusta según lo necesites)
        f"-sOutputFile={temp_path}",
        path_pdf
    ], check=True)
    os.replace(temp_path, path_pdf)


def main(*, folder_name: str, photo_name: Optional[str] = None) -> None:
    colors_cv = StyleCV()
    sizes_cv = SizesCV()
    builder_cv = BuilderCV(
        folder_name=folder_name,
        style_cv=colors_cv,
        sizes_cv=sizes_cv,
        age=AGE,
        location=LOCATION,
        mail=MAIL,
        url_website=URL_WEB,
        url_github=URL_GITHUB,
        url_linkedin=URL_LINKEDIN,
        photo_name=photo_name,
        is_photo_circle=True
    )

    builder_cv.data = extra_process_data(data=builder_cv.data)
    builder_cv.build_and_save()

    path_pdf_final = builder_cv.path_pdf.with_name(f'Curriculum - {builder_cv.data.profile.full_name}.pdf')
    shutil.copy(builder_cv.path_pdf, path_pdf_final)

    comprimir_pdf_con_ghostscript(str(path_pdf_final))


if __name__ == "__main__":
    load_font()
    main(folder_name=FOLDER_NAME, photo_name=PHOTO_NAME)
