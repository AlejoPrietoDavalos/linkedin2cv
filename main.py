from typing import Optional
from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from linkedin2cv.builder import BuilderCV
from linkedin2cv.models import ColorsCV, SizesCV


def load_font():
    path_font = Path("fonts") / "HackNerdFont-Regular.ttf"
    pdfmetrics.registerFont(TTFont("HackNerdFont", str(path_font)))


def main(*, folder_name: str, photo_name: Optional[str] = None):
    colors_cv = ColorsCV()
    sizes_cv = SizesCV()
    builder_cv = BuilderCV(
        folder_name=folder_name,
        colors_cv=colors_cv,
        sizes_cv=sizes_cv,
        photo_name=photo_name,
        photo_circle=True
    )
    builder_cv.build_and_save()



if __name__ == "__main__":
    load_font()
    main(
        folder_name="Basic_LinkedInDataExport_04-14-2025",
        photo_name="img_profile.png"
    )
