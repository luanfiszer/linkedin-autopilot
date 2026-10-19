---
scheduled_at: 2026-10-29T08:30:00-03:00
visibility: PUBLIC
type: TEACH
hook: "#8 Question Trap"
human_score: 73.4
image: "media/fotos/gerado-progresso-identidade.png"
image_alt: "Cartão de código em C# comparando a regra errada (1 item antes, 1 depois = mesmo, por posição) com a certa (comparar o conjunto de ids ordenado, com SequenceEqual)"
image_request: "Print de um teste seu passando no terminal do projeto pessoal, mostrando esse tipo de comparação. Sem nome de projeto ou caminho de pasta visível."
---
Se um item de uma lista for trocado por outro, na mesma posição, o progresso do usuário devia continuar valendo?

A resposta que parece certa é sim.

Foi a resposta que o sistema que eu mantenho dava, até essa semana.

A regra antiga: quando o conteúdo de uma etapa era reconstruído, o progresso anterior passava pro conteúdo novo sempre que houvesse exatamente um item antes e um item depois, na mesma posição.

Parece razoável.

Na prática, "um antes, um depois, deve ser o mesmo" é uma heurística de posição, não de identidade, e as duas coisas só coincidem até o dia em que alguém troca o conteúdo de um item sem trocar a posição dele.

Se o item na posição 3 fosse trocado por outro completamente diferente, o usuário herdava o progresso de algo que ele nunca fez.

Uma etapa sem nenhum item ainda entrava na conta do progresso total.

A correção comparou o conjunto de ids de antes contra o de depois com LINQ puro, em .NET: cada grupo virou um List de Guid, OrderBy pra ordenar, SequenceEqual pra comparar. Só repassa o progresso se os dois conjuntos forem exatamente iguais, e etapa vazia deixou de contar.

Deu pra ir além.

A reconstrução passou a usar GroupBy e Except, devolvendo um IEnumerable só com os grupos que mudaram de composição. A regra de "o que conta como progresso" ficou numa classe só, usada nos dois lados.

Estado de usuário se casa por identidade.

Posição é coincidência, até o dia em que não é mais.

Onde no seu sistema uma regra confia na posição de um item quando devia confiar no id dele?

#BackEnd #DotNet