# DocComposer Application

The **DocComposer Application** package provides the application-level orchestration around the DocComposer Engine.

It translates user-oriented operations into Engine operations while keeping the Engine independent from presentation and delivery concerns.

The Application layer is the preferred integration point for interfaces such as the CLI.

---

## Responsibilities

The Application layer is responsible for:

* defining application use cases;
* coordinating Engine operations;
* managing interaction workflows;
* translating application intent into Engine calls;
* maintaining the lifecycle of document-generation sessions;
* exposing results suitable for presentation layers.

It is not responsible for:

* parsing terminal arguments;
* rendering terminal output;
* implementing document adapters;
* implementing compilers;
* performing low-level document processing.

---

## Architecture

The intended dependency direction is:

```text
Presentation
     │
     ▼
Application
     │
     ▼
Engine
```

For the current project:

```text
CLI
 │
 ▼
Application
 │
 ▼
Engine
```

The CLI should not implement document-generation logic itself.

---

## Use Cases

The Application package organizes operations around user intent rather than Engine internals.

A typical document-generation use case is:

```text
Start Document Build
        │
        ▼
Create Execution Session
        │
        ▼
    Interact
        │
        ├── Requirements pending?
        │        │
        │        ▼
        │   Collect input
        │        │
        │        ▼
        │        │
        ├────────┘
        │
        ▼
Document Resolved
        │
        ▼
    Compile
        │
        ▼
  Build Result
```

This structure allows the same use case to be consumed by different delivery mechanisms.

---

## Build Workflow

The application should expose a complete build workflow without forcing callers to know the internal Engine pipeline.

Conceptually:

```python
use_case = create_build_document(interaction)

session = use_case.start(workspace)

while True:
    result = use_case.interact(
        session=session,
        values=values,
    )

    if result.is_solved:
        break

    values = collect_values(result.pending)

result = use_case.compile(
    session=session,
    target_format="pdf",
)
```

The exact factories and method signatures are part of the package API.

---

## Interaction

Document generation is not necessarily a single request-response operation.

The Application layer therefore treats the solving process as an interaction.

A typical interaction result contains:

```text
Solved
or
Pending Requirements
```

Pending requirements may include:

* input definitions;
* unresolved dependencies;
* the relationship between pending requirements and document nodes.

This information is intentionally structured so that a presentation layer can decide how to collect the missing values.

---

## Why Interaction Belongs Here

The Engine knows **how to solve** a document.

The Application layer knows **how the application should coordinate the solving process**.

The CLI knows **how to communicate with the user**.

These responsibilities should remain separate.

For example:

```text
Engine:
    "These variables are unresolved."

Application:
    "The build operation needs another interaction."

CLI:
    "Please enter the value for this variable."
```

The CLI should never need to understand how the dependency graph itself is implemented.

---

## Session Lifecycle

The `ExecutionSession` is created by the application use case and passed through successive interactions.

```text
Session #1
   │
   ├── Planning
   ├── Solving
   └── Pending
          │
          ▼
     User provides values
          │
          ▼
Session #1
   │
   ├── Solving
   ├── Resolved
   ├── Assembling
   └── Compilation
```

The same session represents the same document-generation operation.

---

## Interaction Results

The application should expose a simple state model.

Conceptually:

```text
READY
PENDING
```

When pending:

```text
PendingResolution
├── input_definitions
├── pending
│   ├── node
│   │   ├── inputs
│   │   └── dependencies
│   └── ...
└── resolved
```

This structure allows callers to understand not only what is missing, but where the requirement originates.

---

## Separation from Presentation

The Application layer should not contain code such as:

```python
print(...)
typer.echo(...)
typer.prompt(...)
```

Those are CLI concerns.

Likewise, it should not contain:

```python
@app.post(...)
```

Those are HTTP delivery concerns.

The Application layer should operate through Python objects and explicit use-case contracts.

---

## Build Result

After successful compilation, the application returns a result containing information required by the presentation layer.

Conceptually:

```text
CompilationResult
├── target format
└── generated output
```

The CLI can then display:

```text
Build completed.
Output: /path/to/output/document.pdf
```

without knowing how the PDF was generated.

---

## Error Handling

Application services should allow domain and Engine exceptions to propagate unless they have a meaningful application-level interpretation.

For example:

```text
Engine exception
      │
      ▼
Application
      │
      ├── handle when meaningful
      │
      └── propagate otherwise
      │
      ▼
Presentation
```

The Application layer should not silently convert every error into a generic failure.

Preserving meaningful exception types allows the CLI and future interfaces to provide useful feedback.

---

## Composition

The Application layer receives its dependencies rather than constructing infrastructure internally.

Conceptually:

```python
application = Application(
    engine=engine,
    interaction=interaction_port,
)
```

The composition root is responsible for assembling concrete implementations.

This prevents application services from becoming hidden dependency containers.

---

## Testing

Application tests should focus on use-case behavior.

Important scenarios include:

* starting a build;
* creating a session;
* handling pending requirements;
* continuing an existing session;
* completing a multi-step interaction;
* refusing compilation before resolution;
* compiling after resolution;
* propagating Engine failures;
* returning useful build results.

Mocks or test doubles can be used for the Engine and interaction ports.

---

## Design Principles

The Application layer follows these principles:

### Use-case oriented

Operations represent application intentions rather than technical details.

### Thin orchestration

Application services coordinate components; they do not reproduce Engine logic.

### Presentation independent

The same use case can be consumed by a CLI, HTTP API, or another interface.

### Explicit state

Interactive progress is represented through explicit sessions and results.

### Dependency inversion

Concrete infrastructure is provided from outside the application service.

---

## Current Scope

The Application package currently exists to support the core document-generation workflow and the CLI.

Future delivery mechanisms can consume the same application services without changing the Engine.

For example:

```text
              ┌── CLI
              │
Application ──┼── HTTP API
              │
              └── Other Interface
```

The Engine remains below all of them.
