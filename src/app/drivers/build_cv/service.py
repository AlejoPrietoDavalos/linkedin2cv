"""Servicio de construcción del CV en PDF."""

from pathlib import Path
import logging

import fitz
from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.build_cv._pdf_line_drawer import PDFLineDrawer
from src.app.drivers.draw_cv.service import DrawCVService
from src.app.drivers.styles_repository import LayoutRepository, SpacingRepository, StylesRepository
from src.core.constants import PATH_PHOTO
from src.core.drivers.builder import CoreBuilderCV
from src.core.entities import (
    DividerLine,
    DrawPositionsResult,
    LinkedInData,
    PersonalInformation,
)

logger = logging.getLogger(__name__)


class BuildCVService(CoreBuilderCV):
    """Orquesta la construcción y guardado del CV."""

    def __init__(
        self,
        *,
        draw_cv_service: DrawCVService | None = None,
        pdf_line_drawer: PDFLineDrawer | None = None,
    ):
        self.draw_cv_service = draw_cv_service or DrawCVService()
        self.pdf_line_drawer = pdf_line_drawer or PDFLineDrawer()

    def build_and_save(
        self,
        *,
        path_pdf: Path,
        personal_information: PersonalInformation,
        linkedin_data: LinkedInData,
        font_name: str,
    ) -> DrawPositionsResult:
        logger.info("==================== Creando CV ====================")
        if not PATH_PHOTO.exists():
            raise FileNotFoundError(f"No existe la foto de perfil: {PATH_PHOTO}")

        layout_cfg = LayoutRepository.load()
        spacing = SpacingRepository.load()
        styles_config = StylesRepository.load()
        styles = StylesRepository.build_stylesheet(styles_config, font_name)

        canvas = Canvas(str(path_pdf), pagesize=layout_cfg.page_size)

        self.draw_cv_service.draw_background(c=canvas, styles_config=styles_config, layout_cfg=layout_cfg)
        self.draw_cv_service.draw_sidebar(
            c=canvas,
            linkedin_data=linkedin_data,
            personal_information=personal_information,
            layout_cfg=layout_cfg,
            styles_config=styles_config,
            styles=styles,
            spacing=spacing,
        )
        positions_result = self.draw_cv_service.draw_positions(
            c=canvas,
            linkedin_data=linkedin_data,
            layout_cfg=layout_cfg,
            styles=styles,
            spacing=spacing,
        )
        canvas.save()
        logger.info(f">>>>> Export PDF: {path_pdf}")
        return positions_result

    def draw_lines(
        self,
        *,
        path_pdf: Path,
        lines: list[DividerLine],
        color: tuple[float, float, float] = (1, 0, 0),
        width: float = 1.0,
    ) -> None:
        """Dibuja líneas divisorias con fitz.

        FIXME:
        - Esto está hardcodeado a la primera hoja (`doc[0]`).
        - Se hace con fitz porque no pude agregar estas líneas directamente con reportlab
          durante la etapa de render de posiciones.
        """
        # FIXME: Desactivado temporalmente. Las líneas salen rojas y fuera de posición.
        flag = False
        if not flag:
            logger.warning(">>>>>  BUG: Desactivado `draw_lines` (líneas rojas/fuera de posición).")
        else:
            doc = fitz.open(path_pdf)
            if len(doc) != 1:
                doc.close()
                raise ValueError(f"Se esperaba un PDF de 1 página para dibujar líneas, pero se encontraron {len(doc)}.")
            page = doc[0]
            self.pdf_line_drawer.draw_lines(page=page, lines=lines, color=color, width=width)
            doc.saveIncr()
            doc.close()
