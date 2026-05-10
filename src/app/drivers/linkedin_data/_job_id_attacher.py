from typing import List
import logging
import json

from src.core.entities.linkedin_data import PositionLinkedInData
from src.core.entities.job_ids import JobIdsConfig
from src.core.constants import PATH_JOB_IDS, ensure_runtime_config_file

logger = logging.getLogger(__name__)


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

    def attach(self, positions: List[PositionLinkedInData]) -> None:
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
