---
scheduled_at: 2026-11-27T08:00:00-03:00
visibility: PUBLIC
type: STORY
hook: "#4 Before/After"
human_score: 71.8
image: "media/fotos/gerado-warmup-concorrente-k6.png"
image_alt: "Infográfico: antes, warm-up sequencial aquece 1 conexão; depois, rajadas concorrentes aquecem o pool inteiro"
image_request: "Foto do seu setup (mesa, notebook, terminal) numa rodada de teste de carga, ou um rascunho seu comparando chamada sequencial com chamada em paralelo. Sem nada do trabalho na tela."
---
Até semana passada, o teste de carga do CI (pipeline de integração contínua) vivia estourando o p95, o tempo de resposta que fica entre os 5% mais lentos, sem padrão nenhum pra explicar. Eu rodava de novo e às vezes passava.

Hoje é estável. A diferença foi uma mudança só.

Antes do k6 (ferramenta que simula vários usuários ao mesmo tempo) começar a medir, meu warm-up chamava os endpoints um de cada vez, num foreach simples, esperando cada resposta antes de ir pro próximo.

Isso deixava só uma conexão do pool do Npgsql, o driver do PostgreSQL pro .NET, pronta antes da medição começar de verdade. Quando o k6 subia vários usuários virtuais de uma vez, o driver abria conexões novas no meio da própria medição, e cada conexão nova paga o preço de TCP, de TLS e de autenticação antes da primeira query rodar.

O endpoint que faz duas chamadas em paralelo por requisição, uma de contagem e outra de busca, sentia isso mais que os outros.

Eu corrigi assim: troquei o foreach por Task.WhenAll, disparando o warm-up em rajadas concorrentes contra os mesmos endpoints que o k6 mede, lidos do próprio catálogo do teste. Endpoint novo já entra aquecido, sem eu precisar lembrar de atualizar uma lista separada em outro arquivo.

Pus um SemaphoreSlim pra não estourar o limite do pool de uma vez, e um CancellationTokenSource com timeout de conexão e de duração em toda chamada.

Uma dependência que aceita a conexão e nunca responde travava a rodada inteira esperando ela sozinha.

Aquecer não é chamar uma vez pra garantir que funciona. É reproduzir a concorrência que vem depois, com o mesmo formato de carga.

Seu warm-up testa o mesmo nível de concorrência que a sua medição de verdade, ou só confirma que o sistema está de pé?
