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