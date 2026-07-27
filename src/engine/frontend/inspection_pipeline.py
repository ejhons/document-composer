from engine.frontend.inspectors.registry import StaticInspectorRegistry

class InspectionPipeline:
    def execute(
        self,
        graph,
        # planning_context: PlanningContext,
        inspector_registry: StaticInspectorRegistry
    ):# -> dict[str, bool]:
        # inspected = {}
        for node in graph.nodes.values():
            # Até então, o único inspector resgistrado é o de Markdown.
            inspector = inspector_registry.get(
                node.component.file_format
            )
            if inspector is None:
                continue
            
            node.inspection = inspector.inspect(node.component)

            # #Realiza a inspeção
            # inspection:InspectionResult = inspector.inspect(node.component)
            # # node.variables = inspection.variables
            # node.inspection = inspection
            # inspected[node.id] = True

        # return inspected