from engine.common.models.inspection import InspectionResult
from engine.planner.planning_context import PlanningContext


class InspectionPipeline:

    def execute(
        self,
        graph,
        planning_context: PlanningContext,
    ) -> dict[str, bool]:
        inspected = {}
        for node in graph.nodes.values():
            # Até então, o único inspector resgistrado é o de Markdown.
            inspector = planning_context.inspector_registry.get(node.component.file_format)

            if inspector is None:
                continue

            #Realiza a inspeção
            inspection:InspectionResult = inspector.inspect(node.component)
            # node.variables = inspection.variables
            node.inspection = inspection
            inspected[node.id] = True

        return inspected