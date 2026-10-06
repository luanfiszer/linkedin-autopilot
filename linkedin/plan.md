# Plano da semana de 05/10 a 11/10/2026 (posts escritos em 06/10)

Pedido fora da rotina de segunda: o Luan rodou a coleta semanal (atrasada,
devia ter sido sexta 02/10) e pediu pra escrever os posts desta semana
corrente, não da próxima. Semana em andamento: segunda 05/10 a domingo
11/10. Como hoje já é terça 06/10, os 4 slots usam os dias úteis que
restam: terça a sexta.

Fontes: `linkedin/voice.md` e o diário técnico de `linkedin/ideias.md`
(coleta de 2026-10-05, a mais recente). Nenhum tema, gancho ou história
repete o que saiu publicado entre 25/09 e 04/10, nem os ganchos já usados
no plano da próxima semana (PR em aberto, branch `semana-2026-10-12`:
#16, #17, #18, #19).

| dia | horário | tipo | gancho | ângulo |
| --- | --- | --- | --- | --- |
| ter 06/10 | 09:20 | PROOF | #2 Number Reveal | Bug de tradução no professor virtual do projeto pessoal: o modelo respondia a perguntas em vez de traduzir. Corrigido delimitando o texto do usuário como material. Medido com Claude Haiku 4.5: 10/90 erros viraram 0/90. |
| qua 07/10 | 08:00 | TEACH | #8 Question Trap | Corrida (race condition) na renovação de refresh token: handler em 3 passos (ler, conferir, revogar) tinha uma janela. Corrigido com um UPDATE atômico e Web Locks API no navegador pra evitar renovação dupla entre abas. |
| qui 08/10 | 07:45 | STORY | #14 Pattern Interrupt | 653 testes verdes na main, mas um roteiro de QA contra a stack real achou cadastro quebrado e vazamento de dado entre alunos. Causa: o mundo dos testes tinha um usuário só. |
| sex 09/10 | 08:30 | OPINION | #7 The Callout | Regras de retenção (TTL) escritas e testadas, mas nenhum código de produção aplicava. Corrigido com um comando de operador idempotente e um boot-check que recusa subir se a config divergir. |

Nenhum dia repetido, nenhum tipo dois dias seguidos, 1 post por dia, todos
entre 7h30 e 9h30. O post de hoje (terça) ficou marcado pra 09:20 por causa
do horário em que a sessão rodou; se o PR não for revisado a tempo, ele sai
com atraso (comportamento esperado do publicador fora da janela da
madrugada).

## Imagens

Nenhuma foto real do Luan disponível em `media/fotos/` pra reaproveitar.
Os 4 saem com reserva gerada (2 infográficos em SVG, 1 cartão de código,
1 diagrama) e pedido de foto real em cada um.

## Engajamento

Fora do escopo desta rodada (só os posts, a pedido do Luan).
