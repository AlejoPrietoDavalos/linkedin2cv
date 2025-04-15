from pathlib import Path

from reportlab.lib import colors

from linkedin2cv.builder import BuilderCV
from linkedin2cv.models import ColorsCV, SizesCV


from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def load_font():
    path_font = Path("fonts") / "HackNerdFont-Regular.ttf"
    pdfmetrics.registerFont(TTFont("HackNerdFont", str(path_font)))


def main(*, path_folder: Path, path_photo: Path):
    colors_cv = ColorsCV()
    sizes_cv = SizesCV()
    builder_cv = BuilderCV(
        path_folder=path_folder,
        colors_cv=colors_cv,
        sizes_cv=sizes_cv,
        path_photo=path_photo,
        photo_circle=True
    )
    builder_cv.build_and_save()



if __name__ == "__main__":
    load_font()

    path_data = Path("data")
    main(
        path_folder=path_data / "Basic_LinkedInDataExport_04-14-2025",
        path_photo=path_data / "img_profile.png"
    )
