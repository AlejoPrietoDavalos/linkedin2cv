from pathlib import Path
import shutil
import logging

from dotenv import load_dotenv

load_dotenv()

from src.app.configure_logging import configure_logging
configure_logging()

from src.app.drivers.build_cv.service import BuildCVService
from src.app.drivers.font_loader import FontLoader
from src.app.drivers.ghostscript import GhostScript
from src.core.constants import PATH_PDF_OUTPUT
from src.core.entities import PersonalInformation
from src.app.drivers.linkedin_csv_repository import LinkedinCSVRepository

logger = logging.getLogger(__name__)

def _copy_and_compress_pdf(path_pdf: Path, linkedin_data: PersonalInformation) -> None:
    path_pdf_output_compressed = path_pdf.with_name(f'Curriculum - {linkedin_data.profile.full_name}.pdf')
    shutil.copy(path_pdf, path_pdf_output_compressed)

    # FIXME: Funciona pero no se por qué hay que hacerlo.
    ghostscript = GhostScript()
    ghostscript.compress_pdf(path_pdf_output_compressed)
    logger.info(f"~ Export PDF Ghostscript: {path_pdf_output_compressed}")


def main(*, path_pdf: Path, personal_information: PersonalInformation) -> None:
    logger.info("==================== Iniciando ====================")
    FontLoader.load_font_from_env()

    linkedin_data_repository = LinkedinCSVRepository()
    linkedin_data = linkedin_data_repository.load_linkedin_data()

    builder_cv = BuildCVService()
    positions_result = builder_cv.build_and_save(
        path_pdf=path_pdf,
        personal_information=personal_information,
        linkedin_data=linkedin_data,
    )

    logger.info("==================== Líneas divisorias posición ====================")
    builder_cv.draw_lines(path_pdf=path_pdf, lines=positions_result.divider_lines)

    logger.info(f"==================== Copy, compress and export PDF ====================")
    _copy_and_compress_pdf(path_pdf=path_pdf, linkedin_data=linkedin_data)

if __name__ == "__main__":
    personal_information = PersonalInformation()
    main(path_pdf=PATH_PDF_OUTPUT, personal_information=personal_information)
