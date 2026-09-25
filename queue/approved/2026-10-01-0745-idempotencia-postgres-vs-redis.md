---
scheduled_at: 2026-10-01T07:45:00-03:00
visibility: PUBLIC
type: TEACH
hook: "#11 Myth Bust"
human_score: 79.6
---
Redis não é por que evento duplicado continua passando na sua idempotência. O motivo é outro: a janela entre 2 passos que ninguém trata como 1 operação só.

Nesse projeto pessoal que venho construindo, um app que processa upload de áudio, eu usava Redis com SETNX pra garantir que o mesmo upload não fosse processado 2 vezes. Parecia resolvido.

Só que criar o registro do upload e colocar ele na fila são 2 passos separados, e não 1. Se o processo cai bem entre os 2, o registro existe, mas a fila nunca soube dele.

Nenhuma trava do Redis impede isso. Ela protege o passo de enfileirar. Não protege a janela antes dele.

A correção foi tirar o Redis dessa parte e usar uma coluna de idempotência direto no Postgres, no mesmo registro que já ia pro banco de qualquer jeito, de forma que criar o registro e marcar ele como pronto pra fila virassem a mesma transação, sem depender de mais nenhum sistema pra isso.

Se a fila falhar depois, dá pra reprocessar sem duplicar nada.

A regra que fica: o banco é a fonte da verdade. Fila e cache são só aceleradores. Quando os 2 discordam, quem manda é o banco.

Sua idempotência hoje mora numa trava de cache ou numa transação que não pode ficar pela metade?
