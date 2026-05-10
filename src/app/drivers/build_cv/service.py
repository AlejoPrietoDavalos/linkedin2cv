"""Servicio de construcción del CV en PDF."""

from pathlib import Path
from typing import Optional

import fitz
from reportlab.lib.styles import StyleSheet1
from reportlab.pdfgen.canvas import Canvas

from src.app.drivers.build_cv._pdf_line_drawer import PDFLineDrawer
from src.app.drivers.draw_cv.service import DrawCVService
from src.core.constants import PATH_PHOTO
from src.core.drivers.builder import CoreBuilderCV
from src.core.entities import (
    BackgroundDrawCfg,
    BuilderCVConfig,
    DrawCVConfig,
    LinkedinData,
    PersonalInformation,
    PhotoDrawCfg,
    PositionsDrawCfg,
    SidebarDrawCfg,
    SizesCV,
    StyleCV,
)

logger = logging.getLogger(__name__)


class BuildCVService(CoreBuilderCV):
    """Orquesta la construcción y guardado del CV."""

    def __init__(
        self,
        *,
        draw_cv_service: Optional[DrawCVService] = None,
        pdf_line_drawer: Optional[PDFLineDrawer] = None,
    ):
        self.draw_cv_service = draw_cv_service or DrawCVService()
        self.pdf_line_drawer = pdf_line_drawer or PDFLineDrawer()
        self.divider_lines = []
        self.line_anchor_x: float | None = None

    def build_and_save(
        self,
        *,
        path_pdf: Path,
        personal_information: PersonalInformation,
        linkedin_data: LinkedinData,
        style_cv: Optional[StyleCV] = None,
        sizes_cv: Optional[SizesCV] = None,
        cfg_builder: Optional[BuilderCVConfig] = None,
    ) -> DrawPositionsResult:
        logger.info("==================== Creando CV ====================")
        if not PATH_PHOTO.exists():
            raise FileNotFoundError(f"No existe la foto de perfil: {PATH_PHOTO}")

        style_cv = style_cv or StyleCV()
        sizes_cv = sizes_cv or SizesCV()
        cfg_builder = cfg_builder or BuilderCVConfig()
        draw_config = DrawCVConfig()
        page_width, page_height = cfg_builder.page_size
        canvas = Canvas(str(path_pdf), pagesize=cfg_builder.page_size)
        styles: StyleSheet1 = style_cv.get_styles()

        self.draw_cv_service.draw_background(
            c=canvas,
            cfg=BackgroundDrawCfg(
                color=(
                    style_cv.background.red,
                    style_cv.background.green,
                    style_cv.background.blue,
                ),
                page_width=page_width,
                page_height=page_height,
            ),
        )
        self.draw_cv_service.draw_sidebar(
            c=canvas,
            cfg=SidebarDrawCfg(
                linkedin_data=linkedin_data,
                personal_information=personal_information,
                sizes_cv=sizes_cv,
                style_cv=style_cv,
                styles=styles,
                page_height=page_height,
            ),
            draw_config=draw_config,
        )
        self.draw_cv_service.draw_photo(
            c=canvas,
            cfg=PhotoDrawCfg(
                path_photo=PATH_PHOTO,
                sizes_cv=sizes_cv,
                page_height=page_height,
                is_photo_circle=cfg_builder.is_photo_circle,
            ),
            draw_config=draw_config,
        )
        positions_result = self.draw_cv_service.draw_positions(
            c=canvas,
            cfg=PositionsDrawCfg(
                linkedin_data=linkedin_data,
                sizes_cv=sizes_cv,
                styles=styles,
                page_width=page_width,
                page_height=page_height,
            ),
            draw_config=draw_config,
        )
        canvas.save()
        logger.info(f"~ Export PDF: {path_pdf}")
        return positions_result

    def draw_lines(
        self,
        *,
        path_pdf: Path,
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
        # doc = fitz.open(path_pdf)
        # if len(doc) != 1:
        #     doc.close()
        #     raise ValueError(f"Se esperaba un PDF de 1 página para dibujar líneas, pero se encontraron {len(doc)}.")
        # page = doc[0]
        # self.pdf_line_drawer.draw_lines(page=page, lines=self.divider_lines, color=color, width=width)
        # doc.saveIncr()
        # doc.close()
        _ = (path_pdf, color, width)
