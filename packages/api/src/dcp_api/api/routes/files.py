from fastapi import APIRouter, Depends, UploadFile

from dcp_api.api.dependencies import get_file_service
from dcp_api.application.files import FileService


router = APIRouter(
    prefix="/api/projects/{project_id}/files",
    tags=["files"],
)


@router.post("")
async def upload_file(
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

    return {
        "filename": path.name,
    }