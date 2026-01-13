from pydantic import BaseModel,Field,model_validator,field_validator
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


class FailSchema(BaseModel):
    is_compile:Literal[False]
    fail_reason: dict

    


class LocalStatusSchema(BaseModel):
    item_name: str
    source_path: str 
    item_type: Literal['file', 'folder']
    item_size: int
    classify_result: Literal['oversize_file', 'zip_file', 'normal_file','empty_folder','oversize_folder','overcount_folder','normal_folder']
    process_status: Literal['local']
    process_result: Literal['success']

class IndexStatusSchema(BaseModel):
    key:int
    item_name: str
    source_path: str 
    item_type: Literal['file', 'folder']
    item_size: int
    classify_result: Literal['oversize_file', 'zip_file', 'normal_file','empty_folder','oversize_folder','overcount_folder','normal_folder']
    process_status: Literal['index']
    process_result: Literal['success']

class HashStatusSchema(BaseModel):
    key:int
    item_name: str
    source_path: str 
    item_type: Literal['file', 'folder']
    item_size: int
    classify_result: Literal['oversize_file', 'zip_file', 'normal_file','empty_folder','oversize_folder','overcount_folder','normal_folder']
    process_status: Literal['hash']
    process_result: Literal['success','fail']
    md5: Optional[str] = Field(default=None, min_length=32, max_length=32)
    sha1: Optional[str] = Field(default=None, min_length=40, max_length=40)
    sha256: Optional[str] = Field(default=None, min_length=64, max_length=64)
    other_hash_info: Optional[dict] = Field(default=None)

    @field_validator('source_path')
    def _validate_source_path(cls, value):
        temp = pathlib.Path(value)
        if not temp._is_file():
            raise ValueError('source_path must exist')
        if temp.suffix != '.zip':
            raise ValueError('source_path must be a zip file')
        return value

    @model_validator(mode='after')
    def _validate_hash_fields(self):
        if self.process_result == 'success':
            if not all([self.md5, self.sha1, self.sha256]):
                raise ValueError('md5, sha1, sha256 must be set when process_result is success')
        return self
class ZipStatusSchema(BaseModel):
    key:int
    item_name: str
    source_path: str 
    item_type: Literal['file', 'folder']
    item_size: int
    classify_result: Literal['oversize_file', 'zip_file', 'normal_file','empty_folder','oversize_folder','overcount_folder','normal_folder']
    process_status: Literal['zip']
    process_result: Literal['success','fail']
    md5:str = Field(..., min_length=32, max_length=32)
    sha1:str = Field(..., min_length=40, max_length=40)
    sha256:str = Field(..., min_length=64, max_length=64)
    zipped_path: Optional[str] = Field(default=None)
    zipped_size: Optional[int] = Field(default=None)


    @field_validator('zipped_path','source_path')
    def _validate_zipped_path(cls, value):
        temp = pathlib.Path(value)
        if not temp._is_file():
            raise ValueError('zipped_path must exist')
        if temp.suffix != '.zip':
            raise ValueError('zipped_path must be a zip file')
        return value

    @model_validator(mode='after')
    def _validate_zip_fields(self):
        if self.process_result == 'success':
            if not all([self.zipped_path, self.zipped_size]):
                raise ValueError('zipped_path, zipped_size must be set when process_result is success')
            if self.zipped_size != pathlib.Path(self.zipped_path).stat().st_size:
                raise ValueError('zipped_path size must equal to zipped_size')
        else:
            if any([self.zipped_path, self.zipped_size]):
                raise ValueError('zipped_path, zipped_size must be None when process_result is fail')
        return self

class ZipHashStatusSchema(BaseModel):
    key:int
    item_name: str
    source_path: str 
    item_type: Literal['file', 'folder']
    item_size: int
    classify_result: Literal['oversize_file', 'zip_file', 'normal_file','empty_folder','oversize_folder','overcount_folder','normal_folder']
    process_status: Literal['zip_hash']
    process_result: Literal['success','fail']
    md5:str = Field(..., min_length=32, max_length=32)
    sha1:str = Field(..., min_length=40, max_length=40)
    sha256:str = Field(..., min_length=64, max_length=64)
    zipped_path: str
    zipped_size: int
    zipped_md5: Optional[str] = Field(default=None, min_length=32, max_length=32)
    zipped_sha1: Optional[str] = Field(default=None, min_length=40, max_length=40)
    zipped_sha256: Optional[str] = Field(default=None, min_length=64, max_length=64)
    other_zip_info: Optional[dict] = Field(default=None)

    @field_validator('zipped_path','source_path')
    def _validate_zipped_path(cls, value):
        temp = pathlib.Path(value)
        if not temp._is_file():
            raise ValueError('zipped_path must exist')
        if temp.suffix != '.zip':
            raise ValueError('zipped_path must be a zip file')
        return value

    @model_validator(mode='after')
    def _validate_zip_fields(self):
        if self.process_result == 'success':
            if not all([self.zipped_md5, self.zipped_sha1, self.zipped_sha256]):
                raise ValueError('zipped_md5, zipped_sha1, zipped_sha256 must be set when process_result is success')
            if self.zipped_size != pathlib.Path(self.zipped_path).stat().st_size:
                raise ValueError('zipped_path size must equal to zipped_size')
        else:
            if any([self.zipped_md5, self.zipped_sha1, self.zipped_sha256]):
                raise ValueError('zipped_md5, zipped_sha1, zipped_sha256 must be None when process_result is fail')
        return self

class UnzipStatusSchema(BaseModel):
    key:int
    item_name: str
    source_path: str 
    item_type: Literal['file', 'folder']
    item_size: int
    classify_result: Literal['oversize_file', 'zip_file', 'normal_file','empty_folder','oversize_folder','overcount_folder','normal_folder']
    process_status: Literal['unzip']
    process_result: Literal['success','fail']
    md5:str = Field(..., min_length=32, max_length=32)
    sha1:str = Field(..., min_length=40, max_length=40)
    sha256:str = Field(..., min_length=64, max_length=64)
    zipped_path: str
    zipped_size: int
    zipped_md5: str = Field(..., min_length=32, max_length=32)
    zipped_sha1: str = Field(..., min_length=40, max_length=40)
    zipped_sha256: str = Field(..., min_length=64, max_length=64)
    other_zip_info: Optional[dict] = Field(...)
    unzip_path: Optional[str] = Field(default=None)
    unzip_size: Optional[int] = Field(default=None)

    @field_validator('zipped_path','source_path')
    def _validate_zipped_path(cls, value):
        temp = pathlib.Path(value)
        if not temp._is_file():
            raise ValueError('zipped_path must exist')
        if temp.suffix != '.zip':
            raise ValueError('zipped_path must be a zip file')
        return value

    @field_validator('unzip_path')
    def _validate_unzip_path(cls, value):
        temp = pathlib.Path(value)
        match cls.process_result:
            case 'success':
                if not temp.exists():
                    raise ValueError('unzip_path must exist,when process_status is unzip and process_result is success')
            case 'fail':
                if temp.exists():
                    raise ValueError('unzip_path must not exist,when process_status is unzip and process_result is fail')
        return value

    @model_validator(mode='after')
    def _validate_unzip_fields(self):
        if self.process_result == 'success':
            if not all([self.unzip_path, self.unzip_size]):
                raise ValueError('unzip_path, unzip_size must be set when process_result is success')
        else:
            if any([self.unzip_path, self.unzip_size]):
                raise ValueError('unzip_path, unzip_size must be None when process_result is fail')
        return self

class UnzipHashStatusSchemaSuccess(BaseModel):
    key:int
    item_name: str
    source_path: str 
    item_type: Literal['file', 'folder']
    item_size: int
    classify_result: Literal['oversize_file', 'zip_file', 'normal_file','empty_folder','oversize_folder','overcount_folder','normal_folder']
    process_status: Literal['unzip_hash']
    process_result: Literal['success']
    md5:str = Field(..., min_length=32, max_length=32)
    sha1:str = Field(..., min_length=40, max_length=40)
    sha256:str = Field(..., min_length=64, max_length=64)
    zipped_path: str
    zipped_size: int
    zipped_md5: str = Field(..., min_length=32, max_length=32)
    zipped_sha1: str = Field(..., min_length=40, max_length=40)
    zipped_sha256: str = Field(..., min_length=64, max_length=64)
    other_zip_info: Optional[dict] = Field(...)
    unzip_path: str
    unzip_size: int
    unzip_md5: str = Field(..., min_length=32, max_length=32)
    unzip_sha1: str = Field(..., min_length=40, max_length=40)
    unzip_sha256: str = Field(..., min_length=64, max_length=64)
    other_unzip_info: Optional[dict] = Field(default=None)
    @field_validator('zipped_path','source_path','unzip_path')
    def _validate_zipped_path(cls, value):
        temp = pathlib.Path(value)
        if not temp.exists():
            raise ValueError('zipped_path,source_path,unzip_path must exist')
        return value

class UnzipHashStatusSchemaFail(BaseModel):
    key:int
    item_name: str
    source_path: str 
    item_type: Literal['file', 'folder']
    item_size: int
    classify_result: Literal['oversize_file', 'zip_file', 'normal_file','empty_folder','oversize_folder','overcount_folder','normal_folder']
    process_status: Literal['unzip_hash']
    process_result: Literal['success']
    md5:str = Field(..., min_length=32, max_length=32)
    sha1:str = Field(..., min_length=40, max_length=40)
    sha256:str = Field(..., min_length=64, max_length=64)
    zipped_path: str
    zipped_size: int
    zipped_md5: str = Field(..., min_length=32, max_length=32)
    zipped_sha1: str = Field(..., min_length=40, max_length=40)
    zipped_sha256: str = Field(..., min_length=64, max_length=64)
    other_zip_info: Optional[dict] = Field(...)
    unzip_path: str
    unzip_size: int
    unzip_md5: None
    unzip_sha1: str = Field(..., min_length=40, max_length=40)
    unzip_sha256: str = Field(..., min_length=64, max_length=64)
    other_unzip_info: Optional[dict] = Field(default=None)
    @field_validator('zipped_path','source_path','unzip_path')
    def _validate_zipped_path(cls, value):
        temp = pathlib.Path(value)
        if not temp.exists():
            raise ValueError('zipped_path,source_path,unzip_path must exist')
        return value