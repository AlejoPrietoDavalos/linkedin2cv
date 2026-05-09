from pathlib import Path
import shutil
import os

from dotenv import load_dotenv

load_dotenv()

from src.app.drivers.build_cv.service import BuildCVService
from src.app.drivers.font_loader import FontLoader, FontLoaderConfig
from src.app.drivers.ghostscript import GhostScript
from src.core.constants import PATH_PDF_OUTPUT
from src.core.entities import PersonalInformation
from src.app.drivers.linkedin_csv_repository import LinkedinCSVRepository


def _load_fonts() -> None:
    FONT_NAME = os.getenv("FONT_NAME")
    if not FONT_NAME:
        raise ValueError("FONT_NAME environment variable is required")
    FontLoader().load_fonts(FontLoaderConfig(base_name=FONT_NAME))


def main(*, path_pdf: Path, personal_information: PersonalInformation) -> None:
    _load_fonts()
    builder_cv = BuildCVService()
    builder_cv.build_and_save(
        path_pdf=path_pdf,
        personal_information=personal_information,
        linkedin_data=linkedin_data,
    )



if __name__ == "__main__":
    personal_information = PersonalInformation()

    linkedin_data_repository = LinkedinCSVRepository()
    linkedin_data = linkedin_data_repository.load_linkedin_data()

    main(path_pdf=PATH_PDF_OUTPUT, personal_information=personal_information)

    # FIXME: Desactivado temporalmente el dibujado de líneas extra sobre el PDF.
    # builder_cv.draw_lines(path_pdf=path_pdf)
    PATH_PDF_OUTPUT_COMPRESSED = PATH_PDF_OUTPUT.with_name(f'Curriculum - {linkedin_data.profile.full_name}.pdf')
    shutil.copy(PATH_PDF_OUTPUT, PATH_PDF_OUTPUT_COMPRESSED)

    # FIXME: Funciona pero no se por qué hay que hacerlo.
    ghostscript = GhostScript()
    ghostscript.compress_pdf(PATH_PDF_OUTPUT_COMPRESSED)
