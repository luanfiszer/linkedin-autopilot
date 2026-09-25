# Ideias e fatos da semana

Anote aqui, do celular mesmo, o que aconteceu: uma conversa com cliente, um
número, um erro, algo que você construiu, uma discussão. Uma linha basta.

A rotina de segunda lê este arquivo para escrever os posts. Ela **só usa o que
estiver escrito aqui ou no `voice.md`**, então quanto mais concreto, melhor.
Depois de usar uma ideia, a rotina não apaga nada: risque ou apague você mesmo.

A coleta semanal (sexta à tarde, no seu Mac) acrescenta aqui um **diário
técnico** tirado dos seus commits, já sem nada da empresa. Revise quando
quiser: se algo estiver específico demais, apague.

## Esta semana

-

## Diário técnico (coleta de 2026-09-25)

- [trabalho] Documento derivado que também guarda estado: um processo noturno reconstruía do zero um JSON desnormalizado a partir da fonte, mas parte do estado (progresso do usuário) só existia nesse JSON. Resultado: o progresso zerava toda madrugada e, pior, outra rotina usava esse valor como "memória" para nunca regredir, então a regressão vazava para outras tabelas. Aprendi que "é só reconstruir da fonte" só vale se o documento for 100% derivado; a correção foi mesclar o estado anterior no documento novo, casando por id com fallback por nome.
- [trabalho] Desserialização tipada apaga dados em silêncio: com dois escritores gravando o mesmo JSON em paralelo, ler para uma classe e regravar descartava toda chave que a classe não declarava, e o campo do outro escritor sumia no round-trip. Resolvi com JsonExtensionData no .NET nos níveis que são regravados. Lição: todo read-modify-write de documento compartilhado precisa preservar o que ele não conhece.
- [trabalho] Bug de fuso em "a mais recente vence": com o modo legado de timestamps do driver do PostgreSQL no .NET, um DateTime lido de uma coluna timestamptz voltava no fuso do processo, e uma consolidação mais antiga passava a parecer mais nova e sobrescrevia a certa. Troquei para DateTimeOffset e escrevi um teste de regressão com a data expressa em -03:00. Só apareceu ao reproduzir num ambiente real, nunca nos testes locais.
- [trabalho] Performance: uma consulta com vários joins projetava uma coluna de JSON grande, e o produto cartesiano repetia esse JSON em cada linha. A resposta saiu de rápida para estourar o timeout. A correção foi buscar o JSON numa consulta própria, uma vez só. Lição: coluna pesada e join com cardinalidade alta não combinam na mesma projeção.
- [trabalho] Revert antes de acertar: um fix que tentava "migrar" uma entidade existente quando o agrupamento do usuário mudava foi revertido no mesmo dia. A versão final modelou o vínculo explicitamente numa tabela de relação, com migration idempotente e backfill, em vez de achar o registro por heurística de nome. Aprendi que identidade inferida por nome vira registro órfão cedo ou tarde.
- [trabalho] Correção manual de dados vira regra versionada: um UPDATE feito à mão para preencher caminhos de arquivos divergia da planilha de referência em muitas linhas (encoding de barra, barra dupla, extensões que nem deviam ter caminho). Transformei as regras da planilha num model dbt com normalização antes da comparação e um teste de not_null. Depois simplifiquei (a macro só tinha um uso) e conferi que o resultado era idêntico linha a linha antes de trocar.
- [trabalho] Spec antes do fix: nas correções maiores da semana escrevi proposta, design e spec (formato OpenSpec) antes do código, com casos de borda e roteiro de validação em homologação. Foi assim que o segundo bug (o do campo apagado no round-trip) apareceu, medindo o documento antes e depois.
