from src.app.drivers.linkedin_data.fix._core import CoreLinkedinDataFix
from src.core.entities.linkedin_data import LinkedinData


class FixStripLastPositionLinkedinData(CoreLinkedinDataFix):
    def apply(self, linkedin_data: LinkedinData) -> None:
        linkedin_data.positions = linkedin_data.positions[:-1]
