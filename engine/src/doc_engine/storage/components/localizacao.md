
### 1. Localização e Dados Gerais

O terreno situa-se na zona urbana, possuindo uma área total calculada pela equação da área poligonal:

$$
A = \frac{1}{2} \sum_{i=1}^{n} (x_i y_{i+1} - x_{i+1} y_i)
$$

O valor declarado para o lote atual é de **{{ area_terreno }} m²**.

#### Diagrama de Fluxo de Cubação do Projeto

```mermaid
graph TD
    A[Início do Projeto] --> B(Análise de Solo)
    B --> C{Aprovado?}
    C -- Sim --> D[Cálculo Estrutural: '{{projeto}}']
    C -- Não --> E[Refazer Sondagem]
```
