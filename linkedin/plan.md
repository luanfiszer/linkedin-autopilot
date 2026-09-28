# Plano da semana de 05/10 a 11/10/2026

Gerado pela rotina semanal (skill `/li-plan`) em 28/09/2026. Semana-alvo:
segunda 05/10 a domingo 11/10 (a próxima semana completa a partir de hoje,
28/09, que também é segunda-feira).

Fontes usadas: `linkedin/voice.md` (posições e provas públicas) e o diário
técnico de `linkedin/ideias.md` (coleta de 25/09/2026). A seção "Esta semana"
de `ideias.md` estava vazia. `queue/approved/` (semana de 28/09) foi revisado
para não repetir tema, gancho ou história.

```
SEMANA DE 05/10

SEG  -
TER  08:15  PROOF     #10 The Receipt        - refatoração de queries N+1 na PROVER: latência caiu 15%
QUA  08:00  OPINION   #15 The Warning        - confiar na memória do agente de IA custa caro; decisão tem que virar ADR
QUI  07:45  TEACH     #21 Direct Value       - JsonExtensionData: como não perder campo em JSON reescrito por dois processos
SEX  08:30  STORY     #20 The Walk-Away      - a otimização de cache que aprovei e derrubei no mesmo dia
SAB  -
DOM  -
```

## Detalhe de cada slot

1. **TER 06/10, 08:15 — PROOF — #10 The Receipt**
   Ângulo: na PROVER, refatorei consultas críticas no SQL Server (EF Core e
   LINQ), eliminei N+1 e a latência das requisições caiu 15%. Fato público de
   `voice.md` (seção "Provas que posso usar"), não é da MEDGRUPO, diferente do
   PROOF da semana passada (sistema de tickets). Nenhum `{{...}}` necessário.

2. **QUA 07/10, 08:00 — OPINION — #15 The Warning**
   Ângulo: posição #1 de `voice.md` — programar com agente de IA exige mais
   disciplina, não menos, porque o agente não lembra o que foi combinado na
   sessão anterior. Decisão tem que estar escrita (ADR), regra de arquitetura
   tem que quebrar o build, comportamento tem que ter teste. Base: projeto
   pessoal construído sessão a sessão com agente, com dezenas de ADRs e um
   registro de aprendizados (sem citar o nome do projeto). Diferente da
   posição de Outbox usada semana passada. Nenhum `{{...}}` necessário.

3. **QUI 08/10, 07:45 — TEACH — #21 Direct Value**
   Ângulo: item do diário técnico — desserialização tipada apaga dados em
   silêncio. Com dois processos escrevendo o mesmo JSON, ler para uma classe
   e regravar descarta toda chave que a classe não declara. Resolvido com
   `JsonExtensionData` do .NET nos níveis que são regravados. Lição: todo
   read-modify-write de documento compartilhado precisa preservar o que não
   conhece. Já sanitizado no diário técnico (sem nome de sistema, tabela ou
   número interno). Diferente do TEACH de idempotência usado semana passada.

4. **SEX 09/10, 08:30 — STORY — #20 The Walk-Away**
   Ângulo: posição #3 de `voice.md` — otimização sem medição é chute. No
   projeto pessoal, aprovei uma otimização de prompt caching e derrubei no
   mesmo dia: a medição mostrou que o prefixo mínimo pra cache engatar era
   4.096 tokens, não os 1.024 que eu tinha assumido, e uma conversa real nunca
   chegava lá. Números já autorizados em `voice.md` (sem citar o nome do
   projeto). Diferente da história de bug de fuso usada semana passada.

Mix respeitado: PROOF, OPINION, TEACH e STORY, um por dia, nunca dois do
mesmo tipo seguidos, máximo 1 post por dia, três em horário de pico (terça a
quinta) e o quarto na sexta de manhã (segunda opção da skill), igual ao
padrão da semana anterior. Nenhum gancho repete o da semana de 28/09
(#12, #1, #11, #9 não reaparecem aqui).

Sem repetição de tema: nenhum dos quatro ângulos acima repete tema, gancho ou
história dos posts já aprovados/publicados (`queue/approved/` da semana de
28/09 e `queue/published/`).

Não há lista de engajamento nesta rotina (fora do escopo do CLAUDE.md deste
repositório — a rotina semanal só cobre posts).
