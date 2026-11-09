---
scheduled_at: 2026-11-17T08:15:00-03:00
visibility: PUBLIC
type: PROOF                 # PROOF | OPINION | TEACH | STORY | OFFER
hook: "#2 Number Reveal"
human_score: 86.9
image: "media/fotos/gerado-medir-antes-de-postar.png"
image_alt: "Diagrama: mudança no código, medição, comparação com a premissa e decisão de manter ou desfazer"
image_request: "Print de um gráfico ou resultado de benchmark do seu projeto pessoal (sem nome do projeto), ou foto de um rascunho à mão comparando o antes e o depois de uma medição."
---
{{N}} {{dias ou semanas}} tentando descobrir se {{a mudança que você fez}} funcionou de verdade. Ainda não sei.

Essa frase devia ter vindo com um número. Não vem.

Minha régua pra isso é simples: antes de postar um resultado, ele passa por tracing no Jaeger, por métrica no Prometheus e no Grafana, ou por um benchmark com taxa de erro e tempo de resposta de antes e depois. Se não passou por isso, não é resultado, é palpite.

A regra por trás disso: otimização sem medição é chute. Vale pra uma fila no RabbitMQ, pra uma query no Postgres, pra um SETNX no Redis, não importa se o serviço é em .NET ou em Python. Medir antes de decidir, e ter coragem de desfazer quando o número desmente a premissa que você tinha assumido.

Esse post ia contar {{o que você mudou}} e {{o resultado em número}}. A medição ainda não terminou.

Prefiro um post incompleto a um número inventado só pra fechar a semana.

Qual foi a última vez que você quase postou um resultado que, medido de verdade, não ia se sustentar?
