
# DocComposer Engine

The **DocComposer Engine** is the core document-processing library of the DocComposer project.

It is responsible for planning document execution, resolving dependencies, assembling components, and compiling the resulting document into the requested output format.

The Engine contains no CLI concerns and does not depend on the application's delivery mechanism.

---

## Responsibilities

The Engine is responsible for:

* loading and interpreting document recipes;
* managing workspaces;
* creating execution sessions;
* inspecting components;
* identifying dependencies;
* resolving runtime requirements;
* scheduling dependent tasks;
* assembling document content;
* compiling assembled documents;
* managing component adapters;
* managing compiler adapters.

It is **not** responsible for:

* terminal interaction;
* HTTP requests;
* frontend rendering;
* user-interface state;
* command-line argument parsing.

---

## Processing Pipeline

The Engine follows four explicit stages:

```text
Planning
   │
   ▼
Solving
   │
   ▼
Assembling
   │
   ▼
Compilation
```

Each stage has a specific purpose.

### 1. Planning

Planning determines what the document needs before runtime execution.

Static inspectors can identify:

```text
Template Variables
File Dependencies
Embedded Content
Special Blocks
```

This allows applications to determine what information must be provided before compilation.

The static inspection process is intentionally designed without executing the document itself.

---

### 2. Solving

Solving resolves the requirements identified during planning.

The solving process may finish immediately or return pending requirements.

This is intentional.

A document can require several rounds of interaction:

```text
Solve
 │
 ├── Missing input
 │
 ├── Provide value
 │
 ├── Re-evaluate
 │
 └── Continue
```

Applications should preserve the `ExecutionSession` between interactions.

---

### 3. Assembling

After all requirements have been resolved, the Engine assembles the document.

The scheduler manages dependencies using a LIFO execution stack.

For example:

```text
Document
 ├── Markdown
 │    └── Excel
 │         └── Mermaid
 └── Image
```

When Markdown discovers the Excel dependency, execution of Markdown can be suspended while the dependency is processed.

The scheduler then returns to the parent task once the dependency is available.

---

### 4. Compilation

Compilation converts the assembled document into the requested target format.

Supported formats currently include:

```text
HTML
PDF
DOCX
```

The compiler is selected through the compilation layer rather than by embedding format-specific conditions in the Engine.

---

## ExecutionSession

The `ExecutionSession` represents the state of a document-generation operation.

It provides the state required to continue processing across multiple solving interactions.

Conceptually:

```text
ExecutionSession
├── Workspace
├── Recipe / Manifest
├── Execution Context
└── Trace / Runtime State
```

A session should be treated as the unit of continuity for an interactive document-generation process.

---

## Workspace

The `Workspace` represents the physical project directory.

It provides access to project resources such as:

```text
workspace.root
workspace.recipe_path
workspace.metadata_path
workspace.components_path
workspace.output_path
```

The Workspace should remain concerned with project resources and their location.

Parsing and domain construction should be delegated to the corresponding domain models/loaders.

---

## Resources

Resources may be referenced using either relative or absolute paths.

### Internal resource

```text
components/report.md
```

The path is resolved relative to the workspace.

### External resource

```text
C:/shared/templates/report.md
```

or another absolute filesystem path.

The Engine should resolve both forms through a centralized resource-resolution mechanism rather than duplicating path logic across adapters.

---

## Component Adapters

Component adapters transform individual resources into representations usable by the assembly process.

Examples include adapters for:

* Markdown;
* Excel;
* images;
* Mermaid;
* other supported document components.

Adapters should not directly depend on other concrete adapters.

When one component needs another component, the Engine mediates the interaction through dependency resolution.

For example, the Markdown adapter can request external content through an injected resolver rather than importing and controlling the Excel adapter directly.

---

## Markdown Templates

Markdown components can contain Jinja expressions:

```jinja2
# {{ title }}

Prepared by {{ author }}.

{{ include_table("data.xlsx") }}
```

The static inspection stage identifies template variables and resource references.

The runtime stage resolves their values and dependencies.

---

## Static Inspection

Static inspection provides information about a component before execution.

The Markdown inspector can identify constructs such as:

```text
{{ variable }}
```

file-oriented function calls, and Mermaid code fences.

The objective is to determine requirements without rendering or executing the component.

---

## Compiler Adapters

Compiler adapters implement output-specific compilation.

The architecture currently includes support for:

### HTML

Generates a standalone HTML document.

### PDF

Uses the HTML representation as an intermediate format and renders the result through the current Python-based PDF pipeline.

### DOCX

Generates Word documents and encapsulates structural document merging inside the DOCX compiler.

The Engine itself should not contain format-specific implementation details.

---

## Dependency Injection

Concrete adapters and compilers are supplied to the Engine through dependency injection.

Conceptually:

```python
engine = Engine(
    planning=planning,
    solving=solving,
    assembling=assembling,
    compilation=compilation,
)
```

This allows:

* independent testing;
* alternative implementations;
* custom component adapters;
* custom compilers;
* reduced coupling between orchestration and infrastructure.

---

## Basic Usage

A typical programmatic workflow is:

```python
workspace = engine.init_workspace("./my-project")

session = engine.create_session(workspace)

while True:
    interaction = engine.create_interaction(session)

    if interaction.is_solved:
        break

    # Application provides the required values.
    # Continue the same session.

result = engine.compile(
    session=session,
    target_format="pdf",
)
```

The exact interaction contract is defined by the Engine's public models.

---

## Important Rule: Do Not Compile an Unresolved Session

Compilation is the final stage.

If the dependency graph has unresolved requirements, the application should continue the solving interaction instead of attempting compilation.

The intended lifecycle is:

```text
Planning
   ↓
Solving
   ↓
Pending? ── Yes ──► Application input
   │
   No
   ↓
Assembling
   ↓
Compilation
```

---

## Extending the Engine

To add a new component type:

1. Define the component contract.
2. Implement the corresponding adapter.
3. Register the adapter.
4. Implement static inspection if the component exposes discoverable dependencies.
5. Add tests.
6. Ensure the Engine does not require format-specific conditional logic.

To add a new output format:

1. Implement the compiler contract.
2. Register the compiler.
3. Add format-specific tests.
4. Keep format-specific behavior inside the compiler.

This preserves the Engine's orchestration role.

---

## Error Handling

Engine-specific errors inherit from the project's base exception.

Typical errors include:

```python
BaseDocException
├── NodeAlreadyRegistered
├── NodeNotFoundException
├── ResolutionException
├── DownloadException
├── GraphNotSolvedException
└── ContentNotAvaliable
```

Consumers should catch the most specific exception applicable to their use case.

---

## Testing

Engine tests should focus on behavior rather than implementation details.

Important test areas include:

* workspace creation;
* recipe loading;
* static dependency discovery;
* unresolved requirements;
* iterative solving;
* nested dependencies;
* scheduler behavior;
* component adapter selection;
* compilation;
* compiler selection;
* invalid resources;
* unresolved graphs.

---

## Design Goals

The Engine is intentionally designed around:

* separation of concerns;
* dependency inversion;
* polymorphism;
* explicit execution state;
* side-effect-free static inspection;
* isolated adapters;
* isolated compilers;
* extensibility without modifying orchestration code.

The dependency-resolution mechanism and adapter architecture were introduced specifically to prevent the central Engine from becoming a collection of format-specific conditionals.
