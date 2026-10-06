---
scheduled_at: 2026-10-07T08:00:00-03:00
visibility: PUBLIC
type: TEACH
hook: "#8 Question Trap"
human_score: 77.1
image: "media/fotos/gerado-refresh-token-corrida.png"
image_alt: "Diagrama: duas abas pedem refresh do mesmo token, o handler em 3 passos abre uma janela de corrida, um UPDATE atômico a substitui e só quem recebe a linha vence"
image_request: "Uma foto do seu caderno ou quadro com o diagrama dessa corrida rabiscado à mão (duas setas chegando juntas, um x no meio). Sem nada do trabalho, só o rascunho."
---
Duas abas pedem refresh do mesmo token ao mesmo tempo. O que o seu backend devolve?

Testei isso essa semana, no projeto pessoal, com dois curl rodando em paralelo, pedindo refresh com o mesmo token.

Os dois receberam token novo.

O handler fazia três passos: lia o token, conferia se já estava revogado e só depois revogava, e entre o segundo passo e o terceiro havia uma janela em que duas requisições podiam passar pela checagem antes de qualquer uma delas revogar.

A família de tokens bifurcava ali. Um refresh roubado, usado bem nesse instante, escapava da detecção de reuso.

Ler, conferir e gravar em três passos separados é uma corrida esperando acontecer.

A correção trocou os três passos por um só:

UPDATE tokens SET revoked_at = now() WHERE revoked_at IS NULL RETURNING id

Quem não recebe uma linha de volta perdeu a corrida e é tratado como reuso.

No navegador, o refresh token mora num cookie HttpOnly, SameSite Strict, na mesma origem da API, e só uma aba renova por vez, usando a Web Locks API do navegador, o navigator.locks, pra isso; a aba que espera a vez já recebe o cookie rotacionado pela primeira, sem precisar repetir a chamada.

Teste de verdade. Com dois curl mesmo, não só de cabeça.

No seu sistema, o que acontece quando duas requisições concorrentes tentam consumir o mesmo token ao mesmo tempo?
