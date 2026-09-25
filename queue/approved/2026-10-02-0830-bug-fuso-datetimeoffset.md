---
scheduled_at: 2026-10-02T08:30:00-03:00
visibility: PUBLIC
type: STORY
hook: "#9 Story Cold Open"
human_score: 71.4
---
"Isso não devia ser possível. Esse registro é de ontem."

Foi o que pensei olhando pro log, tentando entender por que uma consolidação mais antiga tinha acabado de sobrescrever a mais recente.

A regra do sistema era simples: entre 2 versões do mesmo dado, vence a mais recente. Só que "mais recente" dependia de comparar 2 valores de data lidos de uma coluna timestamptz no Postgres, e o driver, no modo legado de timestamps, devolvia esses valores no fuso do processo, não em UTC.

Nos testes locais, processo e banco rodavam no mesmo fuso. Nunca dava pra ver o problema. Só apareceu quando reproduzi num ambiente com fuso diferente: uma consolidação processada perto da virada do dia, e o mais novo virava mais velho na comparação.

Troquei os 2 lados pra DateTimeOffset, que carrega o fuso junto com o valor, e escrevi um teste de regressão com a data escrita explicitamente em -03:00, pra garantir que a comparação não dependesse de onde o processo está rodando.

O que ficou: uma regra de "vence o mais recente" e um tipo de data sem fuso não deviam conviver em nenhum sistema.

Já caçou um bug que só aparecia fora do seu ambiente de teste? O que finalmente entregou a causa?
