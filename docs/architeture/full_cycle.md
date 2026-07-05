1. Cria `ExecutionSession`
2. Workspace is defined
3. Manifest is defined by its localization -> `RecipeManifest` object is generated
4. `RecipeGraphBuilder` is called for transforming `RecipeManifest` in `RecipeGraph` only with declarated nodes in manifest.
5. `RuntimeGraphBuilder` uses `RecipeGraph` -> `ExecutionGraph`
---
while ExecutionGraph.executing:
    6. `InpectionPipeline` inspect `Graph`, generating `Parsedmarkdown` in each `node`
    7. `RuntimeResolver` solves variable values:
        - Verifies missing values in `ExecutionContext.inputs`
        - Creates a dictionary [variable, value]:
            - Missing variables are replaced by identified placeholder
            - Defined variables in context by their values
        - Replace variable values in markdown
        - Brings back missing variables that were replaced by placeholder
        - if node.variables is empty, mark node as parsed
        - if node.variables is not empty and neither of them are in context, mark node as parsed
        - else, mark node as dirty
        - returns ResolutionResult with a generated ParsedMarkdown
    8. `DependencyResolver` is called for resolving dependencies in `ExecutionGraph` using a `PlanningContext`.
        - `PlanningContext` groups registries for directives and inspectors.
        - `Inspectors `extract variables, directives and fields in file. (Only markdown files are inspecioned) -> `InspectionResult`
        - Each `directive`found has the ability of adding new nodes to graph. This analysis is made unitil we don't have any others pendent directives.
        - Takes: `inputs` and `InputDefinitions`
    9. `PendingCollector` is called again for verifying which new dependencies were changed/added to `ExecutionGraph` -> `PendingResolution`
end while if all nodes are completed

10. `RuntimeResolutionResult` is returned by Engine
---
11. Continues only if `RuntimeResolutionResult` is completed
12. `Scheduler` uses `ExecutionGraph`for creating an `ExecutionPlan`from topology of `RecipeGraph`
13. `ExecutionPlan` has a list of steps that will be run by `Engine`
14. Each `node` of `ExecutionGraph` is treated by `Adapter` generating `Intermediate Representation (IR)`
15. Those parts are stick together for generating one file in markdown: `AssembledMarkdown`
16. `Compiler`is called for treating each `node` in `ExecutionGraph` and `Engine`
