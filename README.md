# DocComposer

> A local-first document composition and compilation framework for building complex documents from declarative recipes and reusable components.

DocComposer is a Python-based document composition system designed to transform structured **recipes**, reusable document components, templates, data inputs, and external resources into final documents such as **HTML, PDF, and DOCX**.

The project separates document planning, dependency resolution, document assembly, and final compilation into explicit stages. This makes the composition process predictable, extensible, and suitable for both interactive and automated workflows.

---

## Features

* Declarative document composition through recipe manifests
* Reusable document components
* Jinja-based template rendering
* Static dependency inspection before execution
* Interactive resolution of missing inputs and dependencies
* Dependency-aware execution using a LIFO task scheduler
* Nested component resolution
* Support for internal and external resources
* Pluggable adapters and compilers
* HTML, PDF, and DOCX compilation
* Local filesystem-based workspaces
* Python API for programmatic usage
* Command-line interface for end users
* Extensible architecture based on dependency inversion and polymorphism

The core engine is intentionally independent from the delivery layer. The web API and frontend are separate concerns and are not part of the current usage model.

---

## Architecture

DocComposer processes a document through four major stages:

```text
┌────────────┐
│  Planning  │
└─────┬──────┘
      │
      ▼
┌────────────┐
│  Solving   │◄──── User/Application input
└─────┬──────┘
      │
      ▼
┌────────────┐
│ Assembling │
└─────┬──────┘
      │
      ▼
┌────────────┐
│ Compilation│
└─────┬──────┘
      │
      ▼
 Final Document
```

### Planning

Planning inspects the recipe and its components before document execution.

The static inspection layer identifies information such as:

* template variables;
* file dependencies;
* embedded resources;
* supported component-specific constructs;
* Mermaid blocks and other structural elements.

The inspection process is designed to be free of execution side effects.

### Solving

Solving resolves the requirements identified during planning.

A document does not have to be completely resolvable in a single operation. The engine can return a structured representation of what is still pending, allowing an application or user interface to provide the missing information and continue the same session.

### Assembling

Once all required information is available, the engine resolves the component dependency graph and produces the final assembled document representation.

Nested dependencies are supported. A component may discover additional components during processing, which are scheduled and resolved before the parent component is completed.

### Compilation

The assembled document is passed to a compiler for the requested output format.

Currently supported output formats include:

* HTML
* PDF
* DOCX

Compilation only takes place after the document has been completely resolved.

---

## Dependency Resolution

DocComposer uses a dependency-aware execution model rather than a simple sequential loop.

The `TaskScheduler` maintains an execution stack and completed-task registry. When a component discovers a dependency, that dependency is scheduled before the parent component continues.

For example:

```text
Markdown
   │
   ├── Excel
   │
   └── Mermaid
```

The Markdown component can be temporarily suspended while its dependencies are resolved.

This mechanism also supports deeper dependency chains:

```text
Markdown
   └── Excel
        └── Graph
             └── Resource
```

The execution model is based on a LIFO stack and allows unresolved parent tasks to return to the execution cycle after their dependencies have been completed.

---

## Workspace

A workspace represents the physical directory associated with a DocComposer project.

A typical workspace may look like:

```text
my-document/
├── metadata.json
├── recipe.json
├── components/
└── output/
```

The exact contents depend on the recipe and project configuration.

The workspace is responsible for providing access to project resources such as:

* recipe;
* metadata;
* components;
* generated output.

Resources referenced with relative paths are resolved against the workspace. Absolute paths can be used to reference external resources.

This allows reusable resources to live outside a specific project workspace without introducing a separate component model.

---

## Recipe-Based Composition

A document is described by a recipe.

Conceptually, a recipe defines:

```text
Recipe
├── identity
├── version
├── target format
├── style
└── components
```

Components can represent different types of document content, including Markdown templates, spreadsheets, images, diagrams, and other supported resources.

A component can also reference other components or external resources.

---

## Templates

Markdown templates can use Jinja-style expressions:

```jinja2
# {{ title }}

Prepared for {{ author }}.

The total estimated cost is {{ total_cost }}.
```

During planning, template variables can be identified before rendering.

During solving, the application provides the values required by the template.

Only after all required values have been resolved does the template become part of the final assembled document.

---

## Embedded Content

DocComposer supports content that is embedded inside another document component.

For example, a Markdown document can request content generated from another resource:

```text
Markdown
    ↓
Excel component
    ↓
Generated Markdown representation
```

Mermaid diagrams can also be handled as standalone components or embedded inside text content.

The engine mediates these interactions without requiring individual adapters to depend directly on one another.

---

## Compilation

The compilation layer converts the assembled representation into the requested output format.

### HTML

Produces a standalone HTML document.

### PDF

The current PDF pipeline uses an HTML intermediary and `xhtml2pdf`/ReportLab-based rendering, avoiding the need for LaTeX or GTK/GObject runtimes.

### DOCX

DOCX generation is handled by a dedicated compiler adapter. Structural merging of generated Word subdocuments is encapsulated inside the DOCX compiler rather than in the orchestration layer.

---

## Installation

### From source

Clone the repository and install the project in editable mode:

```bash
git clone <repository-url>
cd doccomposer

pip install -e .
```

For development dependencies:

```bash
pip install -e ".[dev]"
```

> Replace the package extras above if the project defines a different development dependency group.

### Requirements

DocComposer requires a supported Python installation according to the project's `pyproject.toml`.

The exact runtime dependencies should be installed through the package manager rather than manually.

Some output workflows may also rely on external executables, particularly Pandoc. Verify the installation requirements of the selected compiler before using a format that depends on them.

---

## Command-Line Usage

The recommended end-user interface is the `doc-compose` command.

From a project workspace:

```bash
dcp build
```

A different workspace can be supplied explicitly:

```bash
dcp build /path/to/project
```

The output format can be selected with:

```bash
dcp build --format pdf
```

or:

```bash
doc-compose build -f pdf
```

The verbosity of logs can be changed with:

```bash
dcp build --verbose
```

or:

```bash
dcp build -v
```

The CLI starts an interaction session, resolves pending requirements, and only then compiles the final document.

---

## Python Usage

DocComposer can also be used directly from Python.

The recommended architecture is to construct the engine and application services through the project's composition layer rather than instantiating individual internal components unnecessarily.

Conceptually:

```python
from dcp_engine import Engine

engine = Engine(
    planning=planning,
    solving=solving,
    assembling=assembling,
    compilation=compilation,
)

workspace = engine.init_workspace("./my-project")
session = engine.create_session(workspace)
```

The exact constructors and factories are part of the package API and may evolve independently from the CLI.

---

## Interaction Model

Document generation is intentionally iterative.

A typical application flow is:

```text
Start Session
      │
      ▼
   Planning
      │
      ▼
    Solving
      │
      ├── Pending inputs? ──► Provide values
      │                           │
      │                           └──────┐
      ▼                                  ▼
      └────────────────────────────── Solving
                                         │
                                         ▼
                                      Resolved
                                         │
                                         ▼
                                     Assembling
                                         │
                                         ▼
                                     Compiling
```

This is important for applications that cannot provide all document inputs at once.

The solving stage returns structured pending information instead of assuming that every document can be completed immediately.

---

## Project Structure

The project is organized around independent packages:

```text
DocComposer
│
├── Engine
│   └── Document composition and compilation core
│
├── Application
│   └── Application use cases and interaction orchestration
│
└── CLI
    └── Command-line interface
```

The dependency direction is intentionally one-way:

```text
CLI
 │
 ▼
Application
 │
 ▼
Engine
```

The Engine does not depend on the CLI.

The Application layer coordinates use cases without becoming responsible for document-processing internals.

The CLI is responsible for translating terminal interaction into application operations.

---

## Design Principles

DocComposer follows a small set of architectural principles:

### Separation of concerns

Planning, solving, assembling, and compiling have distinct responsibilities.

### Dependency inversion

Concrete adapters and compilers are injected into the engine instead of being hard-coded into orchestration logic.

### Polymorphism

Component and compiler behavior is selected through registries and interfaces rather than large conditional branches.

### Side-effect isolation

Static inspection should be able to analyze a component without executing its runtime behavior.

### Explicit state

Execution state belongs to the `ExecutionSession`, rather than being hidden inside global objects.

### Extensibility

New component types and output formats should be introduced by implementing the appropriate adapter/compiler contracts.

---

## Error Handling

DocComposer defines project-specific exceptions derived from a common base exception.

Examples include:

* `NodeAlreadyRegistered`
* `NodeNotFoundException`
* `ResolutionException`
* `DownloadException`
* `GraphNotSolvedException`
* `ContentNotAvaliable`

Applications should catch the most specific exception they can meaningfully handle.

In particular, compilation should not be attempted while the dependency graph remains unresolved.

---

## Development

Install the project in editable mode with development dependencies:

```bash
pip install -e ".[dev]"
```

Run the test suite using the project's configured test runner.

Before publishing a release, verify the complete workflow in a clean environment:

```text
Install
   ↓
Create/Open Workspace
   ↓
Build
   ↓
Resolve Inputs
   ↓
Compile
   ↓
Verify Output
```

---

## Current Scope

The current project focuses on the document-processing core and command-line workflow.

Included:

* Engine
* Application layer
* CLI
* Workspace management
* Recipe processing
* Static inspection
* Dependency resolution
* Document assembly
* HTML/PDF/DOCX compilation

Not currently covered by this README:

* HTTP API
* Web frontend
* Browser-based project management
* Remote execution

These are separate delivery concerns and should not be considered requirements for using the core engine.

---

## License

DocComposer is released under the Apache License. See [LICENSE](LICENSE) for the full license text.

---

## Status

DocComposer's core engine currently provides a stable architectural foundation for recipe-driven document generation, including dependency resolution, static inspection, component adapters, and compilation to HTML, PDF, and DOCX.
