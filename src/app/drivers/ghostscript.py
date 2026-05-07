"""Compresión de PDFs con Ghostscript. Reduce tamaño de currículos generados."""

import subprocess
import os
import shutil
from pathlib import Path
from typing import Union

from src.core.drivers.ghostscript import CoreGhostScript


class GhostScript(CoreGhostScript):
    """Compresión de PDFs mediante Ghostscript."""
    
    _GS_COMMAND = "gs"
    
    def __init__(self):
        """Valida que Ghostscript esté instalado."""
        self._validate_installation()
    
    def _validate_installation(self) -> None:
        """Verifica que Ghostscript esté en el PATH."""
        if shutil.which(self._GS_COMMAND) is None:
            raise RuntimeError(
                f"Ghostscript ('{self._GS_COMMAND}') no está instalado. "
                "Revisá el README.md para instrucciones de instalación."
            )
    
    def compress_pdf(self, path_pdf: Union[str, Path]) -> None:
        """Comprime un PDF reduciendo su tamaño.
        
        Args:
            path_pdf: Ruta al PDF (string o Path).
        """
        path_pdf = Path(path_pdf)
        path_tmp = path_pdf.with_name(f'{path_pdf.stem}_temp.pdf')
        
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
        os.replace(path_tmp, path_pdf)
