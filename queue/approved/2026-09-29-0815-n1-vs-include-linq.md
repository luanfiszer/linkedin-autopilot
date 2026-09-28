---
scheduled_at: 2026-09-29T08:15:00-03:00
visibility: PUBLIC
type: PROOF
hook: "#10 The Receipt"
human_score: 86.9
image: "media/fotos/gerado-n1-vs-include.png"
image_alt: "Cartão de código: consulta N+1 em LINQ vs a versão que traz tudo com Include"
---
15% de latência a menos. Veio de um N+1 escondido dentro de um LINQ.

Isso foi na PROVER, minha empresa anterior, quando eu ainda era dev júnior.

Tinha um conjunto de consultas críticas no SQL Server. A gente usava Entity Framework Core com LINQ, e é fácil escrever uma consulta que parece inofensiva no código e vira várias idas ao banco por trás.

O padrão era o clássico N+1: a consulta principal disparava uma consulta extra pra cada item do resultado, em vez de trazer tudo de uma vez.

Reescrevi as consultas mais críticas pra buscar os dados relacionados numa única ida ao banco.

A latência das requisições caiu 15%.

A correção não pediu reescrita grande. Pediu olhar o SQL que o LINQ gerava, em vez de confiar que o ORM ia resolver sozinho.

Performance sem olhar a consulta que sai do ORM é chute.

Você já caçou um N+1 escondido atrás de um ORM? Onde ele estava?
