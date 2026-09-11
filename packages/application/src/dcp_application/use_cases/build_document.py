from typing import Any

from dcp_application.ports import InteractionPort



class BuildDocument:
    def __init__(
        self,
        engine,
        interaction: InteractionPort
    ):
        self.engine = engine
        self.interaction = interaction

    def start(self, root):#-> ExecutionSession
        workspace = self.engine.init_workspace(root)
        session = self.engine.create_session(workspace)

        self.engine.reload_manifest(session)
        # self.engine.reload_metadata(session)

        return session

    def interact(self, session, values: dict[str, Any]):# -> IterationResult
        session.context.update(values)

        return self.engine.create_interaction(session)

    def compile(self, session, target_format="default"):# -> CompilingResult
        return self.engine.compile(
            session,
            target_format=target_format,
        )