---
scheduled_at: 2026-09-30T11:00:00-03:00
visibility: PUBLIC
type: OPINION
hook: "#15 The Warning"
human_score: 79.2
image: "media/fotos/gerado-agente-ia-adr-infografico.png"
image_alt: "Infográfico: regra só na cabeça é desfeita pela próxima sessão; ADR, checagem no build e teste resolvem"
---
Confiar na memória do agente de IA está te custando retrabalho que você nem percebe.

Uso agente de IA sessão a sessão num projeto pessoal meu: um app de treino de idioma por conversa de áudio, com backend em Python, banco Postgres e fila sobre Redis. O app mobile é em React Native.

Isso virou o oposto do que boa parte do meu feed repete.

O agente não lembra o que foi combinado ontem. Ponto.

Cada sessão nova enxerga só o código. Não enxerga o raciocínio por trás dele.

Se uma regra de arquitetura mora só na minha cabeça, ela erode: uma sessão futura, sem saber do combinado, desfaz o que a anterior decidiu.

Três coisas mudaram, na prática:

- decisão de arquitetura vira ADR (Architecture Decision Record: documento curto com o contexto e o porquê, não só o quê)
- regra que não pode quebrar vira uma checagem que derruba o build
- comportamento importante vira teste automatizado, nunca comentário

Hoje tenho dezenas de ADRs registrados nesse projeto, e cada decisão que muda depois vira uma entrada no registro de aprendizados, não uma correção silenciosa no código.

Cada um poupa uma sessão inteira de refazer uma discussão que o agente já esqueceu.

Programar com agente de IA não pede menos disciplina.

Pede mais.

Quem lembra agora é o documento. Não a pessoa.

Você registra as decisões do seu projeto nalgum lugar que o próximo (você mesmo, um agente, ou um colega) consegue ler sem te perguntar?
