---
scheduled_at: 2026-10-06T09:20:00-03:00
visibility: PUBLIC
type: PROOF
hook: "#2 Number Reveal"
human_score: 72.8
image: "media/fotos/gerado-prompt-delimitador-codigo.png"
image_alt: "Cartão de código em Python comparando duas versões de uma função que monta o prompt de tradução: a errada manda o texto cru, a certa delimita o texto como material"
image_request: "Print do seu terminal rodando os testes do adaptador de tradução (os 7 que ganhou, incluindo os 3 que falham na versão antiga). Esconda nome do projeto e caminhos de pasta."
---
Rodei a mesma fala 90 vezes contra o modelo, antes e depois de uma mudança de uma linha no prompt. 10 erros viraram 0.

No projeto pessoal que estou construindo (um app de treino de inglês por conversa de áudio), o professor virtual tem um botão que traduz a fala dele. De vez em quando, em vez de traduzir, o modelo respondia à pergunta. Em inglês, inclusive, dizendo que era um assistente de IA sem projetos pessoais.

O prompt já mandava não responder. O problema era outro: o texto ia cru como mensagem do usuário, e a fala do professor quase sempre termina em pergunta. Pro modelo, pergunta de usuário pede resposta.

A correção: o texto passou a entrar delimitado por marcas, com uma instrução dizendo que o que está delimitado é material, não é uma pergunta pra responder. As marcas somem se o modelo ecoar elas de volta.

Medi com o Claude Haiku 4.5, três falas terminando em pergunta, 90 execuções: o prompt antigo errou 10 (11%), o novo errou 0. As duas rodadas custaram US$ 0,063 juntas.

O adaptador que faz essa chamada não tinha nenhum teste. Ganhou sete. Três deles falham se eu reverto a correção.

Separar dado de instrução no prompt é a mesma técnica que se usa contra prompt injection. E comportamento de LLM se decide pela taxa de erro em N execuções, nunca por uma execução que deu certo.

Você mede o prompt rodando uma vez, ou rodando várias e contando quantas erram?
