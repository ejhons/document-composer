
# Cover
Everton
![](C:/Users/evert/AppData/Local/Temp/pytest-of-evert/pytest-562/test_asembling_document0/components/img/image_generic.png)

# MEMORIAL TÉCNICO DE ENGENHARIA
## 1. Escopo Estrutural do Projeto: Generic project

O cálculo de dimensionamento dos pilares de sustentação, no empreendimento HERE, foi executado utilizando o critério de esbeltez e tensão admissível do material, conforme a formulação clássica (35.0):

$$ \sigma = \frac{P}{A} \pm \frac{M}{W} $$

Abaixo, apresentamos o diagrama lógico que descreve o fluxo de validação da infraestrutura da obra de Infraestrutura:
```mermaid
graph TD
    A[Sondagem do Terreno] --> B(Análise de Carga)
    B --> C{Carga Suportada?}
    C -- Sim --> D[Fundação Direta]
    C -- Não --> E[Estacas Profundas]
```

# Annex
Generic project