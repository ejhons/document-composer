from dcp_api.api.mappers.files import FilesMapper
from fastapi import APIRouter, Depends, UploadFile

from dcp_api.api.dependencies import get_file_service
from dcp_api.application.files import FileService


router = APIRouter(
    prefix="/projects/{project_id}/components",
    tags=["files", "components"],
)

mapper = FilesMapper()

@router.get("")
async def get_components(
    project_id: str,
    service: FileService = Depends(
        get_file_service
    ),
):

    path_list = service.list_files(
        project_id=project_id
    )

    return mapper.files_to_response(
        paths=path_list
    )
# {
#         "files": file_list,
#     }


@router.post("")
async def upload_component(
    project_id: str,
    file: UploadFile,
    service: FileService = Depends(
        get_file_service
    ),
):
    content = await file.read()

    path = service.save_file(
        project_id=project_id,
        filename=file.filename or "",
        content=content,
    )

    return mapper.path_to_response(
        path=path.as_posix()
    )
# {
#         "filename": path.name,
#     }