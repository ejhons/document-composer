A overview of execution pipeline is:

```Python
recipe = recipe_resolver.resolve()
scheduler.load(recipe)
while scheduler.has_tasks():
    task = scheduler.next()
    component = repository.load(task)
    adapter = adapter_registry.resolve(component)
    fragment = adapter.render(component)
    assembler.store(task.id, fragment)
markdown = assembler.build()
compiler.compile(markdown)
```
