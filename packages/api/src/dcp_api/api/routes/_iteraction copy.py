from fastapi import APIRouter, Depends

from dcp_api.api.schemas.iteraction import (
    StartIterationRequest,
    ResolveIterationRequest,
    ResolveIterationResponse,
)

router = APIRouter(
    prefix="/api/projects/{project_id}/iterations",
    tags=["iterations"],
)


@router.post(
    "",
    response_model=ResolveIterationResponse,
)
def start_iteration(
    project_id: str,
    request: StartIterationRequest,
    service = Depends(get_iteration_service),
):

    session = service.start(
        project_id=project_id,
        variables=request.variables,
    )

    return to_response(session)

@router.get(
    "/{session_id}",
    response_model=ResolveIterationResponse,
)
def get_iteration(
    project_id: str,
    session_id: str,
    service = Depends(get_iteration_service),
):
    '''
    Consulta o estado.
    '''

    session = service.get(
        project_id,
        session_id,
    )

    return to_response(session)


@router.post(
    "/{session_id}/resolve",
    response_model=ResolveIterationResponse,
)
def resolve_iteration(
    project_id: str,
    session_id: str,
    request: ResolveIterationRequest,
    service = Depends(get_iteration_service),
):
    '''
    Resolve uma iteração
    '''

    session = service.resolve(
        project_id=project_id,
        session_id=session_id,
        values=request.values,
    )

    return to_response(session)

def to_response(session):

    return ResolveIterationResponse(
        session_id=session.id,
        project_id=session.project_id,
        status=session.status,
        variables=session.variables,
        pending=session.pending,
        ready=session.is_ready(),
    )