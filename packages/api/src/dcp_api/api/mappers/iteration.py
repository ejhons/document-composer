from dcp_api.api.schemas.iteraction import PendingResolutionResponse, ResolveIteractionResponse, SessionIteractionListResponse, SessionIteractionResponse
from dcp_api.domain.session import Session

from dcp_engine.language.syntax.fields import InputDefinition
from dcp_engine.runtime.engine import IteractionResult
from dcp_engine.solving.resolution.resolution_collector import PendingItem


class IteractionMapper:
    def to_session_iteraction_response(self, session: Session) -> SessionIteractionResponse:
        return SessionIteractionResponse(
            project_id=session.project_id,
            session_id=session.id,
            variables=session.execution_session.context.inputs
        )

    
    def to_session_iteraction_list_response(self, sessions: list[Session]) -> SessionIteractionResponse:
        return SessionIteractionListResponse(
            sessions=[
                self.to_session_iteraction_response(session)
                for session in sessions
            ]
        )
    
    def to_resolve_iteraction_response(
            self,
            session: Session,
            result: IteractionResult
        ) -> ResolveIteractionResponse:

        # session.execution_session
        if result.pending is None or result.pending.unique_pending_variables is None:
            return ResolveIteractionResponse(
                project_id=session.project_id,
                session_id=session.id,
                status=result.status
            )

        variables = []
        for id in set(result.pending.unique_pending_variables):
            item_definition = result.pending.input_definitions.get(id)
            if item_definition is not None:
                item = self._pending_item_to_response(item_definition)
                variables.append(item)


        return ResolveIteractionResponse(
            project_id=session.project_id,
            session_id=session.id,
            # variables=variables,#session.execution_session.context.inputs,
            status=result.status, #== 'ready'
            pending=variables
        )

    def _pending_item_to_response(self, item:InputDefinition) -> PendingResolutionResponse:
        # print(item)
        return PendingResolutionResponse(
            id=item.name,
            name=item.label or item.name,
            type=item.type,
            description=item.description,
            default=item.default,
            # metadata={
            #     "references": item.references
            # }
        )
        
