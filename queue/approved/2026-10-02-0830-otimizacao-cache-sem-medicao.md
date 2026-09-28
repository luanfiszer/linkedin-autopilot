---
scheduled_at: 2026-10-02T08:30:00-03:00
visibility: PUBLIC
type: STORY
hook: "#20 The Walk-Away"
human_score: 71.9
---
Eu aprovei uma otimização de cache e derrubei ela no mesmo dia.

Estou construindo um projeto pessoal: um app de treino de idioma por conversa de áudio com um professor de IA. Backend em Python, banco Postgres, app mobile em React Native.

O backend chama um LLM a cada resposta. Ele fica atrás de uma fila com worker, sobre Redis, e a resposta volta em áudio por SSE.

Cada chamada carrega um prefixo fixo no prompt, sempre igual entre as chamadas.

Prefixo repetido é candidato natural a prompt caching: a API do modelo cobra menos e responde mais rápido quando reconhece o mesmo início de prompt numa chamada seguinte.

Implementei. Subi. Assumi que já estava economizando.

Antes de comemorar, fui medir.

O prefixo mínimo pra esse cache engatar de verdade era 4.096 tokens. Eu tinha assumido, sem checar, que bastavam 1.024, e uma conversa real do app nunca chegava nem perto disso.

Uma peça a mais no sistema, pra economizar um valor que nunca acontecia.

Derrubei a otimização no mesmo dia, assim que o número apareceu na medição.

Custou uma tarde de trabalho, bem menos do que manter uma peça inútil rodando por meses achando que ela estava ajudando.

Otimização sem medição é chute. A minha só teve a sorte de ser desfeita rápido.

Você já teve que desfazer uma otimização no mesmo dia em que aprovou? O que a medição mostrou?
