from typing import Any

from dcp_application.ports import InteractionPort
from dcp_cli.interaction.terminal import TerminalInteraction
from dcp_engine.solving.resolution.resolution_collector import PendingResolution

def resolve_pending(
    pending: PendingResolution,
    iteraction_port: InteractionPort | None = None
) -> dict[str, Any]:
    '''
    Resolves project variables, asking the answer to user.
    '''
    iteraction_port = iteraction_port or TerminalInteraction.default()
    return iteraction_port.resolve(pending)



# def main():
#     # Create a builder
#     # Call default() method for using default scenario
#     builder: EngineBuilder = Builder.default()
#     # Builds engine by calling build() method
#     engine: Engine = builder.build()

#     # Defines workspace local
#     root = './workspace/project/'
#     # Define workspace
#     workspace = engine.init_workspace(Path(root))
#     # Creates session
#     session = engine.create_session(workspace)

#     # Iteraction proccess
#     context = session.update_context(user_values)
#     # Create interaction
#     iteraction_result = engine.create_iteraction(session)

#     # Defines output path
#     output_path = workspace.default_output()

#     #Repeats iteraction until it is solved
#     ...

#     # Once solved, goes to Compilation
#     result = engine.compile(
#     session,
#     target_format='default'
#     )