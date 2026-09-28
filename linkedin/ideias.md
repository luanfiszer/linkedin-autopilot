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

## Diário técnico (coleta de 2026-09-28)

A coleta anterior (25/09) já cobriu os commits de preservação de estado, do campo apagado no round-trip e do spec antes do fix. Aqui entram só as ideias novas da semana.

### [trabalho] A fila de erro que nunca recebia nada
- **Problema:** o consumer RabbitMQ tinha fila de erro (dead-letter) configurada, mas ela vivia vazia. A classe base capturava toda exceção e devolvia um nack sem requeue como retorno normal; a biblioteca só manda para a fila de erro quando o handler lança. A mensagem que falhava era descartada em silêncio, e o trace ainda marcava a execução como OK.
- **O que fiz:** documentei o comportamento no design, separei o retry num card próprio e deixei o alerta de falha de consumo como parte da entrega.
- **Lição:** configurar dead-letter não prova nada. Teste o caminho de falha de ponta a ponta e veja onde a mensagem realmente vai parar.
- **Rende post de:** STORY ou TEACH

### [trabalho] Mensagem fora de ordem e reprocessamento idempotente
- **Problema:** um serviço publica um consolidado com data de consolidação. Em mensageria, uma mensagem mais antiga pode chegar depois de uma mais nova, e a mesma mensagem pode ser entregue duas vezes.
- **O que fiz:** a entidade só aceita o consolidado novo se ele não for mais antigo que o gravado; mensagem sem a data é ignorada com warning; mensagem sem o bloco preserva o que já estava gravado. Tudo na mesma transação do upsert existente.
- **Lição:** "a última que chegou vence" é bug esperando acontecer. Quem decide é o timestamp do produtor, e reprocessar tem que dar o mesmo estado.
- **Rende post de:** TEACH

### [trabalho] Fail-closed com cadeia de fallback
- **Problema:** a permissão de cada tipo de conteúdo vinha de duas fontes: um valor específico por item, que ainda não cobria todos os tipos, e uma regra global mais grossa.
- **O que fiz:** uma única regra de composição: o pai precisa estar liberado E (valor específico ?? padrão global ?? negado). Valor que não é booleano e chave desconhecida são ignorados. Quando o outro lado passar a mandar o valor específico de um tipo novo, ele vale sem mudança de código.
- **Lição:** o operador de coalescência resolve compatibilidade futura de graça, desde que o último fallback seja "negar" e não "liberar".
- **Rende post de:** TEACH ou OPINION

### [trabalho] Gambiarra provisória desenhada para ser apagada
- **Problema:** um serviço upstream estava mandando um veredito inconsistente enquanto era corrigido, e eu precisava de uma checagem redundante no meu lado nesse meio-tempo.
- **O que fiz:** gravei só o dado de entrada no documento e apliquei a regra na leitura, num único calculator. Não alterei o valor que veio do upstream, que fica como veio para auditoria. Havia um motivo extra: o mesmo objeto era compartilhado por referência entre vários trechos do documento, então marcar um deles na gravação vazaria para os outros.
- **Lição:** remendo temporário não deve contaminar o dado persistido. Se remover exige migração, não era temporário. O meu sai apagando uma classe.
- **Rende post de:** OPINION
