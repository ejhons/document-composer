from dcp_api.api.mappers.iteration import IterationMapper
from dcp_api.api.schemas.iteraction import PendingResolutionResponse, SessionIterationListResponse, SessionIterationResponse
from dcp_api.domain.session import Session
from fastapi import APIRouter, Depends

from dcp_api.api.dependencies import get_iteration_service
from dcp_api.application.iteraction import IterationService
from dcp_api.api.schemas.iteraction import (
    ResolveIterationResponse,
    ResolveIterationRequest,
    StartIterationRequest,
)


router = APIRouter(
    prefix="/projects/{project_id}/iteration",
    tags=["iteration"]
)
mapper = IterationMapper()


@router.get(
    "",
    response_model=SessionIterationListResponse,
)
def list_iteractions(
    project_id: str,
    service: IterationService = Depends(
        get_iteration_service
    ),
):
    sessions = service.list(
        project_id=project_id
    )
    return mapper.to_session_iteration_list_response(
        sessions=sessions
    )


@router.post(
    "",
    response_model=SessionIterationResponse,
)
def start_iteration(
    project_id: str,
    request: StartIterationRequest,
    service: IterationService = Depends(
        get_iteration_service
    ),
):

    session = service.start(
        project_id=project_id,
        variables=request.variables,
    )

    return mapper.to_session_iteration_response(session)


@router.delete("")
def clear_iteraction(
    project_id: str,
    service: IterationService = Depends(
        get_iteration_service
    ),
):

    service.close_all(
        project_id=project_id,
    )

    return {
        "status":"cleared"
    }


@router.get(
    "/{session_id}",
    response_model=SessionIterationResponse,
)
def get_iteration(
    project_id: str,
    session_id: str,
    service: IterationService = Depends(
        get_iteration_service
    ),
):

    session = service.get(
        project_id=project_id,
        session_id=session_id,
    )

    return mapper.to_session_iteration_response(session)


@router.delete("/{session_id}/close")
def close_iteration(
    project_id: str,
    session_id: str,
    service: IterationService = Depends(
        get_iteration_service
    ),
):
    service.close(
        project_id=project_id,
        session_id=session_id
    )
    return {
        "status":"closed"
    }



@router.post(
    "/{session_id}/resolve",
    response_model=ResolveIterationResponse,
)
def resolve_iteration(
    project_id: str,
    session_id: str,
    request: ResolveIterationRequest,
    service: IterationService = Depends(
        get_iteration_service
    ),
):

    result = service.resolve(
        project_id=project_id,
        session_id=session_id,
        values=request.values,
    )
    session = service.get(
        project_id=project_id,
        session_id=session_id
    )

    return mapper.to_resolve_iteration_response(
        session=session,
        result=result
        )



@router.get("/{session_id}/variables")
def get_variables(
    project_id: str,
    session_id: str,
    service: IterationService = Depends(
        get_iteration_service
    ),
):
    session = service.get(
        project_id=project_id,
        session_id=session_id
    )
    return session.execution_session.context.inputs



# def to_response(session) -> ResolveIterationResponse:

#     return ResolveIterationResponse(
#         session_id=session.id,
#         status=result.solved,
#         pending=[
#             PendingResolutionResponse(
#                 p
#                 # id=item.id,
#                 # kind=item.kind,
#                 # name=item.name,
#                 # description=item.description,
#                 # required=item.required,
#                 # metadata=item.metadata,
#             )
#             for item in result.pending.values() for p in item.inputs
#         ],
#         ready=not result.execution_session.pending,
#     )