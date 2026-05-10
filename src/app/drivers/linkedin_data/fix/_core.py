from abc import ABC, abstractmethod

from src.core.entities.linkedin_data import LinkedinData


class CoreLinkedinDataFix(ABC):
    @abstractmethod
    def apply(self, linkedin_data: LinkedinData) -> None:
        raise NotImplementedError
