from typing import Optional
import shutil
import re
import subprocess

from dotenv import load_dotenv
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

load_dotenv()

from linkedin2cv.builder import BuilderCV
from linkedin2cv.constants import PATH_FONTS
from linkedin2cv.models import LinkedinData, PersonalInformation


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


def extra_process_data(*, data: LinkedinData,  in_spanish: bool = True) -> LinkedinData:
    # Saco experiencia dando clases.
    data.positions = data.positions[:-1]

    # Convierto las fechas a español.
    if in_spanish:
        for position in data.positions:
            position.started_on = translate_date(position.started_on)
            position.finished_on = translate_date(position.finished_on)
    
    # Indice del trabajo freelance dentro del CV.
    IDX_FREELANCE = 1
    data.positions[IDX_FREELANCE].company_name = "Profesional independiente"
    desc = move_bracketed_to_end(data.positions[IDX_FREELANCE].description)
    desc = put_bold_in_brackets(desc)
    data.positions[IDX_FREELANCE].description = desc
    return data


def compress_pdf_with_ghostscript(path_pdf: str) -> None:
    """ TODO: Revisar, lo programó ChatGPT."""
    raise_if_ghostscript_is_not_installed()

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


def raise_if_ghostscript_is_not_installed() -> None:
    if shutil.which("gs") is None:
        raise RuntimeError(
            "Ghostscript ('gs') no está instalado. "
            "Revisá el README.md para instrucciones de instalación."
        )


def main(*, personal_information: PersonalInformation) -> None:
    builder_cv = BuilderCV(
        personal_information=personal_information,
    )

    builder_cv.data = extra_process_data(data=builder_cv.data)
    builder_cv.build_and_save()

    path_pdf_final = builder_cv.path_pdf.with_name(f'Curriculum - {builder_cv.data.profile.full_name}.pdf')
    shutil.copy(builder_cv.path_pdf, path_pdf_final)

    compress_pdf_with_ghostscript(str(path_pdf_final))


if __name__ == "__main__":
    load_fonts()

    personal_information = PersonalInformation.from_env()
    main(personal_information=personal_information)
