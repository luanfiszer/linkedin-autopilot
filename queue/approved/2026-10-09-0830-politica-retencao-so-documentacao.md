---
scheduled_at: 2026-10-09T08:30:00-03:00
visibility: PUBLIC
type: OPINION
hook: "#7 The Callout"
human_score: 70.6
image: "media/fotos/gerado-retencao-so-documentacao.png"
image_alt: "Infográfico: de um lado, uma regra de retenção escrita e testada que nenhum código aplica e grava pra sempre sem erro; do outro, um comando de operador idempotente e um worker que recusa subir quando a configuração diverge"
image_request: "Uma foto de um rascunho seu (caderno ou quadro) com um fluxo de boot-check: uma caixa de decisão perguntando 'config bate?' com um X vermelho de um lado e um check verde do outro. Sem nada do trabalho."
---
Se a sua política de retenção de dados pode ficar desligada sem nenhum erro, você não tem uma política. Tem uma sugestão.

No meu projeto pessoal, as regras de TTL do bucket de áudio estavam escritas e testadas havia semanas.

Nenhum código de produção as aplicava.

No ambiente local, a configuração de Lifecycle do bucket nem existia: a voz gravada ficava guardada pra sempre, sem erro nenhum. Como o app ainda não tem usuário real, nada reclamava. A API ainda assinava URL de áudio já expirado, que virava 404 no player.

Função testada que ninguém chama é só documentação.

Eu não quis aplicar as regras direto no boot do Worker, porque isso exigiria dar à credencial do app uma permissão IAM de administrar o bucket pra sempre, só pra um comando raro.

Então aplicar virou um comando de operador. Manual, por CLI, idempotente, que lê de volta o que acabou de aplicar.

A parte que importa é o que acontece quando ninguém roda esse comando.

O Worker confere as regras de TTL no boot: ausente, ou diferente da Config esperada, ele recusa subir, e a mensagem de erro já diz qual comando rodar. A API passou a calcular a expiração pela data de criação, sem consultar o bucket.

Configuração não é política. É intenção.

Virou regra quando passou a derrubar o serviço na cara de quem esqueceu de aplicar.

A sua política de retenção falha alto quando está ausente, ou só fica documentada esperando alguém lembrar?
