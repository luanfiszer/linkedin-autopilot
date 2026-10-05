---
scheduled_at: 2026-10-16T08:30:00-03:00
visibility: PUBLIC
type: STORY
hook: "#19 Curiosity Gap"
human_score: 74.3
image: "media/fotos/gerado-fila-erro-vazia.png"
image_alt: "Infográfico: do lado do que quebra, a classe base captura a exceção e o trace marca sucesso sem a fila de erro receber nada; do lado da correção, a exceção sobe e a biblioteca publica na dead-letter"
image_request: "Print do terminal do seu projeto pessoal com um teste de caminho de falha passando (ex.: uma exceção sendo capturada e logada). Sem nome de projeto ou caminho de pasta visível."
---
A fila de erro mais bem configurada que eu já vi nunca recebeu uma mensagem.

Isso devia ser bom sinal. Não era.

O consumer de uma fila RabbitMQ tinha a Dead-Letter certinha, do jeito que o manual recomenda. Olhei o histórico. Vazia desde que foi criada.

Fui ver o motivo. A causa estava na classe base que todo Consumer dali herdava, uma espécie de ConsumerBase: o HandleAsync dela capturava qualquer exceção e chamava BasicNack com requeue desligado, como se fosse um retorno normal.

O RabbitMQ fala AMQP, e nack com requeue desligado não é a mesma coisa que mandar pra Dead-Letter. A biblioteca só faz isso quando o handler deixa a exceção subir até ela. Como a ConsumerBase sempre capturava antes disso, a mensagem que falhava era descartada em silêncio. E o Trace ainda marcava aquela execução como sucesso.

Uma Dead-Letter vazia não prova que nada falha. Só prova que, se algo falhar, ninguém vai saber por ali.

O que fiz: documentei esse comportamento no design, separei a reconstrução do retry num item de trabalho próprio e deixei um alerta de falha de consumo como parte da entrega, não como um "depois a gente vê".

Testar o caminho feliz garante que a Dead-Letter existe. Só testar o caminho de falha de ponta a ponta garante que ela recebe algo.

Você já conferiu se a sua fila de erro recebe mensagem de verdade, ou só confiou que ela ia funcionar?
