from pathlib import Path
import logging

from dotenv import load_dotenv

load_dotenv()

from src.app.configure_logging import configure_logging
configure_logging()

from src.app.drivers.build_cv.service import BuildCVService
from src.app.drivers.font_loader import FontLoader
from src.app.drivers.ghostscript import GhostScript
from src.app.drivers.linkedin_data.fix.service import FixLinkedinDataService
from src.core.constants import get_path_pdf_output
from src.core.entities import PersonalInformation
from src.app.drivers.linkedin_data.csv_repository import LinkedinCSVRepository

logger = logging.getLogger(__name__)

def _compress_pdf(path_pdf: Path) -> None:
    ghostscript = GhostScript()
    ghostscript.compress_pdf(path_pdf)
    logger.info(f"~ Export PDF: {path_pdf}")



def main(*, personal_information: PersonalInformation, compress: bool = True) -> None:
    logger.info("==================== Iniciando ====================")
    FontLoader.load_font_from_env()

    linkedin_data_repository = LinkedinCSVRepository()
    linkedin_data = linkedin_data_repository.load_linkedin_data()
    linkedin_data = FixLinkedinDataService().fix(linkedin_data)

    builder_cv = BuildCVService()
    path_pdf = get_path_pdf_output(linkedin_data.profile.full_name)
    positions_result = builder_cv.build_and_save(
        path_pdf=path_pdf,
        personal_information=personal_information,
        linkedin_data=linkedin_data,
    )

    logger.info("==================== Líneas divisorias posición ====================")
    builder_cv.draw_lines(path_pdf=path_pdf, lines=positions_result.divider_lines)

    if compress:
        logger.info("==================== Compress and export PDF ====================")
        _compress_pdf(path_pdf=path_pdf)

if __name__ == "__main__":
    COMPRESS = True
    personal_information = PersonalInformation()
    main(personal_information=personal_information, compress=COMPRESS)
