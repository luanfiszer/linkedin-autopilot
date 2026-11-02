---
scheduled_at: 2026-11-13T08:00:00-03:00
visibility: PUBLIC
type: STORY
hook: "#14 Pattern Interrupt"
human_score: 75.2
image: "media/fotos/gerado-documento-derivado-estado.png"
image_alt: "Infográfico: documento reconstruído do zero zerava o progresso; a correção mescla o estado anterior pela chave, com fallback pelo nome"
image_request: "Foto de um rascunho seu, à mão, com duas caixas ligadas por uma seta: 'documento' e 'estado que não é dele'. Sem nada do trabalho atual."
---
O progresso voltava a zero.

Toda madrugada.

Um Job noturno, um Cron se você preferir chamar assim, reconstruía um documento JSON inteiro do zero, direto da fonte, achando que isso bastava pra garantir que tudo ficasse consistente.

Parecia bem seguro.

Se o documento é derivado, reconstruir ele do zero todo dia devia bater sempre com a fonte, sem exceção nenhuma, sem resto de estado antigo escondido em lugar nenhum.

Só que não.

Um campo, o Progresso que o usuário já tinha, só existia dentro desse documento.

Eu não tinha percebido isso antes.

Toda madrugada, o Job apagava o documento antigo, montava um novo, e esse campo recomeçava em zero junto com ele, sem avisar ninguém.

Ficou bem pior.

Outra rotina do sistema lia esse mesmo campo como teto e nunca deixava o progresso regredir abaixo do que já tinha visto antes. Então, com o valor zerado, ela aceitava qualquer número novo como avanço válido, e a regressão vazava pra outras tabelas que dependiam dela.

Eu mesclei o estado anterior no documento novo.

Um Merge pela chave, um Guid que identifica o registro, com fallback pelo Nome nos casos em que o Guid ainda não existia.

Hoje, antes de qualquer Job "reconstruir do zero", eu comparo um Snapshot de antes com um de depois, sem nenhum UPSERT escondendo o campo antigo no meio do caminho, porque um documento derivado de verdade não pode guardar nenhum resto que não exista em mais lugar nenhum da base.

"É só reconstruir da fonte" só é verdade se o documento for cem por cento derivado.

Você já conferiu se um Job que "reconstrói do zero" no seu sistema é só derivado, ou guarda algum campo que não existe em nenhum outro lugar?

#BackEnd #Arquitetura