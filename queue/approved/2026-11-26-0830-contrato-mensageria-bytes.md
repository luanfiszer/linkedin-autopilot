---
scheduled_at: 2026-11-26T08:30:00-03:00
visibility: PUBLIC
type: TEACH
hook: "#5 The List Promise"
human_score: 76.3
image: "media/fotos/gerado-contrato-mensageria-bytes.png"
image_alt: "Cartão de código: teste de contrato de mensageria com 3 casos pelos bytes reais: campo presente, ausente, revogação"
image_request: "Foto de um rascunho seu, à mão, mostrando os 3 casos de teste (campo presente, ausente, revogação) que cobrem o contrato da mensagem. Sem nada do trabalho."
---
3 coisas que um teste de contrato de mensageria pelos bytes pegou, que um objeto montado à mão nunca pegaria.

Um campo novo, RevogadoEm, um DateTimeOffset opcional, passou a viajar numa mensagem entre dois serviços, e eu precisava receber esse campo, gravar ele e repassar adiante pro próximo consumidor da fila, sem quebrar quem ainda não sabia que esse campo existia.

Jeito rápido de testar: monta o objeto na mão, com o construtor, chama ProcessarAsync.

Passa fácil.

Não prova quase nada.

Troquei por um teste que parte dos bytes de verdade: um [Theory] do xUnit em que JsonSerializer.Serialize gera a mensagem exatamente como ela sai de produção, o consumidor deserializa com o mesmo contrato, o pipeline inteiro roda do jeito que roda em produção, e Assert.Equal confere os bytes publicados do outro lado contra o que era esperado, byte a byte.

3 [InlineData]. Três casos que o objeto na mão nunca pegaria:

- campo presente, RevogadoEm chegando certo até o fim;
- campo ausente, porque mensagem antiga da fila não traz essa propriedade;
- revogação chegando depois, sobrescrevendo pela chave natural o que já estava gravado.

Pro campo ausente, o default tinha que ser decidido. Não acidental.

Um objeto montado à mão nunca pegaria um erro de nome de propriedade na serialização: o campo chegava em camelCase do outro serviço, e o meu DTO esperava PascalCase. Esse tipo de erro só aparece quando o JSON de verdade passa pelo deserializador, não quando eu mesmo construo o objeto já certo, com o nome digitado igual nos dois lados.

Teste com objeto na mão testa a sua lógica. Teste pelos bytes testa o contrato.

Seu teste de integração passa pelo JsonSerializer de verdade, ou só pelo objeto que você já montou certo?
