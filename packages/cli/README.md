# DocComposer CLI

The **DocComposer CLI** provides the command-line interface for building documents with **DocComposer**.

It is intentionally a thin presentation layer over the Application package.

The CLI is responsible for terminal interaction, argument parsing, user feedback, and presentation of errors and results. Document-processing logic remains in the Engine and Application packages.

---

## Installation

Install DocComposer using the project's Python package:

```bash
pip install document-composer
```

After installation, the CLI should be available as:

```bash
dcp
```

Verify the installation:

```bash
dcp --help
```

If the project is being developed from source:

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

---

## Basic Usage

DocComposer is designed around a single primary build command.

From a project workspace:

```bash
dcp build
```

The current directory is used as the default workspace.

A different workspace can be provided explicitly:

```bash
dcp build /path/to/project
```

This provides two common usage modes:

```text
Current directory
      │
      ▼
dcp build
```

or:

```text
Explicit workspace
      │
      ▼
dcp build /path/to/project
```

---

## Output Format

The target output format can be selected with `--format` or `-f`.

For example:

```bash
dcp build --format pdf
```

or:

```bash
dcp build -f pdf
```

Supported formats currently include:

```text
html
pdf
docx
md
```

The exact set of registered formats depends on the installed Engine configuration.

---

## Workspace

The directory from which the command is executed is the default workspace.

For example:

```bash
cd my-document
dcp build
```

is equivalent in concept to:

```bash
dcp build ./my-document
```

The workspace contains the project resources required by the document-generation process.

A typical project may contain:

```text
my-document/
├── metadata.json
├── recipe.json
├── components/
└── output/
```

The CLI does not directly implement the workspace model. It delegates workspace handling to the Application and Engine layers.

---

## Build Lifecycle

Running:

```bash
dcp build
```

does not simply execute a fixed sequence of file conversions.

The build operation follows the DocComposer interaction lifecycle:

```text
CLI
 │
 ▼
Application
 │
 ▼
Start Session
 │
 ▼
Planning
 │
 ▼
Solving
 │
 ├── Pending requirements
 │            │
 │            ▼
 │   CLI collects input
 │            │
 │            ▼
 │            │
 └────────────┘
 │
 ▼
Resolved
 │
 ▼
Assembling
 │
 ▼
Compilation
 │
 ▼
Output
```

This is necessary because document requirements may only become fully known after earlier requirements have been resolved.

---

## Interactive Resolution

When the document has unresolved requirements, the CLI presents the pending information to the user.

Conceptually:

```text
Document requires additional input.

Variable: project_title
Value:
```

After receiving the value, the CLI continues the same build session.

This process may repeat several times before the document is ready for compilation.

The CLI should therefore never assume that one call to the Engine is enough to complete a build.

---

## Successful Build

After compilation, the CLI reports the generated output.

Example:

```text
Session started.
Loading document requirements...
Resolving pending inputs...
Compiling document...

Session completed.
Output: output/document.pdf
```

The actual output path is provided by the Application/Engine result rather than reconstructed by the CLI.

---

## Error Handling

Because `build` represents the complete document-generation workflow, error handling is an important part of the CLI.

The CLI should distinguish between:

* invalid user input;
* invalid project configuration;
* missing resources;
* unresolved document requirements;
* dependency-resolution failures;
* compilation failures;
* unexpected internal errors.

The Engine provides typed project exceptions, including:

```text
NodeAlreadyRegistered
NodeNotFoundException
ResolutionException
DownloadException
GraphNotSolvedException
ContentNotAvaliable
```

The CLI should translate these exceptions into concise, actionable terminal messages.

---

## Expected Error Behavior

Errors should provide enough context for the user to understand what failed.

For example:

```text
Error: document graph could not be resolved.

The following requirements are still pending:
- project_title
- author
```

is preferable to:

```text
Error: GraphNotSolvedException
```

Likewise, unexpected exceptions should be logged with sufficient diagnostic information while keeping the terminal output readable.

---

## Logging

The CLI should separate:

```text
User-facing messages
        +
Diagnostic logging
```

User-facing output should communicate the progress and result of the operation.

Logging should provide technical information useful for debugging.

The CLI should not expose internal implementation details unless they are useful for diagnosing a failure.

---

## Command Reference

### `build`

Builds a document from the current workspace or an explicitly provided workspace.

```bash
dcp build [ROOT]
```

Arguments:

| Argument | Description                                                       |
| -------- | ----------------------------------------------------------------- |
| `ROOT` | Path to the project workspace. Defaults to the current directory. |

Options:

| Option       | Short  | Description             |
| ------------ | ------ | ----------------------- |
| `--format` | `-f` | Target document format. |

Examples:

```bash
dcp build
```

```bash
dcp build ./report
```

```bash
dcp build ./report --format pdf
```

```bash
dcp build ./report -f docx
```

---

## CLI Architecture

The CLI should remain deliberately small.

```text
dcp_cli
│
├── commands
│   └── build
│
├── interaction
│   └── terminal interaction
│
└── presentation
    └── messages / errors / output
```

Its dependencies point toward the Application layer:

```text
CLI
 ↓
Application
 ↓
Engine
```

The CLI should not import internal Engine adapters or manipulate document components directly.

---

## Why the CLI Does Not Contain Build Logic

Avoid implementations such as:

```python
if format == "pdf":
    ...
elif format == "docx":
    ...
```

or:

```python
load_recipe(...)
resolve_dependencies(...)
assemble_document(...)
compile_pdf(...)
```

inside the command implementation.

Those responsibilities belong to the lower layers.

The CLI should essentially perform:

```text
Parse arguments
      ↓
Create application use case
      ↓
Start build
      ↓
Interact with user
      ↓
Display result
```

This keeps the command stable even as the Engine evolves.

---

## Python Entry Point

The package should expose the CLI through the project's Python entry point.

The intended user experience is:

```bash
dcp --help
dcp build
```

rather than requiring users to know the internal Python module structure.

---

## Development

Install the CLI from the repository:

```bash
pip install -e .
```

Run it directly:

```bash
dcp build
```

For development dependencies:

```bash
pip install -e ".[dev]"
```

The CLI should be tested independently from the Engine implementation.

Important test categories include:

* argument parsing;
* default workspace behavior;
* explicit workspace behavior;
* format selection;
* successful builds;
* interactive resolution;
* user cancellation/input errors;
* known Engine exceptions;
* unexpected exceptions;
* output reporting.

---

## Design Principles

The CLI follows four primary rules:

### Thin

The CLI should contain as little business logic as possible.

### User-oriented

Messages should describe what the user needs to know rather than expose internal implementation details.

### Deterministic

Arguments should produce predictable application operations.

### Reusable

All document-processing behavior should live below the CLI so that other interfaces can reuse it.

---

## Relationship with the Other Packages

```text
┌───────────────────────┐
│      doc-cli          │
│ Terminal presentation │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│   doc-application     │
│   Application use     │
│       cases           │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│      doc-engine       │
│ Document processing   │
│ Dependency resolution │
│ Assembly & compilation│
└───────────────────────┘
```

The CLI is therefore a consumer of the Application package, not an alternative implementation of the Engine.

---

## End-User Quick Start

For a user who simply wants to build a document:

```bash
pip install document-composer
cd my-document
dcp build
```

To select the output format:

```bash
dcp build -f pdf
```

The CLI handles the interaction required to resolve the document and reports the resulting artifact when compilation succeed
