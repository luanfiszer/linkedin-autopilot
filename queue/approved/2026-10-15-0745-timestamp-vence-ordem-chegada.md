---
scheduled_at: 2026-10-15T07:45:00-03:00
visibility: PUBLIC
type: TEACH
hook: "#16 Good vs Great"
human_score: 72.5
image: "media/fotos/gerado-timestamp-ordem-fluxo.png"
image_alt: "Diagrama: produtor publica com timestamp, a fila entrega fora de ordem ou duas vezes, o consumidor compara o timestamp salvo e ignora o que for mais antigo ou duplicado"
image_request: "Print do relógio mundial do seu celular, ou de um app mostrando dois horários de fuso diferente lado a lado. Ilustra bem a ideia de timestamp vencendo a ordem de chegada."
---
Sistema ruim confia na ordem de chegada da mensagem.

Sistema bom confia no timestamp de quem publicou.

Numa fila (RabbitMQ, SQS, tanto faz pra esse post), nada garante ordem. Uma mensagem mais antiga pode chegar depois de uma mais nova. A mesma mensagem pode chegar duas vezes.

Isso aconteceu comigo essa semana. O serviço que eu mantenho publica um Consolidado com a data em que foi gerado, guardada como DateTimeOffset em UTC. Eu passei a tratar cada mensagem assim, dentro da mesma transação que já fazia o UPSERT no Postgres:

- Consolidado mais antigo que o que já tá gravado? Eu ignoro.
- Chegou sem data? Ignoro e grava um aviso no log, porque isso não devia acontecer nunca.
- Faltou um bloco de dado dentro da mensagem? Preservo o que já estava lá: eu não apago um dado que a mensagem simplesmente não trouxe de novo.

Nada fica numa transação separada. Pra mim, isso importa mais que a regra em si: não existe janela entre eu checar e eu gravar.

Isso é idempotência de reprocessamento: entregar a mesma mensagem dez vezes tem que terminar no mesmo estado que entregar ela uma vez.

"A última que chegou vence" parece óbvio.

Até a sua fila reordenar na sua cara.

No seu sistema, o que decide qual dado é o mais recente: a hora que ele chegou, ou um timestamp de quem gerou?
