---
scheduled_at: 2026-11-19T07:45:00-03:00
visibility: PUBLIC
type: TEACH                 # PROOF | OPINION | TEACH | STORY | OFFER
hook: "#12 The Comparison"
human_score: 78.4
image: "media/fotos/gerado-teste-adapter-testcontainers.png"
image_alt: "Cartão de código: teste com banco em memória deixa passar um UNIQUE que o Testcontainers com Postgres real recusa"
image_request: "Print do terminal do seu projeto pessoal com a suíte de testes rodando contra o Testcontainers. Esconda o nome do projeto e os caminhos de pasta."
---
Banco em memória vs Testcontainers nos testes de adapter. O mais lento venceu.

Teste com banco em memória roda rápido. Rápido, mas errado.

Ele aceita um UPDATE que o Postgres rejeitaria, não aplica a constraint UNIQUE do jeito certo, e não reclama de um tipo de coluna que o Npgsql trata diferente do provider em memória.

Com Testcontainers, cada suíte sobe um container de Postgres de verdade, roda a migration de verdade, e o adapter conversa com o mesmo banco que vai pra produção.

Fica mais lento, alguns segundos por suíte. Mas pegou SQL que só quebrava no banco real, antes de chegar em homologação.

A regra que eu sigo: teste de adapter não é unidade, é integração. Fingir que o banco não existe só empurra o bug pra mais tarde.

Você testa seus adapters contra o banco de verdade, ou confia no banco em memória?
