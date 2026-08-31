from pprint import pprint

from dcp_engine.assembly.atomizer import MarkdownAtomizer
from dcp_engine.language.parser import MarkdownParser



markdown = r"""
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

def test_atomizer_must_return_atomized_markdown():
    parser = MarkdownParser()
    atomizer = MarkdownAtomizer(parser)

    atomized = atomizer.atomize(markdown=markdown)

    print(len(atomized.blocks))
    pprint(atomized.model_dump())

    assert len(atomized.blocks) == 7
    # assert None
