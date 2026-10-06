---
scheduled_at: 2026-10-09T08:30:00-03:00
visibility: PUBLIC
type: OPINION
hook: "#6 Insider Secret"
human_score: 72.8
image: "media/fotos/gerado-soft-delete-filtro-global.png"
image_alt: "Cartão de código em C# comparando uma consulta que filtra exclusão manualmente com a correção: um HasQueryFilter global no EF Core, e IgnoreQueryFilters só no único lugar que precisa ver os excluídos"
image_request: "Uma foto do seu caderno ou quadro com um desenho simples de duas tabelas: uma com um item riscado (excluído) e uma seta mostrando o filtro barrando ele por padrão. Sem nada do trabalho."
---
A parte que a documentação de soft delete nunca conta: ela só funciona se todo leitor souber que existe.

Essa semana, um registro excluído (soft delete) no sistema de origem continuava aparecendo no meu serviço, porque o mapeamento da entidade do meu lado não declarava a coluna de exclusão. Pro meu código, a linha nunca tinha sumido.

Pior: o progresso que o usuário já tinha naquele item continuava contando, porque nada avisava que aquele item tinha sido excluído.

A correção óbvia seria filtrar "excluido = false" em toda consulta LINQ que toca essa tabela. Eu não fiz isso.

Mapeei as colunas de auditoria e de exclusão numa Migration nova, e pus um filtro global no DbContext do EF Core: um HasQueryFilter. Agora o padrão é não ver o excluído, em toda consulta.

No único lugar que precisa enxergar os excluídos, pra descartar o progresso de itens que sumiram, uso IgnoreQueryFilters de forma explícita.

Esquecer o filtro virou impossível. Esquecer de ignorá-lo onde precisa é uma linha visível no Repository, não um bug invisível.

Soft Delete não é uma coluna. É um contrato que todo leitor da tabela precisa conhecer, e filtro por rota depende só de alguém lembrar de escrevê-lo de novo em cada lugar novo. Filtro global depende de decisão.

Sua entidade sabe que a linha dela pode estar excluída, ou isso é responsabilidade de quem escreve a próxima consulta lembrar?
