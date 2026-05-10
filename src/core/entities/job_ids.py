from pydantic import BaseModel


class JobId(BaseModel):
    company_name: str
    job_id: str


class JobIdsConfig(BaseModel):
    jobs: list[JobId]
