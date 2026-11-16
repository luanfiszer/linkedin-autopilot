# Plano da semana — 23/11 a 29/11 (segunda a domingo)

Gerado pela rotina semanal em 2026-11-16. Semana-alvo: a que começa na
próxima segunda-feira depois de hoje.

> **Atenção:** há 5 PRs de semanas anteriores ainda abertos, sem merge, desde
> 04/10 (#10, #13, #14, #15, #16). Nenhum post novo foi publicado desde então.
> Os temas abaixo foram escolhidos para não repetir nada do que já está
> escrito nesses PRs pendentes nem no que já foi publicado.

```
SEMANA DE 23/11

SEG  só engajar (20 min, lista abaixo)
TER 24/11  8:15   PROOF    #10 The Receipt     - 653 testes verdes no projeto pessoal, 2 bugs reais de autorização que um roteiro de QA achou em minutos
QUA  só engajar
QUA 25/11  7:45   OPINION  #1  Contrarian Take - migrar hash de senha legado sem forçar reset geral: re-hash no login, devagar
QUI 26/11  8:30   TEACH    #5  The List Promise - 3 coisas que um teste de contrato de mensageria pelos bytes pegou que um objeto montado à mão nunca pegaria
SEX 27/11  8:00   STORY    #4  Before/After     - teste de carga com p95 instável; antes, warm-up sequencial aquecia 1 conexão; depois, rajadas concorrentes contra o catálogo real de endpoints
SAB  -
DOM  -
```

## Detalhe de cada slot

### TER 24/11, 08:15 — PROOF — #10 The Receipt
**Fonte:** `linkedin/ideias.md`, "Diário técnico (coleta de 2026-10-05)",
item "[pessoal] CI verde, 653 testes, e o cadastro não funcionava".
**Ângulo:** no projeto pessoal, um loop de agente fechava cards com gates
verdes (lint, tipos, cobertura, 653 testes). Um roteiro de QA manual contra a
stack real, com 31 verificações, achou em minutos 2 defeitos que a suíte
nunca pegou: cadastro por e-mail falhando em silêncio (ordem de insert
ORM/FK) e 4 rotas que vazavam dado de um aluno pro outro com token inválido.
A causa: as fixtures de teste só tinham 1 aluno, então autorização nunca era
exercitada. **Números reais a usar:** 653, 31, 2, 4. Não inventar nenhum
outro número.

### QUA 25/11, 07:45 — OPINION — #1 Contrarian Take
**Fonte:** `linkedin/voice.md`, "Provas que posso usar" (MEDGRUPO, sem
números): "migração de hashes legados para criptografia moderna", só no
nível de conceito.
**Ângulo:** a crença comum é que trocar o algoritmo de hash de senha exige
forçar reset de senha de todo mundo de uma vez. Posição contrária: dá pra
migrar sem isso, re-hash no login (quando a senha certa chega em texto
puro, você já tem a chance de regravar com o algoritmo novo). Fica só no
conceito, sem citar a empresa, sem detalhe de como a proteção funciona por
dentro.

### QUI 26/11, 08:30 — TEACH — #5 The List Promise
**Fonte:** `linkedin/ideias.md`, "Diário técnico (coleta de 2026-10-05)",
item "[trabalho] Contrato de mensageria testado nos bytes".
**Ângulo:** um campo novo passou a viajar numa mensagem entre serviços.
Testar com um objeto montado à mão não teria pego os problemas reais. As 3
coisas que o teste pelos bytes (serializando/desserializando de verdade,
pelo pipeline real) pegou: campo presente, campo ausente (mensagem antiga)
e revogação chegando depois sobre o mesmo registro.

### SEX 27/11, 08:00 — STORY — #4 Before/After
**Fonte:** `linkedin/ideias.md`, "Diário técnico (coleta de 2026-10-05)",
item "[trabalho] Warm-up sequencial aquece uma conexão só".
**Ângulo:** o teste de carga do CI estourava o p95 de vez em quando, sem
padrão aparente. Antes: o warm-up chamava os endpoints um de cada vez, só
uma conexão do pool do banco ficava pronta antes da medição começar.
Depois: o warm-up virou rajadas concorrentes contra os mesmos endpoints que
o k6 mede (lidos do catálogo do teste) e ganhou timeout de conexão e de
duração. A diferença foi essa mudança: aquecer tem que reproduzir a
concorrência da medição.

## Engajar (20 min/dia, antes de postar)

Sem uma lista de perfis reais registrada em `voice.md` ou `ideias.md`, não
dá pra montar os 10 nomes (5 alcance / 3 pares / 2 compradores) sem
inventar. **{{lista de 10 perfis reais — 5 de alcance, 3 pares do mesmo
nível, 2 que poderiam te contratar}}**: preencha com quem você realmente
quer comentar essa semana, ou peça pra eu montar a partir de uma lista de
perfis que você mandar.

## Observação sobre horário

O dia e a hora importam bem menos do que a primeira linha funcionar. Os
horários acima só existem porque a rotina exige 1 post por dia entre 7h30 e
9h30; o que decide se o post performa é o gancho.
