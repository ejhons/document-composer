from dcp_api.api.mappers.iteraction import IteractionMapper
from dcp_api.api.schemas.iteraction import PendingResolutionResponse, SessionIteractionListResponse, SessionIteractionResponse
from dcp_api.domain.session import Session
from fastapi import APIRouter, Depends

from dcp_api.api.dependencies import get_iteraction_service
from dcp_api.application.iteraction import IteractionService
from dcp_api.api.schemas.iteraction import (
    ResolveIteractionResponse,
    ResolveIteractionRequest,
    StartIteractionRequest,
)


router = APIRouter(
    prefix="/projects/{project_id}/iteraction",
    tags=["iteraction"]
)
mapper = IteractionMapper()


@router.get(
    "",
    response_model=SessionIteractionListResponse,
)
def list_iteractions(
    project_id: str,
    service: IteractionService = Depends(
        get_iteraction_service
    ),
):
    sessions = service.list(
        project_id=project_id
    )
    return mapper.to_session_iteraction_list_response(
        sessions=sessions
    )


@router.post(
    "",
    response_model=SessionIteractionResponse,
)
def start_iteraction(
    project_id: str,
    request: StartIteractionRequest,
    service: IteractionService = Depends(
        get_iteraction_service
    ),
):

    session = service.start(
        project_id=project_id,
        variables=request.variables,
    )

    return mapper.to_session_iteraction_response(session)


@router.delete("")
def clear_iteraction(
    project_id: str,
    service: IteractionService = Depends(
        get_iteraction_service
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
    response_model=SessionIteractionResponse,
)
def get_iteraction(
    project_id: str,
    session_id: str,
    service: IteractionService = Depends(
        get_iteraction_service
    ),
):

    session = service.get(
        project_id=project_id,
        session_id=session_id,
    )

    return mapper.to_session_iteraction_response(session)


@router.delete("/{session_id}/close")
def close_iteraction(
    project_id: str,
    session_id: str,
    service: IteractionService = Depends(
        get_iteraction_service
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
    response_model=ResolveIteractionResponse,
)
def resolve_iteraction(
    project_id: str,
    session_id: str,
    request: ResolveIteractionRequest,
    service: IteractionService = Depends(
        get_iteraction_service
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

    return mapper.to_resolve_iteraction_response(
        session=session,
        result=result
        )



@router.get("/{session_id}/variables")
def get_variables(
    project_id: str,
    session_id: str,
    service: IteractionService = Depends(
        get_iteraction_service
    ),
):
    session = service.get(
        project_id=project_id,
        session_id=session_id
    )
    return session.execution_session.context.inputs



# def to_response(session) -> ResolveIteractionResponse:

#     return ResolveIteractionResponse(
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