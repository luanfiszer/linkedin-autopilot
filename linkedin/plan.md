# Plano da semana de 16/11 a 22/11/2026

Gerado pela rotina semanal (skill `/li-plan`) em 09/11/2026. Semana-alvo:
segunda 16/11 a domingo 22/11 (a próxima semana completa a partir de hoje,
09/11/2026, que também é segunda-feira).

## Aviso: estoque de ideias esgotado

`linkedin/ideias.md` não recebe uma coleta semanal nova desde **05/10/2026**
(mais de um mês). Todo item do diário técnico das coletas de 25/09, 28/09 e
05/10, e todas as "provas públicas" de `voice.md`, já foram usados em algum
post — publicado em `queue/published/` ou escrito em uma das **6 branches
ainda não mergeadas**: `semana-2026-10-05-posts`, `semana-2026-10-05-posts-v2`,
`semana-2026-10-12`, `semana-2026-10-19`, `semana-2026-10-26`,
`semana-2026-11-09` (PRs #10 a #15, todos abertos). Alguns itens (soft delete
com filtro global, corrida de refresh token) até se repetem entre essas
branches.

Para não empilhar mais uma repetição em cima dessas 6 PRs pendentes, este
plano:

- usa para OPINION e TEACH as duas ideias de `voice.md` → "Outras ideias que
  viram posts de TEACH" que **nenhuma das 6 branches nem nenhum post
  publicado usou ainda**: teste de adapter contra banco de verdade
  (testcontainers) e "não decidir arquitetura sobre código que ainda não
  existe";
- troca STORY por **OFFER** no quarto slot, porque OFFER não depende de um
  fato novo;
- deixa o slot de PROOF com fato pendente (`{{...}}`) em vez de repetir uma
  prova já usada ou inventar uma nova. Não há fato novo disponível em
  `ideias.md` nem em `voice.md`.

Fontes usadas: `linkedin/voice.md` (posições e "outras ideias" ainda não
usadas). A seção "Esta semana" de `ideias.md` está vazia.

```
SEMANA DE 16/11

SEG  -
TER  08:15  PROOF    #2  Number Reveal      - fato pendente: nenhuma prova nova disponível esta semana
QUA  08:00  OPINION  #18 The Unpopular Rule  - eu não decido arquitetura sobre código que ainda não existe
QUI  07:45  TEACH    #12 The Comparison      - banco em memória vs Testcontainers nos testes de adapter
SEX  08:30  OFFER    #14 Pattern Interrupt   - o que eu faço e que tipo de vaga/oportunidade eu busco
SAB  -
DOM  -
```

## Detalhe de cada slot

1. **TER 17/11, 08:15 — PROOF — #2 Number Reveal**
   Sem fato novo disponível: toda prova pública de `voice.md` e todo item do
   diário técnico de `ideias.md` já está em `queue/published/` ou numa das 6
   branches pendentes. O post sai com o resultado em `{{seu número}}` e o
   contexto em `{{o que você fez}}`, com a explicação no PR. Quando o Luan
   rodar "rodar coleta semanal" no Mac ou anotar algo em "Esta semana" de
   `ideias.md`, este slot pode ser preenchido direto no PR.

2. **QUA 18/11, 08:00 — OPINION — #18 The Unpopular Rule**
   Ângulo: "não decidir arquitetura sobre código que ainda não existe" —
   regra pessoal contra desenhar abstração para um caso hipotético. Fonte:
   `voice.md`, seção "Outras ideias", ainda não usada em post nenhum (nem
   publicado, nem nas 6 branches pendentes). Sem número interno, sem nome de
   empresa.

3. **QUI 19/11, 07:45 — TEACH — #12 The Comparison**
   Ângulo: testar um adapter contra um banco de verdade com Testcontainers em
   vez de banco em memória — o que o banco em memória deixa passar (SQL
   específico do driver, constraint, tipo de coluna). Fonte: `voice.md`,
   mesma seção, também inédita. Sem número interno, sem nome de empresa.

4. **SEX 20/11, 08:30 — OFFER — #14 Pattern Interrupt**
   Ângulo: dizer de forma direta o que o Luan faz (microsserviços ASP.NET
   Core: autenticação, mensageria, APIs; modernização de sistemas legados) e
   que tipo de oportunidade ele busca (vaga de backend .NET, de júnior a
   pleno). Base: `voice.md`, seção "Quem eu sou". Sem venda de serviço (o
   objetivo do perfil é vaga/autoridade, não oferta comercial), então o
   "offer" aqui é a disponibilidade dele mesmo, dita sem pedir desculpa.

Mix respeitado: PROOF, OPINION, TEACH, OFFER, um por dia, nunca dois do mesmo
tipo seguidos, máximo 1 post por dia, todos em horário de pico (terça a
sexta de manhã, dentro de 7h30-9h30 em America/Sao_Paulo).

Sem repetição de tema: nenhum dos quatro ângulos aparece em
`queue/published/`, em `log.md`, nem em nenhuma das 6 branches de PR ainda
abertas (verificado item a item contra `queue/approved/*.md` de cada uma).

Não há lista de engajamento nesta rotina (fora do escopo do `CLAUDE.md` deste
repositório — a rotina semanal só cobre posts).
