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
# Create a builder
# Call default() method for using default scenario
builder: EngineBuilder = Builder.default()
# Builds engine by calling build() method
engine: Engine = builder.build()
```

## 2 - How it should be done

```Python
# Create a builder
# Call default() method for using default scenario
builder: EngineBuilder = Builder.default()
# Builds engine by calling build() method
engine: Engine = builder.build()

# Defines workspace local
root = './workspace/project/'
# Define workspace
workspace = engine.init_workspace(Path(root))
# Creates session
session = engine.create_session(workspace)

# Iteration proccess
context = session.update_context(user_values)
# Create interaction
iteraction_result = engine.create_iteraction(session)

# Defines output path
output_path = workspace.default_output()

#Repeats iteraction until it is solved
...

# Once solved, goes to Compilation
result = engine.compile(
  session,
  target_format='default'
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

```
# Reads recipe manifest
loader = ManifestLoader(
  workspace.recipe_path('manifest.json')
)#'./workspace/project/recipe.json')
recipe: RecipeManifest = loader.load_manifest()
# Receives ExecutionContext
context = get_context()
# Create a session
session: Session = engine.create_section(
  workspace=workspace,
  mainfest=recipe,
  context=context
)

# Once solved, goes to Compilation
result = engine.compile(
  session,
  target_format='default'
  output_path = workspace.path_from_output(
    'document.md',
    exists_ok = True
  )
)
```
