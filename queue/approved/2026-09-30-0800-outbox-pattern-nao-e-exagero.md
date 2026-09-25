---
scheduled_at: 2026-09-30T08:00:00-03:00
visibility: PUBLIC
type: OPINION
hook: "#1 Contrarian Take"
human_score: 81.8
---
Outbox Pattern. Todo mundo acha que é over-engineering pra maioria dos projetos.

Depois de ver o buraco que ele tapa, acho o contrário.

O argumento contra é sempre o mesmo: publica o evento direto depois de salvar, sem essa complexidade toda. Só que salvar no banco e publicar na fila são 2 operações separadas, com 2 pontas que podem falhar cada uma por conta própria, e não existe uma transação que cubra as 2 ao mesmo tempo.

Se o banco confirma e a publicação falha, ninguém percebe na hora. O sistema segue rodando. Os dados ficam inconsistentes. O bug só aparece semanas depois, quando alguém pergunta por que 1 evento nunca chegou.

Implementei Outbox Pattern com processamento em background e RabbitMQ no trabalho, recentemente: a escrita no Postgres e o registro do evento acontecem na mesma transação, e um processo separado garante a publicação depois.

Deu mais peça pra manter, sim. Mas tirou uma categoria inteira de bug da mesa.

"Simples" só é virtude se o sistema continuar certo quando 1 das 2 pontas falha no meio.

Você já viu uma inconsistência dessas aparecer tarde demais pra dar pra saber de onde veio?
