---
scheduled_at: 2026-10-07T08:30:00-03:00
visibility: PUBLIC
type: STORY
hook: "#9 Story Cold Open"
human_score: 70.1
---
Um dado antigo estava vencendo um dado novo. O culpado era o fuso horário.

A regra era simples: entre duas versões do mesmo registro, vence a mais recente.

Só que às vezes a versão antiga ganhava.

A causa estava num detalhe do driver do PostgreSQL no .NET: no modo legado de timestamps, um DateTime lido de uma coluna timestamptz voltava convertido pro fuso do processo, e não em UTC como eu esperava.

Na prática, a comparação dependia de onde o código rodava. O mais antigo podia parecer mais novo.

E o pior: nos testes locais, nunca apareceu. Só quando eu reproduzi num ambiente de verdade.

O que eu fiz:
- troquei DateTime por DateTimeOffset, que guarda o fuso junto com a data
- escrevi um teste de regressão com a data explícita em -03:00, pra esse bug não voltar escondido

Se a regra é "vence o mais recente", a data precisa saber em que fuso está.

Senão, "mais recente" vira questão de sorte.

Qual foi o bug mais difícil de reproduzir que você já pegou?
