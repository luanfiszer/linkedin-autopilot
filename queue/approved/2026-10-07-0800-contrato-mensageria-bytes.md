---
scheduled_at: 2026-10-07T08:00:00-03:00
visibility: PUBLIC
type: TEACH
hook: "#5 The List Promise"
human_score: 71.9
image: "media/fotos/gerado-contrato-mensageria-bytes.png"
image_alt: "Cartão de código em C# comparando um teste de mensageria errado (objeto montado à mão) com o certo (parte dos bytes recebidos, passa pelo serializer de produção e termina nos bytes publicados)"
image_request: "Print do terminal do seu projeto pessoal rodando os testes desse contrato (os três casos: campo presente, ausente, revogação). Esconda nome do projeto e caminhos de pasta."
---
3 coisas que aprendi testando contrato de mensageria pelos bytes, não pelo objeto.

Um campo novo passou a viajar numa mensagem entre dois serviços.

Eu precisava receber, gravar e repassar adiante. Mensagens antigas não trazem esse campo, e uma revogação pode chegar depois, sobre o mesmo registro.

A regra: ausência do campo vale false. Revogação sobrescreve o mesmo documento, pela chave natural.

- Objeto montado à mão no teste não pega erro de nome de campo: se o teste cria o objeto em C# e serializa, um campo renomeado nos dois lados do contrato ainda bate sozinho, porque os dois lados usam o mesmo nome errado. O contrato real é o JSON que trafega, a classe é só um Payload por cima dele.
- O teste de fluxo parte dos bytes recebidos e termina nos bytes publicados, passando pelo pipeline real e pelo mesmo Serializer de produção. Foi assim que um erro de Schema apareceu.
- Três casos cobrem a maior parte dos bugs de contrato: campo presente, campo ausente, revogação chegando depois.

Cada caso como Snapshot de bytes reais. Nunca um mock do meio do caminho.

Teste de mensageria que não passa pelo Serializer de produção testa a sua classe. Não o seu contrato.

O teste do seu contrato de mensageria parte de bytes de verdade, ou de um objeto que você mesmo montou?
