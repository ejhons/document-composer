```
                 composer build recipe.json
                              │
                              ▼
                    doc-composer-cli
                              │
                              ▼
                    BuildDocumentUseCase
                              │
                              ▼
                    DocumentEngine.execute()
                              │
                    ┌─────────┴──────────┐
                    │                    │
             internal dependency    external value
                    │                    │
                    ▼                    ▼
              TaskScheduler           PENDING
                    │                    │
                    │                    ▼
                    │                  CLI
                    │                    │
                    │                    ▼
                    │              ExecutionContext
                    │                    │
                    └──────────┬─────────┘
                               ▼
                        execute(session)
                               │
                               ▼
                            SUCCESS
```
