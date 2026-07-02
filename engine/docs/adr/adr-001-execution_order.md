## Context
I am facing a problem for solving markdown template. 
They may have children componentes as mermaid graphs, images, variable fields.
Those dependencies occur in execution time since the artifacts are loaded when executed and the proposal
of application defends on that. So, I can't change it to a static or pre-loaded way.

Decision
I have to build a dependency solver. 
One interesting thing is that way that dependencies are found suggest a only one depth level which simplifies it.

Consequences
I have to reestructure the engine, scheduler and create a dependency solver.
