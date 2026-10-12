---
scheduled_at: 2026-10-22T08:30:00-03:00
visibility: PUBLIC
type: TEACH
hook: "#16 Good vs Great"
human_score: 72
image: "media/fotos/gerado-soft-delete-filtro.png"
image_alt: "Diagrama: registro excluído ainda aparecia pro serviço; correção foi um filtro global HasQueryFilter no EF Core, com IgnoreQueryFilters só onde precisa"
image_request: "Print de um teste seu passando no terminal do projeto pessoal, ou uma foto do seu setup à noite. Sem nada do trabalho na tela."
---
Código comum lembra de filtrar o registro excluído em cada consulta nova. Código bom não dá essa escolha pra ninguém.

A diferença é onde a regra mora: na cabeça de quem escreve a query, ou no mapeamento, uma vez só.

Soft delete é a prática de não apagar a linha do banco quando um registro é excluído: só marca uma coluna (por exemplo excluido_em) e os sistemas deveriam parar de mostrar aquele registro.

Um registro apagado assim no sistema de origem continuava aparecendo no meu serviço. O motivo: o mapeamento da minha entidade, em EF Core, não sabia que a coluna de exclusão existia. Toda consulta via o registro como se estivesse vivo, inclusive o progresso que o usuário tinha ali, que continuava contando pra sempre.

A correção óbvia seria lembrar de colocar um WHERE excluido_em IS NULL em toda query nova. Isso funciona até a query que alguém escreve numa sexta-feira às 18h, sob pressão, sem lembrar da regra.

O que eu fiz foi diferente: mapear a coluna de exclusão e colocar um filtro global de consulta, HasQueryFilter, direto no DbContext. Por padrão, nenhuma consulta do sistema vê um registro excluído. Ninguém precisa lembrar de nada.

O único lugar que realmente precisa ver os excluídos, pra descartar o progresso de um item que sumiu, usa IgnoreQueryFilters de forma explícita, no código, visível pra quem revisar o Pull Request.

Soft delete é um contrato. Todo leitor da tabela precisa conhecer ele. Filtro por consulta depende de memória; filtro global transforma esquecer em impossível, e quem quiser a exceção tem que pedir ela às claras, em texto, não por acidente.

Seu soft delete está documentado em algum lugar, ou só na cabeça de quem escreveu a primeira query?

#EFCore #DotNet
