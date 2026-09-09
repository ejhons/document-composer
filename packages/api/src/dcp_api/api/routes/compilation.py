from dcp_api.api.dependencies import get_compilation_service
from dcp_api.api.mappers.files import FilesMapper
from dcp_api.api.schemas.compilation import CompilationResponse, CompileRequest
from dcp_api.api.schemas.files import PathResponse
from dcp_api.application.compilation import CompilationService
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse


router = APIRouter(
    prefix="/projects/{project_id}",
    tags=["compilation"],
)
mapper = FilesMapper()

@router.post(
    "/compile/{session_id}",
    response_model=CompilationResponse,
)
def compile_project(
    project_id: str,
    session_id: str,
    request: CompileRequest,
    service: CompilationService = Depends(
        get_compilation_service
    ),
):
    result = service.compile(
        project_id=project_id,
        session_id=session_id,
        target_format=request.target_format
    )

    return CompilationResponse(
        project_id=result.project_id,
        target_format=result.target_format,
        artifact=result.output_path.name,
    )


@router.get(
    "/artifacts/{filename}",
    response_model=PathResponse,
)
def download_artifact(
    project_id: str,
    filename: str,
    service: CompilationService = Depends(
        get_compilation_service
    ),
):
    
    path = service.get_artifact(
        project_id,
        filename,
    )
     # 1. Verifique se o arquivo realmente existe no servidor
    if not os.path.exists(CAMINHO_DO_ARQUIVO):
        return {"erro": "Arquivo não encontrado"}

    # 2. Retorne o FileResponse para iniciar o download
    return FileResponse(
        path=CAMINHO_DO_ARQUIVO, 
        filename="meu_relatorio_final.pdf", 
        media_type="application/pdf"
    )
