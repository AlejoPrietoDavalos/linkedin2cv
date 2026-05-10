"""Compresión de PDFs con Ghostscript. Reduce tamaño de currículos generados."""

import subprocess
import shutil
import logging
import tempfile
from pathlib import Path
from typing import Union

from src.core.drivers.ghostscript import CoreGhostScript

logger = logging.getLogger(__name__)


class GhostScript(CoreGhostScript):
    """Compresión de PDFs mediante Ghostscript."""
    
    _GS_COMMAND = "gs"
    
    def _is_available(self) -> bool:
        """Verifica que Ghostscript esté en el PATH."""
        return shutil.which(self._GS_COMMAND) is not None
    
    def compress_pdf(self, path_pdf: Union[str, Path]) -> None:
        """Comprime un PDF reduciendo su tamaño.
        
        Args:
            path_pdf: Ruta al PDF (string o Path).
        """
        if not self._is_available():
            logger.warning(
                "Ghostscript no está instalado; se omite la compresión del PDF final."
            )
            return

        path_pdf = Path(path_pdf)
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            prefix=f"{path_pdf.stem}_",
            dir=path_pdf.parent,
            delete=False,
        ) as tmp:
            path_tmp = Path(tmp.name)
        
        subprocess.run([
            self._GS_COMMAND,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/printer",  # Mejor calidad, ideal para imágenes
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            "-dDownsampleColorImages=true",  # Habilitar submuestreo de imágenes
            "-dColorImageResolution=300",  # Resolución de imágenes (ajusta según lo necesites)
            f"-sOutputFile={path_tmp}",
            str(path_pdf)
        ], check=True)
        path_tmp.replace(path_pdf)
