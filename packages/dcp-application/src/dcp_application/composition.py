from dcp_application.use_cases.build_document import BuildDocument
from dcp_engine.runtime.builder import EngineBuilder


def create_build_document(interaction) -> BuildDocument:
    engine = EngineBuilder.default().build()

    return BuildDocument(
        engine=engine,
        interaction=interaction,
    )