---
scheduled_at: 2026-09-30T08:00:00-03:00
visibility: PUBLIC
type: OPINION
hook: "#1 Contrarian Take"
human_score: 75.0
image: "media/fotos/gerado-outbox-fluxo.png"
image_alt: "Diagrama: dados e evento gravados na mesma transação numa tabela outbox; um worker lê e publica no RabbitMQ"
---
Salvar no banco e publicar o evento logo em seguida parece inofensivo. Não é.

No .NET, o código costuma ser um SaveChangesAsync() do EF Core e, na linha de baixo, um publish no RabbitMQ.

Se você já escreveu isso, provavelmente funciona. Até o dia em que não funciona.

São duas operações diferentes, e nenhuma transação cobre as duas. Aí, uma hora:
- o banco confirma, a publicação falha, e o evento some
- a publicação sai, o banco faz rollback, e existe um evento sobre algo que nunca foi salvo

Nenhum erro aparece.

O Outbox Pattern resolve isso de um jeito direto: o evento vai pra uma tabela de outbox no mesmo SaveChangesAsync() dos dados, e um hosted service em background lê essa tabela e publica no RabbitMQ. Se falhar, o registro continua lá pra próxima tentativa.

Eu implementei isso no trabalho há pouco tempo, com health check junto.

É mais uma peça pra gente manter? É. Mas tira uma categoria inteira de bug da mesa.

Por isso eu não acho que Outbox seja exagero.

Você publica eventos direto do código ou já usa algum tipo de outbox?
