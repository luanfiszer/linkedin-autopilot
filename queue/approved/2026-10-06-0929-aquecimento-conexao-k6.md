---
scheduled_at: 2026-10-06T09:29:00-03:00
visibility: PUBLIC
type: PROOF
hook: "#4 Before / After"
human_score: 72.4
image: "media/fotos/gerado-warmup-concorrente.png"
image_alt: "Diagrama: warm-up sequencial deixa 1 conexão pronta, o k6 sobe carga em paralelo e paga TCP/TLS/auth no meio da medição; a correção faz o warm-up em rajadas concorrentes e todo endpoint já entra aquecido"
image_request: "Uma foto de um rascunho seu (caderno ou quadro) com duas réguas de tempo lado a lado: uma mostrando conexões abrindo uma de cada vez, outra mostrando todas juntas. Sem nada do trabalho."
---
Meu warm-up aquecia uma conexão. Hoje ele aquece todas que a carga real vai abrir.

O teste de carga no CI estourava o p95 de vez em quando. Sem padrão aparente.

O warm-up antes da medição chamava os endpoints um de cada vez, sequencial. Isso deixava só uma conexão do pool do Postgres pronta.

O k6 sobe vários usuários virtuais em paralelo. No meio da medição, o driver abria conexão nova: DNS, o Handshake do TCP, o Handshake do TLS, autenticação HTTP, até um Postgres numa região diferente.

O Endpoint que abre duas conexões por request, pra contagem e busca em paralelo, sofria o dobro.

A correção: warm-up virou rajadas concorrentes contra os mesmos Endpoints que o k6 mede, lidos do próprio catálogo do teste. Endpoint novo já entra aquecido.

Também pus timeout de conexão e de duração em toda chamada do warm-up. Uma dependência que aceita a conexão e não responde travava a rodada inteira esperando, sem timeout um warm-up travado parecia um teste de carga travado.

Aquecer é reproduzir a concorrência da medição. Não só chamar uma vez.

Warm-up sequencial deixa o pool do tamanho de um, não importa quantas conexões a carga real vai abrir.

Seu warm-up aquece na mesma concorrência que o teste depois vai usar, ou só confirma que o serviço responde?
