## Context

I have too much layers for converting a RecipeManifest to a AssmbledMarkdown. The step after solving RecipeGraph dependencies, variables and directives is getting noisy. In this moment, I convert the RecipeGraph to a DocumentIR but it doesn't seems represent correctly the assembled document as well.

## Decision

Use a object Fragmented Markdown. This object represents very well the structure of finished document, keeping spaces and locals of insertion of directives, images, references, etc.

DocumentIR will not act in RecipeGraph, but in FragmentedMarkdown allowing editing and locking positions.

## Consequences

Create a new class: FragmentedMarkdown.
