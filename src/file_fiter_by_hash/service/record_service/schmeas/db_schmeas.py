from pydantic import BaseModel,Field
from typing import Literal


class SuccessSchema(BaseModel):
    key:int = Field(...,description="主键key")
    process_result: Literal['success'] = Field(default='success')

class FailSchema(BaseModel):
    process_result: Literal['fail'] = Field(default='fail')
    db_fail_reason: dict

class ClassifySuccessSchema(SuccessSchema):
    item_name: str
    source_path: str
    item_type: Literal['file', 'folder']
    item_size: int
    classify_result: Literal['oversize_file', 'zip_file', 'normal_file','empty_folder','oversize_folder','overcount_folder','normal_folder']
    process_status: Literal['classify'] = Field(default='classify')

class ClassifyFailSchema(FailSchema):
    item_name: str
    source_path: str
    item_type: Literal['file', 'folder']
    item_size: int
    classify_result: Literal['oversize_file', 'zip_file', 'normal_file','empty_folder','oversize_folder','overcount_folder','normal_folder']
    process_status: Literal['classify'] = Field(default='classify')


if __name__ == '__main__':
    c= ClassifySuccessSchema(
        key=1,
        item_name='test',
        source_path='test',
        item_type='file',
        item_size=1,
        classify_result='normal_file',
        process_status='classify'

    )
    c.key