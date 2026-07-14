from engine.backend.ir.block import ComponentIRBlock, IRBlock
from engine.backend.ir.document import DocumentIR
from engine.planner.graph.component_node import ComponentNode
from engine.planner.graph.graph import RecipeGraph
from engine.runtime.execution.execution_plan import ExecutionPlan

class DocumentIRBuilder:
    def build(
        self, 
        graph: RecipeGraph
    ) -> DocumentIR:
        
        # root = IRBlock(
        #     id='__root__',
        #     # node_id='',
        #     content=''
        # )
        document = DocumentIR.create()

        for root in graph.roots:
            self._append_subtree(
                document,
                graph,
                document.root.id,
                root#root
            )
            # block = self._build_subtree(graph, node)
            # document.append(
            #     parent_id=root.id,
            #     block=block
            # )

        return document

    def _append_subtree(
        self,
        document: DocumentIR,
        graph: RecipeGraph,
        parent_id: str,
        node: ComponentNode
    ):
        if not node.resolution.resolved:
            # message = f'node {node.id} not resolved.' + f' pending inputs: {list(node.resolution.pending_inputs)}. ' + f'. pending_dependencies: {list(node.resolution.pending_dependencies)}'  
            raise ValueError(f'node {node.id} not resolved.')
        
        block = ComponentIRBlock(
            # id=node.id,
            node_id=node.id,
            type = node.component.type,
            content=node.resolution.content,
            metadata=node.component.metadata,
        )

        document.append(
            parent_id,
            block
        )

        for child in graph.children(node.id):
            self._append_subtree(
                document,
                graph,
                block.id,
                child
            )

    # def _build_subtree(
    #     self,
    #     graph: RecipeGraph,
    #     node: ComponentNode
    # ) -> IRBlock:

    #     if not node.resolution.resolved:
    #         raise ValueError(
    #             f"Node '{node.id}' is not fully resolved."
    #         )

    #     block = IRBlock(
    #         # id=node.id,
    #         node_id=node.id,
    #         content=node.resolution.content,
    #         metadata=node.component.metadata,
    #     )

    #     for child in graph.children(node.id):
    #         block.append(
    #             self._build_subtree(graph, child)
    #         )

    #     return block

    # def build(
    #     self,
    #     graph: RecipeGraph,
    #     plan: ExecutionPlan
    # ) -> DocumentIR:
    #     root = IRBlock(
    #         id="document",
    #         node=None,
    #         content=""
    #     )
    #     ir_document = DocumentIR(root=root)
    #     block_index: dict[str, IRBlock] = {}
    #     # Cria um bloco para cada Step
    #     for step in plan.steps:
    #         node = step.node
    #         block = IRBlock(
    #             node_id=node.id,
    #             content=node.resolution.content,
    #             metadata=node.component.metadata
    #         )
    #         block_index[node.id] = block

    #     # Reconstrói a hierarquia
    #     for node in graph.roots:
    #         ir_document.append(
    #             paret_id=root.id, 
    #             block=block_index[node.id]
    #         )

    #     for edge in graph.edges:
    #         parent =  block_index[edge.source_id]
    #         child = block_index[edge.target_id]

    #         ir_document.append(
    #             parent_id=parent.id,
    #             block=child
    #         )

    #         # if parent_block is None:
    #         #     root.children.append(child_block)
    #         #     continue
            
    #         # parent = block_index[parent_block.node_id]
    #         # parent._children.append(child)

    #     # for step in plan.steps:
    #     #     block = block_index[step.node.id]
    #     #     parent_id = step.parent_id

    #     #     if parent_id is None:
    #     #         root.children.append(block)
    #     #         continue

    #     #     parent = block_index[parent_id]
    #         # parent.children.append(block)

    #     return ir_document#DocumentIR(root=root)