import pytest

from engine.compilation.ir.builder import DocumentIRBuilder
from engine.solving.inspection.pipeline import InspectionPipeline
from engine.planning.graph.builder import RecipeGraphBuilder
from engine.runtime.execution.context import ExecutionContext
from engine.runtime.engine import Engine
from engine.runtime.execution.session import ExecutionSession

def test_end_to_end(
    full_engine,
    temp_workspace,
    markdown_file,
    recipe_manifest,
    planning_context,
    scheduler
):

    markdown_file(
        "cover.md",
        """
# Cover
{{ client }}
"""
    )

    markdown_file(
        "memorial.md",
        """
---
fields_definition:
project_title:
    data_type: text
    label: Nome do Empreendimento
discipline:
    data_type: text
    label: Disciplina de projeto
fields:
  flow:
    type: number
    label: Vazão
---
@include('cover.md')
@include('image_{{logo}}.png')

# MEMORIAL TÉCNICO DE ENGENHARIA
## 1. Escopo Estrutural do Projeto: {{ project_title }}

O cálculo de dimensionamento dos pilares de sustentação, no empreendimento {{localization}}, foi executado utilizando o critério de esbeltez e tensão admissível do material, conforme a formulação clássica ({{ flow }}):

$$ \sigma = \frac{P}{A} \pm \frac{M}{W} $$

Abaixo, apresentamos o diagrama lógico que descreve o fluxo de validação da infraestrutura da obra {{classe}}:
```mermaid
graph TD
    A[Sondagem do Terreno] --> B(Análise de Carga)
    B --> C{Carga Suportada?}
    C -- Sim --> D[Fundação Direta]
    C -- Não --> E[Estacas Profundas]
```
@include("annex.md")
"""
    )

    markdown_file(
        "annex.md",
        """
# Annex
{{ project_title }}
"""
    )

    recipe_manifest.components[0].source = (
        temp_workspace / "cover.md"
    ).as_posix()

    recipe_manifest.components.append(
        recipe_manifest.components[0].model_copy(
            update={
                "id": "memorial",
                "source": (
                    temp_workspace / "memorial.md"
                ).as_posix()
            }
        )
    )

    execution_context = ExecutionContext(
        inputs= {
            'cliente': 'Cliente 123',
            'client': 'Cliente 1234',
            'classe': 'main',
            'logo':'generic',
            'project_title': 'Generic project',
            'localization': 'HERE',
            'flow': 35.0,
        }
    )

    session: ExecutionSession = full_engine.create_session(
        manifest=recipe_manifest,
        context=execution_context
    )

    full_engine.build_graph(
        session
    )
    
    full_engine.resolve(
        session
    )


    execution_plan = full_engine.plan(
        session,
        scheduler
    )

    
    document = DocumentIRBuilder().build(session.graph)

    assert document is not None