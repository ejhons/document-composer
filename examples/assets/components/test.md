
---
title: Memorial
fields:
  flow:
    type: number
    label: Vazão
---
# Memorial
Cliente: {{ client.name }}
Vazão: {{ flow }}

@include(
    "tabela.xlsx",
    optional=True
)
