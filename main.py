from pathlib import Path
import shutil
import os

from dotenv import load_dotenv

load_dotenv()

from src.app.drivers.build_cv.service import BuildCVService
from src.app.drivers.font_loader import FontLoader, FontLoaderConfig
from src.app.drivers.ghostscript import GhostScript
from src.core.constants import PATH_DATA_DIR, PATH_FOLDER_DATA, PDF_EXTENSION
from src.core.entities import PersonalInformation
from src.app.drivers.linkedin_csv_repository import LinkedinCSVRepository


def load_fonts() -> None:
    FONT_NAME = os.getenv("FONT_NAME")
    if not FONT_NAME:
        raise ValueError("FONT_NAME environment variable is required")
    FontLoader().load_fonts(FontLoaderConfig(base_name=FONT_NAME))


def main(*, path_pdf: Path, personal_information: PersonalInformation) -> None:
    load_fonts()

    linkedin_data_repository = LinkedinCSVRepository()
    linkedin_data = linkedin_data_repository.load_linkedin_data()

    builder_cv = BuildCVService()
    builder_cv.build_and_save(
        path_pdf=path_pdf,
        personal_information=personal_information,
        linkedin_data=linkedin_data,
    )
    # FIXME: Desactivado temporalmente el dibujado de líneas extra sobre el PDF.
    # builder_cv.draw_lines(path_pdf=path_pdf)

    path_pdf_final = path_pdf.with_name(f'Curriculum - {linkedin_data.profile.full_name}.pdf')
    shutil.copy(path_pdf, path_pdf_final)

    # FIXME: Funciona pero no se por qué hay que hacerlo.
    ghostscript = GhostScript()
    ghostscript.compress_pdf(path_pdf_final)



if __name__ == "__main__":
    path_pdf = PATH_DATA_DIR / f"{PATH_FOLDER_DATA.stem}{PDF_EXTENSION}"

    personal_information = PersonalInformation()
    main(path_pdf=path_pdf, personal_information=personal_information)
