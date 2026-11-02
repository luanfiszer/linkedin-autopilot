# Plano da semana de 09/11 a 15/11/2026

Gerado pela rotina semanal (skill `/li-plan`) em 02/11/2026 (segunda-feira).
Semana-alvo: segunda 09/11 a domingo 15/11 (a próxima semana completa a
partir de hoje).

Fontes usadas: `linkedin/voice.md` (posições e provas públicas) e o diário
técnico de `linkedin/ideias.md` (coletas de 25/09, 28/09 e 05/10/2026 — não
há coleta mais recente; a "coleta semanal" roda só no Mac do Luan e não foi
executada desde 05/10). A seção "Esta semana" de `ideias.md` está vazia.

```
SEMANA DE 09/11

SEG  -
TER  08:15  PROOF    #12 The Comparison     - chat em tempo real num legado sem WebSocket, com Long Polling e AJAX, vs esperar a stack toda mudar
QUA  07:45  OPINION  #15 The Warning        - achar o registro certo por heurística de nome custa um registro órfão que ainda não apareceu
QUI  08:30  TEACH    #16 Good vs Great      - correção manual de dado divergente vira regra versionada (dbt), não um UPDATE isolado
SEX  08:00  STORY    #14 Pattern Interrupt  - o processo que existia pra nunca perder progresso foi o que mais perdeu progresso essa semana
SAB  -
DOM  -
```

## Detalhe de cada slot

1. **TER 10/11, 08:15 — PROOF — #12 The Comparison**
   Ângulo: na PROVER (emprego anterior à MEDGRUPO, fato público autorizado em
   `voice.md`), fiz chat em tempo real com Long Polling e AJAX num ambiente
   legado sem suporte a WebSocket. Comparação: reescrever a stack pra suportar
   WebSocket de verdade vs entregar tempo real com o que já tinha no ar.
   Fonte: `voice.md`, seção "Provas que posso usar". Nenhum `{{...}}`
   necessário.

2. **QUA 11/11, 07:45 — OPINION — #15 The Warning**
   Ângulo: um fix que tentava "migrar" um vínculo existente quando o
   agrupamento do usuário mudava foi revertido no mesmo dia; a versão final
   modelou o vínculo explicitamente numa tabela de relação, com migration
   idempotente e backfill, em vez de achar o registro por heurística de nome.
   Posição: identidade inferida por nome vira registro órfão cedo ou tarde.
   Fonte: `ideias.md`, diário técnico de 25/09 ("Revert antes de acertar"),
   já sanitizado (sem nome de sistema, sem número interno). Sem `{{...}}`.

3. **QUI 12/11, 08:30 — TEACH — #16 Good vs Great**
   Ângulo: um UPDATE feito à mão pra preencher caminho de arquivo divergia da
   planilha de referência em muitas linhas (encoding de barra, barra dupla,
   extensão que nem devia ter caminho). Correção: as regras da planilha
   viraram um model dbt com normalização antes da comparação e um teste
   `not_null`; depois simplifiquei (a macro só tinha um uso) e conferi que o
   resultado era idêntico linha a linha antes de trocar. Lição ensinável:
   correção manual que não vira regra testada se repete pra sempre. Fonte:
   `ideias.md`, diário técnico de 25/09 ("Correção manual de dados vira regra
   versionada"), sanitizado (sem nome de tabela, sistema ou planilha). Sem
   `{{...}}`.

4. **SEX 13/11, 08:00 — STORY — #14 Pattern Interrupt**
   Ângulo: um processo noturno reconstruía do zero um documento desnormalizado
   a partir da fonte, mas parte do estado (o progresso do usuário) só existia
   nesse documento. Resultado: o progresso zerava toda madrugada, e outra
   rotina usava esse valor como "memória" pra nunca regredir — então a
   regressão vazava pra outras tabelas. Correção: mesclar o estado anterior no
   documento novo, casando por id com fallback por nome. Lição: "é só
   reconstruir da fonte" só vale se o documento for 100% derivado. Fonte:
   `ideias.md`, diário técnico de 25/09 ("Documento derivado que também
   guarda estado"), sanitizado. Sem `{{...}}`.

## Observações sobre o mix e a não-repetição

- Mix: PROOF, OPINION, TEACH, STORY — um de cada, nenhum tipo repetido, nunca
  dois do mesmo tipo em sequência.
- Nenhum tema, gancho ou história repete o que está em `queue/published/` ou
  em `linkedin/log.md` (Outbox Pattern, N+1/LINQ, disciplina com agente de
  IA/ADR, `JsonExtensionData` round-trip, cache sem medição, idempotência
  Postgres vs Redis, bug de fuso `DateTimeOffset`). `queue/approved/` está
  vazio em `main`, então não há conflito de data com posts já agendados ali.
- **Atenção (achado, não exigido pelo `CLAUDE.md`, mas relevante):** há 5
  Pull Requests abertos e sem merge há semanas — #10 (semana de 12/10), #11 e
  #12 (duas versões da semana de 05/10), #13 (semana de 19/10) e #14 (semana
  de 26/10) — nenhum deles publicado. Por isso `queue/published/` não tem
  nada depois de 04/10, embora hoje seja 02/11. Como complemento, também
  evitei repetir os temas e ganchos já usados nesses PRs pendentes (warm-up/
  k6, contrato de mensageria em bytes, 653 testes/1 aluno, soft delete com
  filtro global — usado duas vezes entre eles —, JOIN com JSON grande,
  fallback que fecha por padrão, timestamp vs ordem de chegada, fila de erro
  vazia, tradutor com delimitador de prompt, remendo que não toca o dado
  persistido, corrida de refresh token, ticket system da PROVER, spec antes
  do código, progresso por identidade, desafio de trainee com Clean
  Architecture). Esta semana usa só ideias que nenhum PR pendente usou ainda.
  Isso é só pra qualidade; os PRs antigos continuam valendo e cabe ao usuário
  decidir se revisa, atualiza ou fecha cada um.
- Horários só de manhã (7h30–9h30, America/Sao_Paulo), terça a quinta de
  preferência, sexta como segunda opção, no máximo 1 post por dia.
- Sem lista de engajamento: fora do escopo da rotina semanal deste
  repositório (`CLAUDE.md` só cobre os 4 posts).

## Ideias do diário técnico ainda não usadas em nenhum PR (ficam pra depois)

- `[pessoal]` A política de retenção que nenhum código chamava (coleta de
  05/10) — regra de expiração escrita e testada, mas que nenhum código de
  produção aplicava.
- Provas de `voice.md` ainda não usadas em nenhum post: microsserviços de
  autenticação do MEDGRUPO (JWT, MFA via QR Code, geofencing, detecção de
  VPN, migração de hash — só no nível de conceito, sem citar a empresa).
- Vale avisar o usuário, na descrição do PR, sobre o backlog de PRs abertos
  acima — isso trava a publicação há quase um mês.
