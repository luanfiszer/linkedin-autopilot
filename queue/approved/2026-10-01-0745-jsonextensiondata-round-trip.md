---
scheduled_at: 2026-10-01T07:45:00-03:00
visibility: PUBLIC
type: TEACH
hook: "#21 The Direct Value"
human_score: 76.5
image_request: "Foto de um rascunho à mão (caderno ou quadro) com os dois processos gravando o mesmo JSON e o campo sumindo no round-trip. Nada de tela nem código do trabalho."
image: "media/fotos/gerado-json-round-trip.png"
image_alt: "Infográfico: classe C# sem o campoB regrava o JSON e apaga o campo; [JsonExtensionData] preserva"
---
Aqui está a correção exata que uso quando dois processos escrevem no mesmo JSON. Rouba.

Mexi nisso há pouco tempo: dois escritores gravavam o mesmo JSON em paralelo.

Eu lia esse JSON pra uma classe C# e regravava com o System.Text.Json depois de alterar um campo.

Só que a classe só declarava as propriedades que ela mesma usava.

No round-trip, ler, alterar, regravar, toda chave sem propriedade correspondente na classe sumia, e o campo que o outro escritor tinha acabado de gravar ia junto, sem erro nenhum, sem log, sem exceção.

Silencioso.

A correção: [JsonExtensionData] numa propriedade do tipo IDictionary<string, JsonElement>.

Esse atributo diz ao desserializador pra guardar ali qualquer chave que não bate com nenhuma propriedade declarada, e devolver o mesmo dicionário quando serializa de novo.

A classe passa a preservar o que não conhece.

Não descarta mais.

A regra que fica: todo read-modify-write de um documento compartilhado precisa preservar o que ele não sabe interpretar, porque o outro escritor pode saber exatamente o que aquela chave significa mesmo sem essa classe conhecer.

Se não preservar, dado sumindo em silêncio é questão de tempo.

Você já perdeu um campo assim, num round-trip que parecia inofensivo?
