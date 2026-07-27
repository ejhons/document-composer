from yaml import Node

from engine.common.exceptions import GraphNotSolvedException
from engine.frontend.syntax.markdown.atom import MarkdownDirective, MarkdownPlaceholder
from engine.frontend.syntax.markdown.atomized_markdown import AtomizedMarkdown
from engine.frontend.syntax.markdown.atomizer import MarkdownAtomizer
from engine.planner.graph.component_node import ComponentNode
from engine.runtime.context import EngineContext
from engine.runtime.execution.session import ExecutionSession


class AssemblingModule:
    def __init__(
            self,
            context: EngineContext
            # atomizer: MarkdownAtomizer
    ):
        self.atomizer = context.atomizer

    def execute(
        self,
        session: ExecutionSession            
    ) -> ExecutionSession:     
        '''
        Create FragmentedMarkdown
        '''
        graph = session.graph
        if not graph.solved:
            raise GraphNotSolvedException(f"Can't fragment unsolved Graph")
        
        # Initializate map of fragments relation Node in graph to its Fragmented Markdown equivalent.
        node_fragment = {
            node:self.atomizer.atomize(node.adapted.markdown)
            for node in graph.nodes.values()
        }
        # Runs through every node creating equivalent node correspondence to Markdown
        for node, parsed in node_fragment.items():
            for i, block in enumerate(parsed.blocks):
                if not isinstance(block, MarkdownDirective):
                    continue

                node_id = node.id
                dependencies = graph.get_dependency(node_id)

                index:int = block.directive.index
                dependency = [dep for dep in dependencies if (dep.origin == str(index))][0]

                parsed.blocks[i] = MarkdownPlaceholder(
                    node_id=dependency.target_id
                )
        return session#node_fragment.values

    def _solve_directives(
            self,
            graph,
            node: ComponentNode,
            parsed: AtomizedMarkdown,
    ) -> None:
        for i, block in enumerate(parsed.blocks):
            # Solve only directives because its capability of creating references
            if not isinstance(block, MarkdownDirective):
                continue

            node_id = node.id
            dependencies = graph.get_dependency(node_id)


            index:int = block.directive.index
            # List of nodes dependents to node_id
            dependency = [dep for dep in dependencies if (dep.origin == str(index))][0]
            # Replace framented node generated above for a placeholder for further compiling.
            parsed.blocks[i] = MarkdownPlaceholder(
                node_id=dependency.target_id
            )