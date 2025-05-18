from typing import Optional
from dotenv import load_dotenv
from pathlib import Path
import shutil
import re
import subprocess
import os
import json

from pydantic import BaseModel, EmailStr
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

from linkedin2cv.builder import BuilderCV
from linkedin2cv.models import LinkedinData, StyleCV, SizesCV

load_dotenv()


class ExtraData(BaseModel):
    folder_linkedin_data: str
    photo_name: str
    age: int
    location: str
    email: EmailStr
    url_web_es: Optional[str] = None    # TODO: Hacer algo con los opcionales.
    url_web_en: Optional[str] = None    # TODO: Hacer algo con los opcionales.
    url_github: Optional[str] = None    # TODO: Hacer algo con los opcionales.
    url_linkedin: Optional[str] = None  # TODO: Hacer algo con los opcionales.

    def save_json(self, *, path_json: Path) -> None:
        with open(path_json, "w") as f:
            json.dump(path_json)


def load_fonts() -> None:
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


def main(*, extra_data: ExtraData) -> None:
    colors_cv = StyleCV()
    sizes_cv = SizesCV()
    builder_cv = BuilderCV(
        folder_name=extra_data.folder_linkedin_data,
        style_cv=colors_cv,
        sizes_cv=sizes_cv,
        age=extra_data.age,
        location=extra_data.location,
        mail=extra_data.email,
        url_website_es=extra_data.url_web_es,
        url_website_en=extra_data.url_web_en,
        url_github=extra_data.url_github,
        url_linkedin=extra_data.url_linkedin,
        photo_name=extra_data.photo_name,
        is_photo_circle=True
    )

    builder_cv.data = extra_process_data(data=builder_cv.data)
    builder_cv.build_and_save()

    path_pdf_final = builder_cv.path_pdf.with_name(f'Curriculum - {builder_cv.data.profile.full_name}.pdf')
    shutil.copy(builder_cv.path_pdf, path_pdf_final)

    compress_pdf_with_ghostscript(str(path_pdf_final))


if __name__ == "__main__":
    load_fonts()

    extra_data = ExtraData(
        folder_linkedin_data=os.getenv("FOLDER_DATA"),
        photo_name=os.getenv("PHOTO_NAME"),
        age=os.getenv("AGE"),
        location=os.getenv("LOCATION"),
        email=os.getenv("EMAIL"),
        url_web_es=os.getenv("URL_WEB_ES"),
        url_web_en=os.getenv("URL_WEB_EN"),
        url_github=os.getenv("URL_GITHUB"),
        url_linkedin=os.getenv("URL_LINKEDIN"),
    )
    main(extra_data=extra_data)
