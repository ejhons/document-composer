## 1 - How to compile a recipe?

```Python
# Defines workspace local
root = './workspace/project/'
# Define workspace
workspace = Workspace(root)
# Reads recipe manifest
loader = ManifestLoader('./workspace/project/recipe.json')
recipe: RecipeManifest = loader.load_manifest()
# Receives ExecutionContext
context = get_context()
# Create a builder
# Call default() method for using default scenario
builder: EngineBuilder = Builder.default()
# Builds engine by calling build() method
engine: Engine = builder.build()
# Create a session
session: Session = engine.create_section(
  workspace=workspace,
  mainfest=recipe,
  context=context
)
# Defines output path
output_path = workspace.default_output()
# Compilation
result = engine.compile(
  session,
  output_path = workspace.path_from_output(
    'document.md',
    exists_ok = True
  )
)
```

## 2 - How it should be done

```Python
# Defines workspace local
root = './workspace/project/'
# Define workspace
workspace = Workspace(root)

# Reads recipe manifest
loader = ManifestLoader(
  workspace.recipe_path('manifest.json')
)#'./workspace/project/recipe.json')
recipe: RecipeManifest = loader.load_manifest()
# Receives ExecutionContext
context = get_context()
# Create a builder
# Call default() method for using default scenario
builder: EngineBuilder = Builder.default()
# Builds engine by calling build() method
engine: Engine = builder.build()
# Create a session
session: Session = engine.create_section(
  workspace=workspace,
  mainfest=recipe,
  context=context
)
# Defines output path
output_path = workspace.default_output()

# Create interaction
iteraction_result = engine.create_iteraction(session)

#Repeats iteraction until it is solved
...

# Once solved, goes to Compilation
result = engine.compile(
  session,
  output_path = workspace.path_from_output(
    'document.md',
    exists_ok = True
  )
)
```

```bash
dcp init
dcp start --workspace test
dcp load --manifest
dcp context "context.json"
dcp start -i
dcp compile
```