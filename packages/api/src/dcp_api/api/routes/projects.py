# @router.post("/projects")
# def create_project(
#     request: CreateProjectRequest,
#     service: ProjectService = Depends(get_project_service),
# ):
#     return service.create_project(request.name)

# @router.get("/projects")
# def list_projects(
#     service: ProjectService = Depends(get_project_service),
# ):
#     return service.list_projects()
from fastapi import APIRouter, Depends

from dcp_api.api.dependencies import get_project_service
from dcp_api.api.schemas.project import (
    CreateProjectRequest,
    ProjectResponse,
)
from dcp_api.application.projects import ProjectService


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
)
def create_project(
    request: CreateProjectRequest,
    service: ProjectService = Depends(
        get_project_service
    ),
):
    project = service.create_project(
        request.name
    )

    return ProjectResponse(
        id=project.id,
        name=project.name,
    )


@router.get(
    "",
    response_model=list[ProjectResponse],
)
def list_projects(
    service: ProjectService = Depends(
        get_project_service
    ),
):
    projects = service.list_projects()

    return [
        ProjectResponse(
            id=project.id,
            name=project.name,
        )
        for project in projects
    ]


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: str,
    service: ProjectService = Depends(
        get_project_service
    ),
):
    project = service.get_project(project_id)

    return ProjectResponse(
        id=project.id,
        name=project.name,
    )


@router.delete(
    "/{project_id}",
    status_code=204,
)
def delete_project(
    project_id: str,
    service: ProjectService = Depends(
        get_project_service
    ),
):
    service.delete_project(project_id)