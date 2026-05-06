"""Interfaz para compresión de PDFs con Ghostscript."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union


class CoreGhostScript(ABC):
    """Interfaz para comprimir PDFs."""
    
    @abstractmethod
    def compress_pdf(self, path_pdf: Union[str, Path]) -> None:
        """Comprime un PDF reduciendo su tamaño.
        
        Args:
            path_pdf: Ruta al PDF (string o Path).
        """
        pass
