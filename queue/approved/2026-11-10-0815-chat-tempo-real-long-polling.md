---
scheduled_at: 2026-11-10T08:15:00-03:00
visibility: PUBLIC
type: PROOF
hook: "#12 The Comparison"
human_score: 72.9
image: "media/fotos/gerado-long-polling-ajax.png"
image_alt: "Diagrama: cliente abre requisição HTTP, servidor espera mensagem ou timeout, responde, e o cliente já abre a próxima"
image_request: "Foto de um rascunho seu, à mão, desenhando o ciclo de uma requisição HTTP que fica esperando a resposta (Long Polling). Sem nada do trabalho atual."
---
Long Polling com AJAX virou tempo real num sistema que nunca teve WebSocket.

Isso foi na PROVER, antes da empresa onde trabalho hoje.

Fiz um chat em tempo real num ambiente legado sem suporte a WebSocket.

Sem WebSocket.

Long Polling funciona assim: o navegador abre uma requisição HTTP, o servidor some com a resposta até chegar mensagem nova ou vencer um tempo limite, e no instante que ela volta o cliente já abre a próxima.

AJAX fazia essa troca, sem recarregar a página.

Não é uma conexão permanente, como WebSocket mantém. É uma fila curta de requisições HTTP, uma atrás da outra, de novo e de novo.

Pra quem usava o chat, a mensagem chegava quase na hora.

A diferença entre as duas técnicas ficava só do lado de quem escreveu o código, nunca do lado de quem digitava e esperava a resposta aparecer na tela.

Tempo real não é sinônimo de WebSocket.

É não deixar o cliente esperando a próxima resposta por muito tempo.

Você já resolveu uma necessidade de tempo real sem poder trocar a infraestrutura por baixo?

#DotNet #Arquitetura