# Routes

```
GET    /api/projects
POST   /api/projects

GET    /api/projects/{id}
DELETE /api/projects/{id}

GET    /api/projects/{id}/files
POST   /api/projects/{id}/files
DELETE /api/projects/{id}/files/{path}

GET    /api/projects/{id}/recipe
PUT    /api/projects/{id}/recipe

POST   /api/projects/{id}/compile

GET    /api/projects/{id}/artifacts/{file}
```

## Request & Response Table

| Method | Rota                            | Função                                                                                        | Request              | Response              |
| ------ | ------------------------------- | ----------------------------------------------------------------------------------------------- | -------------------- | --------------------- |
| GET    | `/projects`                   | Retorna a lista de projetos                                                                     |                      | ProjectListResponse   |
| POST   | `/projects`                   | Cria um novo projeto                                                                            | CreateProjectRequest |                       |
| GET    | `/projects/{id}`              | Retorna as informações do projeto                                                             |                      | ProjectResponse       |
| DELETE | `/projects/{id}`              | Deleta o projeto, mantendo os arquivos                                                          |                      |                       |
| GET    | `/projects/{id}/files`        | Retorna a lista de arquivos presentes no projeto (melhorar para retornar a árvore de arquivos) |                      | FileTreeResponse      |
| POST   | `/projects/{id}/files`        | Adiciona o arquivo baixado como componente                                                      | UploadFile           |                       |
| DELETE | `/projects/{id}/files/{path}` | Apaga um arquivo componente                                                                     | FilePathRequest      |                       |
| GET    | `/projects/{id}/recipe`       | Retorna o endereço e o conteúdo do arquivo recipe.json                                        |                      | RecipeContentResponse |
| PUT    | `/projects/{id}/recipe`       | Atualiza o conteúdo do arquivo recipe.json                                                     | UpdateRecipeRequest  |                       |
| POST   | `/projects/{id}/compile`      | Compila os componentes para gerar o arquivo                                                     | CompileRequest       | CompilationResponse   |
| GET    | `/projects/{id}/files/{path}` | Retorna uma prévia do arquivo (quando disponível, no caso de markdown.)                       | FilePathRequest      | FileContentResponse   |
| PUT    | `/projects/{id}/files/{path}` | Atualiza o conteúdo do arquivo markdown.                                                       | FileContentRequest   |                       |
