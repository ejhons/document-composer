Hexagonal: Para tarefa de conversão, permitindo atribuir a um formato uma metodologia de conversão

CGerenciador de Registro: Para a engine, os adaptadores de conversão são registrados com o formato oque irão atender.

**Artefato Compilado Intermediário** (ou *Intermediate Representation* - IR) -> Assembled Manifest
    Fazer isso traz três vantagens brutas para o seu projeto:

    Rastreabilidade Total: O usuário ganha um arquivo Markdown "puro", sem placeholders {{ ... }}, sem blocos complexos de código Mermaid (já convertidos em imagens) e com as tabelas Excel já injetadas em texto. Ele pode abrir esse arquivo em qualquer editor de Markdown do planeta e o documento estará perfeitamente montado.

    Auditoria e Debug: Se a conversão para PDF ou Word falhar ou quebrar o layout, você consegue abrir o Markdown final e descobrir exatamente qual bloco quebrou o texto.

    Ponto de Entrada Perfeito para o Flutter Web: Na nuvem, você pode salvar esse arquivo intermediário no seu banco de dados ou storage. Se o usuário quiser apenas visualizar o documento na tela do navegador via Flutter, você renderiza esse Markdown final de forma instantânea, sem precisar que ele baixe o Word ou acione o Pandoc novamente.