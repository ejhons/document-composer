from dataclasses import dataclass, field
from email.policy import default

from dcp_engine.assembly.atomizer import MarkdownAtomizer
from dcp_engine.compilation.adapters.registry import AdapterRegistry
from dcp_engine.compilation.compilers.registry import CompilerRegistry
from dcp_engine.language.directives.registry import DirectiveRegistry
from dcp_engine.solving.inspection.pipeline import InspectionPipeline
from dcp_engine.solving.inspection.registry import StaticInspectorRegistry
from dcp_engine.language.parser import MarkdownParser

from dcp_engine.solving.resolution.dependency_resolver import DependencyResolver
from dcp_engine.solving.resolution.resolution_collector import PendingCollector
from dcp_engine.solving.resolution.runtime_resolver import RuntimeResolver
from dcp_engine.planning.loaders.base import ResourceResolver
from dcp_engine.planning.loaders.resource_resolver import LocalResourceResolver

@dataclass
class EngineContext:
    resource_resolver: ResourceResolver 
    markdown_parser: MarkdownParser = field(default_factory = MarkdownParser)

    inspector_registry: StaticInspectorRegistry = field(default_factory=StaticInspectorRegistry)
    directive_registry: DirectiveRegistry = field(default_factory=DirectiveRegistry)
    adapter_registry: AdapterRegistry = field(default_factory=AdapterRegistry)
    compiler_registry: CompilerRegistry = field(default_factory=CompilerRegistry)

    runtime_resolver: RuntimeResolver = field(default_factory=RuntimeResolver)
    dependency_resolver: DependencyResolver = field(default_factory=DependencyResolver)
    pending_collector: PendingCollector = field(default_factory=PendingCollector)

    inspection_pipeline: InspectionPipeline = field(default_factory=InspectionPipeline)

    atomizer: MarkdownAtomizer = field(default_factory=MarkdownAtomizer)