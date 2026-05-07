import shutil
import os

from dotenv import load_dotenv

load_dotenv()

from src.app.drivers.builder import BuilderCV
from src.app.drivers.font_loader import FontLoader, FontLoaderConfig
from src.app.drivers.ghostscript import GhostScript
from src.core.entities import PersonalInformation
from src.app.drivers.linkedin_csv_repository import LinkedinCSVRepository


def load_fonts() -> None:
    FONT_NAME = os.getenv("FONT_NAME")
    if not FONT_NAME:
        raise ValueError("FONT_NAME environment variable is required")
    FontLoader().load_fonts(FontLoaderConfig(base_name=FONT_NAME))


def main(*, personal_information: PersonalInformation) -> None:
    load_fonts()

    linkedin_data_repository = LinkedinCSVRepository()
    linkedin_data = linkedin_data_repository.load_linkedin_data()

    builder_cv = BuilderCV(
        personal_information=personal_information,
        linkedin_data=linkedin_data,
    )
    builder_cv.build_and_save()

    path_pdf_final = builder_cv.path_pdf.with_name(f'Curriculum - {builder_cv.linkedin_data.profile.full_name}.pdf')
    shutil.copy(builder_cv.path_pdf, path_pdf_final)

    ghostscript = GhostScript()
    ghostscript.compress_pdf(path_pdf_final)


if __name__ == "__main__":
    personal_information = PersonalInformation()
    main(personal_information=personal_information)
