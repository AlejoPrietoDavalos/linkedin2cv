from typing import List, Dict, Any, Type, TypeVar

import pandas as pd
from pydantic import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)


def _nan2none(v):
    return None if pd.isna(v) else v

def _format_key(key: str) -> str:
    return key.lower().replace(" ", "_")

def _format_row(row: pd.Series) -> Dict[str, Any]:
    row_dict: Dict[str, Any] = row.to_dict()
    return {_format_key(k): _nan2none(v) for k, v in row_dict.items()}

def _pick_model_fields(data: Dict[str, Any], model_cls: Type[TModel]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if k in model_cls.model_fields}


class LinkedinCSVRowFormatter:
    def build_model_from_row(self, *, row: pd.Series, model_cls: Type[TModel]) -> TModel:
        data = _format_row(row=row)
        return model_cls(**_pick_model_fields(data=data, model_cls=model_cls))

    def build_models_from_dataframe(
        self, *, df: pd.DataFrame, model_cls: Type[TModel]
    ) -> List[TModel]:
        return [self.build_model_from_row(row=row, model_cls=model_cls) for _, row in df.iterrows()]
