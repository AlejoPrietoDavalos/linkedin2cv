"""Interfaz del repositorio de LinkedIn CSV."""

from abc import ABC, abstractmethod

from src.core.entities import LinkedInData


class CoreLinkedinCSVRepository(ABC):
    """Interfaz para cargar datos de LinkedIn desde CSV."""

    @abstractmethod
    def load_linkedin_data(self) -> LinkedInData:
        """Carga los datos de LinkedIn y devuelve el modelo unificado."""
        pass
