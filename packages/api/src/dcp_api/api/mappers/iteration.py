from dcp_api.api.schemas.iteraction import PendingResolutionResponse, ResolveIterationResponse, SessionIterationListResponse, SessionIterationResponse
from dcp_api.domain.session import Session

from dcp_engine.language.syntax.fields import InputDefinition
from dcp_engine.runtime.engine import IteractionResult
from dcp_engine.solving.resolution.resolution_collector import PendingItem


class IterationMapper:
    def to_session_iteration_response(self, session: Session) -> SessionIterationResponse:
        return SessionIterationResponse(
            project_id=session.project_id,
            session_id=session.id,
            variables=session.execution_session.context.inputs
        )

    
    def to_session_iteration_list_response(self, sessions: list[Session]) -> SessionIterationResponse:
        return SessionIterationListResponse(
            sessions=[
                self.to_session_iteration_response(session)
                for session in sessions
            ]
        )
    
    def to_resolve_iteration_response(
            self,
            session: Session,
            result: IteractionResult
        ) -> ResolveIterationResponse:

        # session.execution_session
        if result.pending is None or result.pending.pending_inputs is None:
            return ResolveIterationResponse(
                project_id=session.project_id,
                session_id=session.id,
                status=result.solved
            )

        variables = []
        for id in set(result.pending.pending_inputs):
            item_definition = result.pending.input_definitions.get(id)
            if item_definition is not None:
                item = self._pending_item_to_response(item_definition)
                variables.append(item)


        return ResolveIterationResponse(
            project_id=session.project_id,
            session_id=session.id,
            # variables=variables,#session.execution_session.context.inputs,
            status=result.solved, #== 'ready'
            pending=variables
        )

    def _pending_item_to_response(self, item:InputDefinition) -> PendingResolutionResponse:
        print(item)
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
        
