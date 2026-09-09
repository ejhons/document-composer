from typing import List, Union
from pydantic import BaseModel, Field

class FilePathRequest(BaseModel):
    path: str

class FilePathResponse(BaseModel):
    path: str
    name: str
    extension: str

class FilePathListResponse(BaseModel):
    files: list[FilePathResponse] = Field(default_factory=list)

class DirectoryResponse(BaseModel):
    name: str
    files: list[FilePathResponse] = Field(default_factory=list)
    dir: list["DirectoryResponse"] = Field(default_factory=list)

class FileContentResponse(BaseModel):
    path: str
    content: str

class FileContentRequest(BaseModel):
    path: str
    content: str

class FileTreeResponse(DirectoryResponse):
    pass

PathResponse = FilePathResponse | DirectoryResponse
