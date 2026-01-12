from pydantic import BaseModel,Field,model_validator
from typing import Literal,Optional
import pathlib
class RecordSchema(BaseModel):
    key:int|None = None
    item_name: str
    source_path: str 
    item_type: Literal['file', 'folder']
    item_size: int
    classify_result: Literal['oversize_file', 'zip_file', 'normal_file','empty_folder','oversize_folder','overcount_folder','normal_folder']
    process_status: Literal['local','index', 'hash', 'zip', 'zip_hash','unzip','unzip_hash','compare','upload','delete','compile']
    process_result: Literal['success', 'fail']
    md5: Optional[str] = Field(default=None, min_length=32, max_length=32)
    sha1: Optional[str] = Field(default=None, min_length=40, max_length=40)
    sha256: Optional[str] = Field(default=None, min_length=64, max_length=64)
    other_hash_info: Optional[dict] = Field(default=None)
    zipped_path: Optional[str] = Field(default=None)
    zipped_size: Optional[int] = Field(default=None)
    zipped_md5: Optional[str] = Field(default=None, min_length=32, max_length=32)
    zipped_sha1: Optional[str] = Field(default=None, min_length=40, max_length=40)
    zipped_sha256: Optional[str] = Field(default=None, min_length=64, max_length=64)
    other_unzip_info: Optional[dict] = Field(default=None)
    unzip_path: Optional[str] = Field(default=None)
    unzip_size: Optional[int] = Field(default=None)
    unzip_md5: Optional[str] = Field(default=None, min_length=32, max_length=32)
    unzip_sha1: Optional[str] = Field(default=None, min_length=40, max_length=40)
    unzip_sha256: Optional[str] = Field(default=None, min_length=64, max_length=64)
    other_unzip_info: Optional[dict] = Field(default=None)
    is_compiled: bool = Field(default=False)

    @model_validator(mode='after')
    def check_fields(self):
        print('model')
        self._in_check()
        print('in_check')
        return self


    def _in_check(self):
        print('return')
        return self
if __name__ == '__main__':
    record = RecordSchema(
        item_name='test',
        source_path='test',
        item_type='file',
        item_size=1024,
        classify_result='normal_file',
        process_status='local',
        process_result='success'
    )

    print(record.model_dump(include=['item_name','source_path']))
