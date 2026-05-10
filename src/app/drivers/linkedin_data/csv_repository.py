from typing import List
from pathlib import Path
import logging

import pandas as pd

from src.core.entities.linkedin_data import ProfileLinkedInData, PositionLinkedInData, EducationLinkedInData, LinkedInData
from src.core.constants import (
    PATH_FOLDER_DATA,
    PATH_LINKEDIN_PROFILE,
    PATH_LINKEDIN_POSITIONS,
    PATH_LINKEDIN_EDUCATION,
)
from src.core.drivers.linkedin_csv_repository import CoreLinkedinCSVRepository
from src.app.drivers.linkedin_data._csv_row_formatter import LinkedinCSVRowFormatter
from src.app.drivers.linkedin_data._job_id_attacher import LinkedinJobIdAttacher

logger = logging.getLogger(__name__)


class LinkedinCSVRepository(CoreLinkedinCSVRepository):
    def __init__(
        self,
        row_formatter: LinkedinCSVRowFormatter = None,
        job_id_attacher: LinkedinJobIdAttacher = None,
    ) -> None:
        self.row_formatter = row_formatter or LinkedinCSVRowFormatter()
        self.job_id_attacher = job_id_attacher or LinkedinJobIdAttacher()

    @staticmethod
    def _read_dataframe(path_csv: Path):
        # LinkedIn exports are consumed by string-based domain models; reading as text
        # avoids pandas inferring ints (e.g. 2015) that later fail strict Pydantic validation.
        return pd.read_csv(path_csv, dtype=str)

    def _load_profile(self) -> ProfileLinkedInData:
        row = self._read_dataframe(PATH_LINKEDIN_PROFILE).iloc[0]
        return self.row_formatter.build_model_from_row(row=row, model_cls=ProfileLinkedInData)

    def _load_positions(self) -> List[PositionLinkedInData]:
        df = self._read_dataframe(PATH_LINKEDIN_POSITIONS)
        positions = self.row_formatter.build_models_from_dataframe(df=df, model_cls=PositionLinkedInData)
        self.job_id_attacher.attach(positions)
        return positions

    def _load_educations(self) -> List[EducationLinkedInData]:
        df = self._read_dataframe(PATH_LINKEDIN_EDUCATION)
        return self.row_formatter.build_models_from_dataframe(df=df, model_cls=EducationLinkedInData)

    def load_linkedin_data(self) -> LinkedInData:
        logger.info(f"==================== LinkedIn Data ====================")
        linkedin_data = LinkedInData(
            profile=self._load_profile(),
            positions=self._load_positions(),
            educations=self._load_educations(),
        )
        logger.info(f">>>>> Path data: {PATH_FOLDER_DATA}")
        logger.info(f">>>>> len(positions)={len(linkedin_data.positions)}")
        logger.info(f">>>>> len(educations)={len(linkedin_data.educations)}")
        return linkedin_data
