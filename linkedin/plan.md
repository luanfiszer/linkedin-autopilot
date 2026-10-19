# Plano da semana de 26/10 a 01/11/2026

Gerado pela rotina semanal (skill `/li-plan`) em 19/10/2026 (segunda-feira).
Semana-alvo: segunda 26/10 a domingo 01/11 (a próxima semana completa a
partir de hoje).

Fontes usadas: `linkedin/voice.md` (posições, provas públicas) e o diário
técnico de `linkedin/ideias.md` (coletas de 25/09, 28/09 e 05/10/2026). A
seção "Esta semana" de `ideias.md` está vazia.

```
SEMANA DE 26/10

SEG  -
TER  08:15  PROOF    #12 The Comparison     - o sistema de tickets que fiz do zero na PROVER vs a ferramenta paga que ele substituiu
QUA  07:45  OPINION  #7  The Callout        - escrever a spec antes do código, mesmo numa correção que parece pequena
QUI  08:30  TEACH    #8  Question Trap      - progresso de usuário casado por identidade, não por posição
SEX  08:00  STORY    #14 Pattern Interrupt  - o desafio final de trainee: API REST com Clean Architecture apresentada ao vivo pra banca
SAB  -
DOM  -
```

## Detalhe de cada slot

1. **TER 27/10, 08:15 — PROOF — #12 The Comparison**
   Ângulo: na PROVER (emprego anterior ao atual, não é a MEDGRUPO), fiz do
   zero, em C# e ASP.NET MVC, um sistema interno de gestão de tickets que
   substituiu uma ferramenta paga. Custo operacional caiu 97,5%, sobrou só o
   custo de infraestrutura. Tinha autenticação, controle de acesso e
   histórico de atendimentos. Fato público de `voice.md` ("Provas que posso
   usar"). Nenhum `{{...}}` necessário.

2. **QUA 28/10, 07:45 — OPINION — #7 The Callout**
   Ângulo: nas correções maiores da semana (relato sanitizado, sem nome de
   sistema), escrevi proposta, design e spec (formato OpenSpec) antes de
   tocar no código — o que ia mudar, os casos de borda, o roteiro de
   validação em homologação. Foi assim, no papel, que um caso que ia quebrar
   apareceu antes de qualquer linha de código mudar. Posição: pular o design
   numa correção "pequena" é a parte mais cara de um bug maior. Apoiada
   também na ideia já registrada em `voice.md` ("não decidir arquitetura
   sobre código que ainda não existe"). Fonte: `ideias.md`, diário técnico de
   25/09 ("Spec antes do fix"). Sem `{{...}}`.

3. **QUI 29/10, 08:30 — TEACH — #8 Question Trap**
   Ângulo: quando o conteúdo de uma etapa era reconstruído, o progresso do
   usuário passava pro novo conteúdo sempre que havia exatamente um item
   antes e um depois — heurística de posição. Se o item tinha sido trocado,
   o usuário herdava progresso de algo que nunca fez; etapa vazia ainda
   contava. Correção: o progresso só passa adiante se o conjunto de ids for
   o mesmo (comparado ordenado). Lição ensinável: estado do usuário se casa
   por identidade, nunca por posição. Fonte: `ideias.md`, diário técnico de
   05/10 ("Progresso casado por posição, não por identidade"), já sanitizado
   (sem nome de sistema ou tabela). Sem `{{...}}`.

4. **SEX 30/10, 08:00 — STORY — #14 Pattern Interrupt**
   Ângulo: na seleção de trainee, passei por etapas eliminatórias (lógica,
   console, APIs) e o desafio final foi uma API REST de locadora de veículos
   com Clean Architecture, apresentada ao vivo para a banca. Fato público de
   `voice.md`. Nenhum `{{...}}` necessário.

## Observações sobre o mix e a não-repetição

- Mix: PROOF, OPINION, TEACH, STORY — um de cada, nenhum tipo repetido,
  nunca dois do mesmo tipo em sequência.
- Nenhum tema, gancho ou história repete o que já saiu em `queue/published/`
  ou no `log.md` (Outbox Pattern, N+1/LINQ, disciplina com agente de
  IA/ADR, `JsonExtensionData` round-trip, cache sem medição, idempotência
  Postgres vs Redis, bug de fuso `DateTimeOffset` — hooks #1, #9, #10, #11,
  #15, #20, #21). `queue/approved/` está vazio em `main`, então não há
  conflito de data com posts já agendados ali.
- Como complemento (não exigido pelo `CLAUDE.md`, mas evita repetição óbvia
  quando os PRs pendentes forem revisados): também evitei os temas e os
  ganchos já usados nos PRs #10, #11, #12 e #13 (ainda abertos, sem merge) —
  warm-up/k6, contrato de mensageria em bytes, 653 testes/1 aluno, soft
  delete com filtro global, fila de erro vazia, timestamp vs ordem de
  chegada, fallback que fecha por padrão, tradução delimitada por marcas,
  remendo que não toca o dado persistido, corrida de refresh token
  (ganchos #2, #3, #4, #5, #6, #16, #17, #18, #19). Esta semana usa #7, #8,
  #12 e #14, nenhum deles usado antes em post publicado ou em PR aberto.
- Horários só de manhã (7h30–9h30, America/Sao_Paulo), terça a sexta, no
  máximo 1 post por dia.
- Sem lista de engajamento: fora do escopo da rotina semanal deste
  repositório (`CLAUDE.md` só cobre os 4 posts).

## Ideias do diário técnico ainda não usadas (ficam pra depois)

- Documento derivado que também guarda estado (reconstrução zerava progresso).
- Revert antes de acertar (vínculo inferido por nome vira registro órfão).
- Correção manual de dados vira regra versionada (normalização + teste dbt).
- Provas de `voice.md` ainda não usadas: PROVER chat em legado (Long
  Polling/AJAX); microsserviços de autenticação do MEDGRUPO (JWT, MFA,
  geofencing, detecção de VPN, migração de hash — só no nível de conceito).
