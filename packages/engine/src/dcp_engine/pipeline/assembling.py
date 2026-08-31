from __future__ import annotations

from dcp_engine.common.exceptions import GraphNotSolvedException
from dcp_engine.language.syntax.markdown.atom import MarkdownDirective
from dcp_engine.language.syntax.markdown.atomized_markdown import AtomizedMarkdown
from dcp_engine.planning.graph.component_node import ComponentNode
from dcp_engine.runtime.context import EngineContext
from dcp_engine.runtime.execution.session import ExecutionSession



class AssemblingModule:

    def __init__(self, context: EngineContext):
        self.atomizer = context.atomizer

    def execute(self, session: ExecutionSession):
        graph = session.graph

        if not graph.solved:
            raise GraphNotSolvedException("Can't assemble while documents has pendencies.")

        roots = graph.roots
        cache: dict[str, AtomizedMarkdown] = {}
        document = AtomizedMarkdown()

        for node in roots:
            assembled = self._assemble_node(
                graph=graph,
                node=node,
                cache=cache,
            )
            document.blocks.extend(assembled.blocks)

        # Lista encadeada de documentos
        session.fragmented_markdown = document

        return session


    def _assemble_node(
        self,
        graph,
        node: ComponentNode,
        cache: dict[str, AtomizedMarkdown],
    ) -> AtomizedMarkdown:

        if node.id in cache:
            return cache[node.id]

        parsed: AtomizedMarkdown = self.atomizer.atomize(node.adapted.markdown)

        assembled = AtomizedMarkdown()

        dependencies = {
            dep.origin: dep
            for dep in graph.get_dependency(node.id)
        }

        for block in parsed.blocks:

            if not isinstance(block, MarkdownDirective):
                assembled.blocks.append(block)
                continue

            dependency = dependencies.get(
                str(block.directive.index)
            )

            if dependency is None:
                continue

            child = graph.get_node(dependency.target_id)

            child_markdown = self._assemble_node(
                graph=graph,
                node=child,
                cache=cache,
            )

            assembled.blocks.extend(
                child_markdown.blocks
            )

        cache[node.id] = assembled

        return assembled


# from yaml import Node

# from engine.common.exceptions import GraphNotSolvedException
# from engine.frontend.syntax.markdown.atom import MarkdownDirective, MarkdownPlaceholder
# from engine.frontend.syntax.markdown.atomized_markdown import AtomizedMarkdown
# from engine.frontend.syntax.markdown.atomizer import MarkdownAtomizer
# from engine.planner.graph.component_node import ComponentNode
# from engine.runtime.context import EngineContext
# from engine.runtime.execution.session import ExecutionSession


# class AssemblingModule:
#     def __init__(
#             self,
#             context: EngineContext
#             # atomizer: MarkdownAtomizer
#     ):
#         self.atomizer = context.atomizer

#     def execute(
#         self,
#         session: ExecutionSession            
#     ) -> ExecutionSession:     
#         '''
#         Create FragmentedMarkdown
#         '''
#         graph = session.graph
#         if not graph.solved:
#             raise GraphNotSolvedException(f"Can't fragment unsolved Graph")
        
#         # Initializate map of fragments relation Node in graph to its Fragmented Markdown equivalent.
#         node_fragment = {
#             node:self.atomizer.atomize(node.adapted.markdown)
#             for node in graph.nodes.values()
#         }
#         # Runs through every node creating equivalent node correspondence to Markdown
#         for node, parsed in node_fragment.items():
#             for i, block in enumerate(parsed.blocks):
#                 if not isinstance(block, MarkdownDirective):
#                     continue

#                 node_id = node.id
#                 dependencies = graph.get_dependency(node_id)

#                 index:int = block.directive.index
#                 dependency = [dep for dep in dependencies if (dep.origin == str(index))][0]

#                 parsed.blocks[i] = MarkdownPlaceholder(
#                     node_id=dependency.target_id
#                 )
#         return session#node_fragment.values
    
#     def _solve_directives(
#             self,
#             graph,
#             node: ComponentNode,
#             parsed: AtomizedMarkdown,
#     ) -> None:
#         for i, block in enumerate(parsed.blocks):
#             # Solve only directives because its capability of creating references
#             if not isinstance(block, MarkdownDirective):
#                 continue

#             node_id = node.id
#             dependencies = graph.get_dependency(node_id)


#             index:int = block.directive.index
#             # List of nodes dependents to node_id
#             dependency = [dep for dep in dependencies if (dep.origin == str(index))][0]
#             # Replace framented node generated above for a placeholder for further compiling.
#             parsed.blocks[i] = MarkdownPlaceholder(
#                 node_id=dependency.target_id
#             )