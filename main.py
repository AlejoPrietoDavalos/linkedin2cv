from typing import Optional
from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from linkedin2cv.builder import BuilderCV
from linkedin2cv.models import LinkedinData, ColorsCV, SizesCV


def load_font():
    path_font = Path("fonts") / "HackNerdFont-Regular.ttf"
    pdfmetrics.registerFont(TTFont("HackNerdFont", str(path_font)))

def extra_process_data(*, data: LinkedinData) -> LinkedinData:
    data.positions = data.positions[:-1]
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
