---
scheduled_at: 2026-10-03T07:45:00-03:00
visibility: PUBLIC
type: TEACH
hook: "#11 Myth Bust"
human_score: 72.5
image_request: "Print do ADR em que você decidiu pôr a idempotência numa coluna do Postgres em vez do Redis (título + contexto). Recorte o nome do projeto e caminhos de pasta."
image: "media/fotos/gerado-idempotencia-fluxo.png"
image_alt: "Infográfico: reenvio com a mesma chave é recusado pelo índice UNIQUE no Postgres"
posted_urn: "urn:li:share:7512100474158874624"
posted_at: "2026-10-03T07:45:21-03:00"
posted_via: "rest/posts"
posted_image_urn: "urn:li:image:D4D10AQHxM-Jd5xe5Bg"
---
Idempotência com Redis parece resolvida. Até o processo cair no meio do caminho.

Estou construindo um projeto pessoal, um app de treino de inglês por conversa de áudio: você fala, o app transcreve, uma IA corrige e responde em voz. App em React Native, backend em Python, fila com worker sobre Redis.

Um caso bem real.

A rede do celular cai no meio do upload, o app reenvia o mesmo áudio, e aquela fala não pode ser processada duas vezes, porque cada processamento custa dinheiro de verdade.

O plano inicial era usar o SETNX do Redis como trava (um "grava só se ainda não existir").

Só que o próprio plano já apontava um risco: a janela entre criar o registro no Postgres e colocar o trabalho na fila. Se o processo cai bem ali, a trava do Redis não resolve.

Então mudei.

O app passou a mandar uma chave de idempotência num header, e ela foi pra uma coluna do próprio Postgres com índice UNIQUE, no mesmo registro que já ia pro banco. Criar o registro e reservar a chave viraram uma coisa só.

A regra que ficou pra mim:
- o banco é a fonte da verdade
- fila e cache aceleram, mas não decidem nada sozinhos

E no seu sistema, a idempotência mora no cache ou no banco?
