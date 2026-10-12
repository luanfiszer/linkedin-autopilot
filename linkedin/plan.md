# Plano da semana de 19/10 a 25/10/2026

Gerado pela rotina semanal (skill `/li-plan`) em 12/10/2026. Semana-alvo:
segunda 19/10 a domingo 25/10 (a próxima semana completa a partir de hoje,
12/10/2026, que é segunda-feira).

Fontes usadas: `linkedin/voice.md` (posições e provas públicas) e o diário
técnico de `linkedin/ideias.md` (coletas de 25/09, 28/09 e 05/10/2026). A
seção "Esta semana" de `ideias.md` estava vazia.

```
SEMANA DE 19/10

SEG  -
TER  08:15  PROOF    #2  Number Reveal      - o prompt do tradutor testado em 90 execuções: 10 erros antes, 0 depois
QUA  07:45  OPINION  #18 Unpopular Rule     - remendo temporário não pode contaminar o dado persistido
QUI  08:30  TEACH    #16 Good vs Great      - soft delete é um contrato; filtro global em vez de lembrar em cada consulta
SEX  07:45  STORY    #19 Curiosity Gap      - o bug de corrida que só apareceu rodando dois comandos iguais ao mesmo tempo
SAB  -
DOM  -
```

## Detalhe de cada slot

1. **TER 20/10, 08:15 — PROOF — #2 Number Reveal**
   Ângulo: no botão de tradução do projeto pessoal (app de inglês, sem citar
   o nome), o modelo às vezes respondia à pergunta do professor virtual em
   vez de traduzir. Medi em 90 execuções: o prompt antigo errou 10 (11%); a
   correção (delimitar o texto e tratar o conteúdo delimitado como dado, não
   instrução) zerou os erros nas 90 novas. As duas rodadas custaram US$ 0,063
   juntas. O adaptador ganhou 7 testes, 3 deles falham na versão antiga.
   Fonte: `ideias.md`, diário técnico de 05/10 ("A tradução que respondia em
   vez de traduzir"). Números reais, medidos, do projeto pessoal — `voice.md`
   autoriza usar números dele. Nenhum `{{...}}` necessário.

2. **QUA 21/10, 07:45 — OPINION — #18 Unpopular Rule**
   Ângulo: uma correção redundante enquanto um serviço upstream corrigia um
   veredito inconsistente. A posição: remendo temporário não pode contaminar
   o dado persistido — grava-se só o dado de entrada e a regra se aplica na
   leitura; se tirar o remendo depois exige migração, ele nunca foi
   temporário. Fonte: `ideias.md`, diário técnico de 28/09 ("Gambiarra
   provisória desenhada para ser apagada"), já sanitizado (sem nome de
   sistema, sem número interno, trata só da técnica e da decisão). Sem
   `{{...}}`.

3. **QUI 22/10, 08:30 — TEACH — #16 Good vs Great**
   Ângulo: soft delete que a entidade não conhecia — um registro excluído na
   origem continuava aparecendo porque o mapeamento não declarava a coluna de
   exclusão. A lição ensinável: tratar soft delete como contrato, com filtro
   global de consulta (EF Core `HasQueryFilter`) por padrão e
   `IgnoreQueryFilters` só onde precisa ver o excluído, em vez de confiar que
   cada consulta vai lembrar de filtrar. Fonte: `ideias.md`, diário técnico de
   05/10 ("Soft delete que a entidade não conhecia"), sanitizado (sem nome de
   tabela ou sistema). Sem `{{...}}`.

4. **SEX 23/10, 07:45 — STORY — #19 Curiosity Gap**
   Ângulo: ao desenhar a sessão da versão web do projeto pessoal, rodei dois
   `curl` em paralelo pedindo refresh com o mesmo token — os dois receberam
   token novo. Causa: o handler lia, conferia revogação e só depois revogava
   (check-then-act), uma corrida clássica. Correção: um único
   `UPDATE ... WHERE revoked_at IS NULL RETURNING id` atômico, cookie
   `HttpOnly`/`SameSite=Strict` e só uma aba renovando por vez via Web Locks
   API (`navigator.locks`). Fonte: `ideias.md`, diário técnico de 05/10
   ("Duas abas renovando o token ao mesmo tempo"), projeto pessoal. Sem
   `{{...}}`.

## Observações sobre o mix e a não-repetição

- Mix: PROOF, OPINION, TEACH, STORY — um de cada, nenhum tipo repetido, nunca
  dois do mesmo tipo em sequência.
- Nenhum tema, gancho ou história repete o que já saiu em `queue/published/`
  nas últimas duas semanas (Outbox Pattern, N+1/LINQ, disciplina com agente
  de IA/ADR, `JsonExtensionData` round-trip, cache sem medição, idempotência
  Postgres vs Redis, bug de fuso `DateTimeOffset`). Ganchos já usados nesse
  período (#1, #9, #10, #11, #15, #20, #21) foram evitados; esta semana usa
  #2, #16, #18 e #19, nenhum repetido antes.
  `queue/approved/` está vazio, então não há conflito de data com posts já
  agendados.
- Horários só de manhã (7h30–9h30, America/Sao_Paulo), terça a quinta na
  preferência e sexta como segunda opção, no máximo 1 post por dia, como
  exige o `CLAUDE.md` deste repositório (o fuso do público é o mesmo do
  usuário).
- Sem lista de engajamento: fora do escopo da rotina semanal deste
  repositório (`CLAUDE.md` só cobre os 4 posts).
