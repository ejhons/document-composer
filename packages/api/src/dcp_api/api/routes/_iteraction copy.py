from fastapi import APIRouter, Depends

from dcp_api.api.schemas.iteraction import (
    StartIteractionRequest,
    ResolveIteractionRequest,
    ResolveIteractionResponse,
)

router = APIRouter(
    prefix="/api/projects/{project_id}/iteractions",
    tags=["iteractions"],
)


@router.post(
    "",
    response_model=ResolveIteractionResponse,
)
def start_iteraction(
    project_id: str,
    request: StartIteractionRequest,
    service = Depends(get_iteraction_service),
):

    session = service.start(
        project_id=project_id,
        variables=request.variables,
    )

    return to_response(session)

@router.get(
    "/{session_id}",
    response_model=ResolveIteractionResponse,
)
def get_iteraction(
    project_id: str,
    session_id: str,
    service = Depends(get_iteraction_service),
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
    response_model=ResolveIteractionResponse,
)
def resolve_iteraction(
    project_id: str,
    session_id: str,
    request: ResolveIteractionRequest,
    service = Depends(get_iteraction_service),
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

    return ResolveIteractionResponse(
        session_id=session.id,
        project_id=session.project_id,
        status=session.status,
        variables=session.variables,
        pending=session.pending,
        ready=session.is_ready(),
    )