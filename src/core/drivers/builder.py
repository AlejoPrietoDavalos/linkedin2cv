"""Interfaz para constructor de CV."""

from abc import ABC, abstractmethod


class CoreBuilderCV(ABC):
    """Interfaz para constructor de CV."""
    
    @abstractmethod
    def build_and_save(self) -> None:
        """Construye y guarda el CV en PDF."""
        pass
    
    @abstractmethod
    def draw_lines(self) -> None:
        """Dibuja líneas adicionales en el PDF."""
        pass
