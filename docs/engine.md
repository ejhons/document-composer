1. Create `Engine`

```python
    engine = Engine(...)
```

2. Inicializa Compilers e Adapters`Engine._bootstrap()`

```python
    engine._bootstrap()
```

3. Create Session: `Engine.create_session()` passing `manifest` and `Context`

```python
    session = engine.create_session()
```

4. Build `graph` from `manifest`in `session`: `Engine.build_graph()`

```python
    graph = engine.build_graph()
```

5. Resolve `graph`in interective mode, taking passed user values:

```python
    engine.resolve()
```

6.1.
 If not `engine.resolved`, receive more user data and go back to step 5.
6.2. If `engine.resolved` generate adapated text converting artifact content to markdown or reference:

```python
    engine.adapt()
```

7. Tranforms `graph` into a `FragmentedMarkdown`. This object orgnizes in linear way blocks of markdown totally solved:

```python
    fragmented_markdown = engine.fragment()
```

8. Compiles document into given format.

```python
    engine.compile()
```

```json
{
    "recipe_name": "Relatório de Engenharia Estrutural",
    "version": "1.4.2",
    "target_format": "pdf",
    "style": {
        "reference_docx": "engine/src/doc_engine/storage/styles/reference.docx",
        "include_header": true,
        "include_footer": true,
        "header_text_left": "M&A Engenharia Associados",
        "header_text_right": "Cálculo de Infraestrutura",
        "footer_text_left": "Uso Interno e Confidencial - Proibida Reprodução",
        "primary_color": "#d9534f"
    },
    "components": [
        {
            "id": "corpo_tecnico",
            "type": "template",
            "source": "engine/src/doc_engine/storage/components/specifications.md",
            "file_format": "md"
        },
        {
            "id": "imagem simples",
            "type": "external",
            "source": "engine/src/doc_engine/storage/components/fluxograma.png",
            "file_format": "image",
            "condition": "discipline == 'terraplenagem'"
        }
    ]
}
```
