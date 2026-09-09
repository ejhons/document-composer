from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from dcp_api.domain.session import Session

from dcp_engine import Engine
from dcp_engine.runtime.engine import IteractionResult



class ExecutionSessionRepository(ABC):

    @abstractmethod
    def save(self, session) -> None:
        ...

    @abstractmethod
    def get(
        self,
        *,
        project_id: str,
        session_id: str,
    ):
        ...

class IterationService:
    def __init__(
        self,
        *,
        engine: Engine,
        execution_sessions, #ExecutionSessionsRepository
        project_repository,
    ):
        self._engine: Engine = engine
        self._sessions = execution_sessions
        self._projects = project_repository


    def start(
        self,
        *,
        project_id: str,
        variables: dict[str, Any] | None = None,
    ) -> Session:
        '''
        Creates ExecutionSession and saves it in Repository.
        '''
        project = self._projects.get(project_id)
        execution_session = self._engine.create_session(
            workspace=project.path,
        )
        self._engine.reload_manifest(execution_session)
        
        execution_session.context.update(variables)

        session = Session(
            project_id=project_id,
            execution_session = execution_session
        )


        self._sessions.save(session)

        return session


    def close_all(
        self,
        *,
        project_id: str,
    ) -> dict[str, str]:
        '''
        Creates ExecutionSession and saves it in Repository.
        '''
        self._sessions.close_all(
            project_id=project_id
        )
        return {
            "status":"cleared"
        }
    

    def get(
        self,
        *,
        project_id: str,
        session_id: str,
    ) -> Session:
        '''
        Gets session saved in repository.
        '''
        return self._sessions.get(
            project_id=project_id,
            session_id=session_id,
        )


    def list(
        self,
        *,
        project_id: str
    ) -> list[Session]:
        '''
        Gets session saved in repository.
        '''
        return self._sessions.list(
            project_id=project_id,
        )

    
    def close(
        self,
        *,
        project_id: str,
        session_id: str,
    ) -> Session:
        '''
        Gets session saved in repository.
        '''
        return self._sessions.close(
            project_id=project_id,
            session_id=session_id,
        )
    
    def resolve(
        self,
        *,
        project_id: str,
        session_id: str,
        values: dict[str, Any],
    ) -> IteractionResult:
        self._projects.get(project_id)

        session = self._sessions.get(
            project_id=project_id,
            session_id=session_id,
        )

        result = self._engine.create_interaction(session.execution_session)

        if values:
            session.execution_session.context.update(values)
            result = self._engine.create_interaction(session.execution_session)

        session.execution_session = result.session

        self._sessions.save(session)

        return result


# class DocumentIterationPort(ABC):
#     @abstractmethod
#     def iterate(
#         self,
#         *,
#         project_id: str,
#         variables: dict[str, Any],
#     ):
#         ...


# class EngineIterationAdapter(DocumentIterationPort):
#     def __init__(self, engine):
#         self._engine = engine

#     def iterate(
#         self,
#         *,
#         project_id: str,
#         variables: dict,
#     ):
#         # Aqui conectamos às APIs REAIS da
#         # versão atual da DocumentEngine.

#         return self._engine.iterate(
#             project_id=project_id,
#             variables=variables,
#         )


# class IterationRepository(ABC):
#     @abstractmethod
#     def create(
#         self,
#         project_id: str,
#     ) -> IterationSession:
#         ...

#     @abstractmethod
#     def get(
#         self,
#         project_id: str,
#         session_id: str,
#     ) -> IterationSession:
#         ...

#     @abstractmethod
#     def save(
#         self,
#         session: IterationSession,
#     ) -> None:
#         ...

#     @abstractmethod
#     def delete(
#         self,
#         project_id: str,
#         session_id: str,
#     ) -> None:
#         ...
    
# class IterationService:
#     def __init__(
#         self,
#         *,
#         repository: IterationRepository,
#         engine,
#         recipe_repository,
#     ):
#         self._repository = repository
#         self._engine = engine
#         self._recipe_repository = recipe_repository


#     def start(
#         self,
#         project_id: str,
#         variables: dict,
#     ) -> IterationSession:
#         session = self._repository.create(project_id)
#         session.update_variables(variables)

#         self._iterate(session)

#         self._repository.save(session)

#         return session

#     def resolve(
#         self,
#         project_id: str,
#         session_id: str,
#         values: dict,
#     ) -> IterationSession:

#         session = (
#             self._repository.get(
#                 project_id,
#                 session_id,
#             )
#         )

#         if (
#             session.status
#             == IterationStatus.COMPLETED
#         ):
#             return session

#         session.update_variables(
#             values
#         )

#         self._iterate(session)

#         self._repository.save(
#             session
#         )

#         return session

#     def get(
#         self,
#         project_id: str,
#         session_id: str,
#     ) -> IterationSession:

#         return self._repository.get(
#             project_id,
#             session_id,
#         )

#     def _iterate(
#         self,
#         session: IterationSession,
#     ) -> None:

#         recipe = self._recipe_repository.get(session.project_id)
#         result = self._inspect_and_resolve(
#             recipe=recipe,
#             variables=session.variables
#         )

#         session.update_pending(
#             self._to_pending_resolutions(result)
#         )

#     def _inspect_and_resolve(
#         self,
#         *,
#         recipe,
#         variables,
#     ):
#         """
#         Adaptador para a API da Engine.

#         A implementação exata deve ser conectada
#         às interfaces atuais da DocumentEngine.
#         """

#         return self._engine.inspect(
#             recipe=recipe,
#             variables=variables,
#         )

#     def _to_pending_resolutions(
#         self,
#         result,
#     ) -> list[PendingResolution]:

#         pending = []

#         for item in result.pending_variables:

#             pending.append(
#                 PendingResolution(
#                     id=f"variable:{item}",
#                     kind=ResolutionKind.VARIABLE,
#                     name=item,
#                 )
#             )

#         for item in result.pending_dependencies:

#             pending.append(
#                 PendingResolution(
#                     id=f"dependency:{item}",
#                     kind=ResolutionKind.DEPENDENCY,
#                     name=item,
#                 )
#             )

#         return pending