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

## Diário técnico (coleta de 2026-10-05)

### [trabalho] Warm-up sequencial aquece uma conexão só
- **Problema:** o teste de carga do CI estourava o p95 de vez em quando. O warm-up antes da medição fazia as chamadas uma por vez, então só uma conexão do pool do banco ficava pronta. Quando o k6 subia vários usuários virtuais em paralelo, o driver abria conexões novas no meio da medição, e cada uma pagava TCP, TLS e autenticação até um banco em outra região. O endpoint que usa duas conexões por request (contagem e busca em paralelo) sofria mais.
- **O que fiz:** o warm-up virou rajadas concorrentes contra os mesmos endpoints que o k6 mede, lidos do próprio catálogo do teste, então endpoint novo já entra aquecido. Depois pus timeout de conexão e de duração em toda chamada: uma dependência que aceita a conexão e não responde travava a rodada inteira esperando.
- **Lição:** aquecer é reproduzir a concorrência da medição, não só "chamar uma vez". Warm-up sequencial deixa o pool do tamanho de um.
- **Rende post de:** TEACH

### [trabalho] Soft delete que a entidade não conhecia
- **Problema:** um registro excluído (soft delete) no sistema de origem continuava aparecendo no meu serviço, porque o mapeamento da entidade do meu lado não declarava a coluna de exclusão. E o progresso que o usuário já tinha naquele item continuava contando.
- **O que fiz:** mapeei as colunas de auditoria e de exclusão e pus um filtro global de consulta no EF Core (HasQueryFilter), para o padrão ser "não ver o excluído". No único lugar que precisa enxergar os excluídos (descartar o progresso de itens que sumiram), uso IgnoreQueryFilters de forma explícita.
- **Lição:** soft delete é um contrato que todo leitor precisa conhecer. Com filtro global, esquecer vira impossível e a exceção fica visível no código, em vez do contrário.
- **Rende post de:** TEACH

### [trabalho] Progresso casado por posição, não por identidade
- **Problema:** quando o conteúdo de uma etapa era reconstruído, o progresso anterior passava para o novo sempre que havia exatamente um item antes e um depois. Se o item tinha sido trocado por outro, o usuário herdava o progresso de algo que nunca fez. E uma etapa sem nenhum item ainda entrava na conta do progresso.
- **O que fiz:** o progresso só passa adiante se o conjunto de ids for o mesmo, comparado ordenado. Etapa vazia deixou de contar. A reconstrução agora devolve quais grupos mudaram de composição, para recalcular só esses. A regra de "o que conta no progresso" ficou numa classe só, usada pelos dois lados.
- **Lição:** "um antes, um depois, deve ser o mesmo" é heurística de posição. Estado do usuário se casa por identidade, ou vaza para o item errado.
- **Rende post de:** TEACH ou STORY

### [trabalho] Contrato de mensageria testado nos bytes
- **Problema:** um campo novo passou a viajar numa mensagem entre serviços, e eu precisava receber, gravar e repassar adiante. Mensagens antigas não trazem o campo, e uma revogação pode chegar depois sobre o mesmo registro.
- **O que fiz:** ausência do campo vale false; a revogação sobrescreve o mesmo documento pela chave natural. O teste de fluxo parte dos bytes recebidos e termina nos bytes publicados, passando pelo pipeline real e pelo mesmo serializador de produção, com três casos: campo presente, campo ausente e revogação.
- **Lição:** teste de mensageria com objeto montado à mão não pega erro de nome de campo nem de serialização. O contrato é o JSON que trafega.
- **Rende post de:** TEACH

### [pessoal] CI verde, 653 testes, e o cadastro não funcionava
- **Problema:** no meu projeto pessoal (um app de conversação em inglês por voz), um loop autônomo de agente fechava cada card pelos gates: lint, tipos, cobertura e testes. Um roteiro de QA contra a stack real achou em minutos dois defeitos que estavam na main com 653 testes passando. Todo cadastro por e-mail falhava em silêncio: o ORM inseria a credencial antes do aluno, a FK recusava, e o erro virava "e-mail já existe", que responde 202 de propósito para não revelar contas. E quatro rotas não isolavam um aluno do outro: com um token inválido, uma delas devolvia a transcrição e o áudio de outro aluno.
- **O que fiz:** a causa era o mundo dos testes ter um aluno só: uma fixture gravava o aluno antes da credencial, e outra sobrescrevia a identidade de quem pede em todas as rotas. Pus a checagem de dono no caso de uso (o id de quem pede virou campo obrigatório do comando, e o mypy recusa a chamada sem ele), recurso alheio responde o mesmo 404 do inexistente, e toda rota desse tipo ganhou dois testes: sem token dá 401, outro aluno dá 404. O roteiro ponta a ponta virou arquivo versionado, com 31 verificações.
- **Lição:** gates verdes provam que o código é coerente consigo mesmo, não que o produto funciona. Teste com um usuário só não exercita autorização.
- **Rende post de:** STORY ou OPINION

### [pessoal] Duas abas renovando o token ao mesmo tempo
- **Problema:** ao desenhar a sessão da versão web do projeto pessoal, rodei dois curl em paralelo pedindo refresh com o mesmo token. Os dois receberam token novo. O handler lia o token, conferia se estava revogado e só depois o revogava (check-then-act): a família de tokens bifurcava, e um refresh roubado usado no mesmo instante que o dono escapava da detecção de reuso.
- **O que fiz:** a revogação virou um único UPDATE ... WHERE revoked_at IS NULL RETURNING id; quem não recebe a linha perdeu a corrida e é tratado como reuso. No navegador, o refresh fica em cookie HttpOnly, SameSite=Strict, na mesma origem da API, e só uma aba renova por vez com a Web Locks API (navigator.locks); a aba que espera já manda o cookie rotacionado pela primeira.
- **Lição:** ler, conferir e gravar em três passos é uma corrida esperando acontecer. A pergunta "e se duas chegarem juntas?" vale ser testada de verdade, não só pensada.
- **Rende post de:** TEACH

### [pessoal] A tradução que respondia em vez de traduzir
- **Problema:** no botão que traduz a fala do professor virtual do projeto pessoal, o modelo às vezes respondia à pergunta em vez de traduzir, e em inglês, dizendo que era um assistente de IA sem projetos pessoais. O prompt já mandava não responder, mas enviava o texto cru como mensagem do usuário, e a fala do professor quase sempre termina em pergunta.
- **O que fiz:** o texto passou a entrar delimitado por marcas, e a instrução diz que o delimitado é material: pergunta ali é traduzida, não respondida. As marcas são removidas se o modelo ecoar. Medi com o Claude Haiku 4.5 em três falas terminando em pergunta: o prompt antigo errou 10 de 90 (11%), o novo errou 0 de 90. As duas rodadas custaram US$ 0,063. O adaptador não tinha nenhum teste; ganhou sete, e três deles falham na versão antiga.
- **Lição:** separar dado de instrução no prompt é a mesma técnica usada contra prompt injection. E comportamento de LLM se decide por taxa sobre N execuções, nunca por uma execução que funcionou.
- **Rende post de:** PROOF ou TEACH

### [pessoal] A política de retenção que nenhum código chamava
- **Problema:** no projeto pessoal, as regras de expiração do bucket de áudio estavam escritas e testadas, mas nenhum código de produção as aplicava. No bucket local a configuração de lifecycle nem existia: a voz gravada ficava guardada para sempre, sem erro nenhum (o app ainda não tem usuários reais). E a API assinava URL de áudio já expirado, que virava 404 no player.
- **O que fiz:** aplicar as regras virou um comando de operador, idempotente, que lê de volta o que aplicou. O worker confere no boot: sem as regras, ou com prazos diferentes da configuração, ele não sobe e a mensagem diz qual comando rodar. A API passou a prever a expiração pela data de criação, sem consultar o bucket. Não apliquei no boot de propósito: isso daria à credencial do app permissão de administrar o bucket.
- **Lição:** função testada que ninguém chama é só documentação. Política obrigatória tem que falhar alto quando não está valendo.
- **Rende post de:** TEACH ou OPINION
