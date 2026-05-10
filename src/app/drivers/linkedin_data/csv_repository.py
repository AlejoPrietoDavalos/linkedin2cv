from typing import List, Dict, Any, Type, TypeVar
from pathlib import Path
import logging
import json

import pandas as pd
from pydantic import BaseModel

from src.core.entities.linkedin_data import Profile, Position, Education, LinkedinData
from src.core.entities.job_ids import JobIdsConfig
from src.core.constants import (
    PATH_JOB_IDS,
    PATH_FOLDER_DATA,
    PATH_LINKEDIN_PROFILE,
    PATH_LINKEDIN_POSITIONS,
    PATH_LINKEDIN_EDUCATION,
    ensure_runtime_config_file,
)
from src.core.drivers.linkedin_csv_repository import CoreLinkedinCSVRepository

logger = logging.getLogger(__name__)
TModel = TypeVar("TModel", bound=BaseModel)


def _nan2none(v):
    return None if pd.isna(v) else v


class LinkedinCSVRowFormatter:
    def format_key(self, key: str) -> str:
        return key.lower().replace(" ", "_")

    def format_row(self, *, row: pd.Series) -> Dict[str, Any]:
        row_dict: Dict[str, Any] = row.to_dict()
        return {self.format_key(k): _nan2none(v) for k, v in row_dict.items()}

    def _pick_model_fields(
        self, *, data: Dict[str, Any], model_cls: Type[TModel]
    ) -> Dict[str, Any]:
        return {k: v for k, v in data.items() if k in model_cls.model_fields}

    def build_model_from_row(self, *, row: pd.Series, model_cls: Type[TModel]) -> TModel:
        data = self.format_row(row=row)
        return model_cls(**self._pick_model_fields(data=data, model_cls=model_cls))

    def build_models_from_dataframe(
        self, *, df: pd.DataFrame, model_cls: Type[TModel]
    ) -> List[TModel]:
        return [self.build_model_from_row(row=row, model_cls=model_cls) for _, row in df.iterrows()]


class LinkedinJobIdAttacher:
    def _load_job_ids_config(self) -> JobIdsConfig:
        path_job_ids = ensure_runtime_config_file(PATH_JOB_IDS.name)
        raw = json.loads(path_job_ids.read_text(encoding="utf-8"))
        config = JobIdsConfig.model_validate(raw)
        self._validate_unique_job_ids(config)
        return config

    def _validate_unique_job_ids(self, config: JobIdsConfig) -> None:
        all_job_ids = [entry.job_id for entry in config.jobs]
        duplicates = sorted({job_id for job_id in all_job_ids if all_job_ids.count(job_id) > 1})
        if duplicates:
            raise RuntimeError(f"job_id duplicados en config/job_ids.json: {duplicates}")

    def attach(self, positions: List[Position]) -> None:
        logger.info(f">>>>> Attach JobId: {PATH_JOB_IDS}")
        config = self._load_job_ids_config()
        company_to_job_id = {job.company_name: job.job_id for job in config.jobs}

        for position in positions:
            position.job_id = company_to_job_id.get(position.company_name)

        removed_company_names = sorted({p.company_name for p in positions if p.job_id is None})
        if removed_company_names:
            for company_name in removed_company_names:
                logger.warning(f">>>>> (SKIP JOB) job_id no configurado: '{company_name}'")
            
            positions[:] = [p for p in positions if p.job_id is not None]


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

    def _load_profile(self) -> Profile:
        row = self._read_dataframe(PATH_LINKEDIN_PROFILE).iloc[0]
        return self.row_formatter.build_model_from_row(row=row, model_cls=Profile)

    def _load_positions(self) -> List[Position]:
        df = self._read_dataframe(PATH_LINKEDIN_POSITIONS)
        positions = self.row_formatter.build_models_from_dataframe(df=df, model_cls=Position)
        self.job_id_attacher.attach(positions)
        return positions

    def _load_educations(self) -> List[Education]:
        df = self._read_dataframe(PATH_LINKEDIN_EDUCATION)
        return self.row_formatter.build_models_from_dataframe(df=df, model_cls=Education)

    def load_linkedin_data(self) -> LinkedinData:
        logger.info(f"==================== LinkedIn Data ====================")
        linkedin_data = LinkedinData(
            profile=self._load_profile(),
            positions=self._load_positions(),
            educations=self._load_educations(),
        )
        logger.info(f">>>>> Path data: {PATH_FOLDER_DATA}")
        logger.info(f">>>>> len(positions)={len(linkedin_data.positions)}")
        logger.info(f">>>>> len(educations)={len(linkedin_data.educations)}")
        return linkedin_data
