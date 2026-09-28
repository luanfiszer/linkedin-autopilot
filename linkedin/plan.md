# Plano da semana de 28/09 a 04/10/2026

Gerado pela rotina semanal (skill `/li-plan`) em 25/09/2026. Semana-alvo:
segunda 28/09 a domingo 04/10 (a próxima semana completa a partir de hoje).

Fontes usadas: `linkedin/voice.md` (posições e provas públicas) e o diário
técnico de `linkedin/ideias.md` (coleta de 25/09/2026). A seção "Esta semana"
de `ideias.md` estava vazia.

```
SEMANA DE 28/09

SEG  -
TER  08:15  PROOF    #12 The Comparison     - o sistema de tickets da PROVER vs a ferramenta paga que ele substituiu
QUA  08:00  OPINION  #1  Contrarian Take    - Outbox não é exagero: publicar evento logo após salvar no banco é bug esperando acontecer
QUI  07:45  TEACH    #11 Myth Bust          - Redis não resolve idempotência sozinho: banco como fonte da verdade, fila/cache como aceleradores
SEX  08:30  STORY    #9  Story Cold Open    - o registro "mais recente" que na verdade era o mais antigo (bug de fuso com DateTimeOffset)
SAB  -
DOM  -
```

## Detalhe de cada slot

1. **TER 29/09, 08:15 — PROOF — #12 The Comparison**
   Ângulo: o sistema de gestão de tickets que fiz do zero na PROVER (C#,
   ASP.NET MVC) substituiu uma ferramenta paga. Custo operacional caiu 97,5%,
   sobrou só infraestrutura. Fato público de `voice.md` (seção "Provas que
   posso usar"), não é da MEDGRUPO. Nenhum `{{...}}` necessário.

2. **QUA 30/09, 08:00 — OPINION — #1 Contrarian Take**
   Ângulo: publicar evento logo depois de salvar no banco é bug esperando
   acontecer; Outbox Pattern não é over-engineering. Base: posição #2 de
   `voice.md`, apoiada no formato já autorizado ali ("implementei Outbox
   Pattern num consumer RabbitMQ; evento perdia quando o banco confirmava e a
   publicação falhava"). Sem nome de empresa, sem número interno.

3. **QUI 01/10, 07:45 — TEACH — #11 Myth Bust**
   Ângulo: uma das "outras ideias" listadas em `voice.md` — idempotência numa
   coluna do Postgres em vez de Redis `SETNX`, motivada por uma janela de
   crash entre criar o registro e enfileirar. Fonte: história do projeto
   pessoal (app de treino de inglês, sem citar o nome), que `voice.md`
   autoriza usar com números e detalhes. Trocado no lugar do item do diário
   técnico sobre `JsonExtensionData` porque este último não tinha material
   concreto suficiente (números/nomes públicos) para passar no `detect.py`
   sem enfraquecer o texto.

4. **SEX 02/10, 08:30 — STORY — #9 Story Cold Open**
   Ângulo: item do diário técnico — bug de fuso com o modo legado de
   timestamps do driver do PostgreSQL: um `DateTime` voltava no fuso do
   processo, uma consolidação mais antiga parecia mais nova e sobrescrevia a
   certa. Só apareceu num ambiente real, nunca nos testes locais. Correção:
   trocar para `DateTimeOffset` e teste de regressão com data em -03:00.
   Sanitizado, sem nome de sistema ou número interno.

Mix respeitado: PROOF, OPINION, TEACH e STORY, um por dia, nunca dois do
mesmo tipo seguidos, máximo 1 post por dia, todos em horário de pico
(terça a quinta) exceto o quarto, que foi para sexta de manhã (segunda opção
da skill) para fechar com STORY sem cair no fim de semana.

Sem repetição de tema: não há posts publicados de verdade ainda (só um post
de teste em `queue/published/`), e `queue/approved/` está vazio.

Não há lista de engajamento nesta rotina (fora do escopo do CLAUDE.md deste
repositório — a rotina semanal só cobre posts).
