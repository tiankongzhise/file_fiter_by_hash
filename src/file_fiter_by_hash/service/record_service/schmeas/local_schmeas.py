from pydantic import BaseModel,Field
from typing import Literal


class SuccessSchema(BaseModel):
    process_result: Literal['success'] = Field(default='success')

class FailSchema(BaseModel):
    process_result: Literal['fail'] = Field(default='fail')
    fail_reason: dict

class ClassifySuccessSchema(SuccessSchema):
    item_name: str
    source_path: str
    item_type: Literal['file', 'folder']
    item_size: int
    classify_result: Literal['oversize_file', 'zip_file', 'normal_file','empty_folder','oversize_folder','overcount_folder','normal_folder']
    process_status: Literal['classify'] = Field(default='classify')
