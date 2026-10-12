---
scheduled_at: 2026-10-20T08:15:00-03:00
visibility: PUBLIC
type: PROOF
hook: "#2 Number Reveal"
human_score: 82
image: "media/fotos/gerado-traducao-delimitador.png"
image_alt: "Infográfico: 10 de 90 execuções erradas antes da correção, 0 de 90 depois, com trecho delimitado <<<TRADUZIR...TRADUZIR>>>"
image_request: "Print da tela do seu app pessoal no botão de tradução, ou da conversa com o professor virtual. Esconda qualquer nome do projeto que apareça na tela."
---
Testei o tradutor do meu projeto pessoal em 90 conversas. Em 10 delas, o modelo respondeu a pergunta do professor virtual em vez de traduzir ela.

Troquei uma linha no prompt. Nas 90 conversas seguintes, zero erros.

O projeto é um app de inglês por conversa de voz: você fala com um professor de IA, ele responde, e tem um botão pra traduzir a fala dele. O problema aparecia quando a fala do professor terminava em pergunta, o que é quase sempre, e às vezes o modelo respondia em inglês, dizendo que era um assistente de IA sem projetos pessoais.

Eu já tinha pedido no prompt pra não responder, só traduzir. Não bastou: eu mandava o texto cru como se fosse uma mensagem minha, e o modelo tratava aquilo como parte da conversa, não como material pra traduzir.

A correção foi separar dado de instrução: o texto a traduzir passou a entrar delimitado por marcas, com uma instrução dizendo que tudo ali dentro é material. Pergunta lá dentro é traduzida, não respondida. As marcas são removidas se o modelo ecoar elas por engano.

Medi com o Claude Haiku 4.5 em três falas diferentes terminando em pergunta. Prompt antigo: 10 erros em 90 execuções. Prompt novo: 0 em 90. As duas rodadas de teste custaram US$ 0,063 juntas.

O adaptador não tinha nenhum teste antes disso. Ganhou sete; três deles falham se eu volto pro prompt antigo.

Comportamento de modelo de linguagem se decide pela taxa em várias execuções, nunca por uma execução que deu certo. E separar dado de instrução é a mesma técnica usada contra prompt injection, só que eu não tinha pensado nela pro meu próprio texto.

Você já testou seu prompt mais de uma vez com o mesmo tipo de entrada antes de confiar nele?

#Python #IA
