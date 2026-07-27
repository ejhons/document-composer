def create_engine():

    planning = PlanningModule(
        resource_resolver=LocalResourceResolver(),
        directive_registry=DirectiveRegistry(),
        inspector_registry=StaticInspectorRegistry(),
        inspection_pipeline=InspectionPipeline()
    )

    runtime = RuntimeModule(
        runtime_resolver=RuntimeResolver(),
        dependency_resolver=DependencyResolver(
            markdown_parser=MarkdownParser(
                expression_parser=ExpressionParser()
            )
        ),
        pending_collector=PendingCollector()
    )

    compilation = CompilationModule(
        adapter_registry=AdapterRegistry.default(),
        compiler_registry=CompilerRegistry.default()
    )

    return Engine(
        planning=planning,
        runtime=runtime,
        compilation=compilation
    )