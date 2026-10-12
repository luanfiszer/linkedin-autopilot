---
scheduled_at: 2026-10-23T07:45:00-03:00
visibility: PUBLIC
type: STORY
hook: "#19 Curiosity Gap"
human_score: 74
image: "media/fotos/gerado-duas-abas-token.png"
image_alt: "Diagrama: dois refresh em paralelo recebem token novo; correção é um UPDATE atômico e só uma aba renovando por vez com a Web Locks API"
image_request: "Print dos dois terminais com os comandos curl rodando em paralelo no seu projeto pessoal. Esconda token, IP e qualquer dado real; só os comandos e as respostas."
---
O bug mais estranho que eu já achei apareceu quando rodei o mesmo comando duas vezes, nos mesmos milissegundos, só pra ver o que acontecia.

As duas chamadas voltaram com sucesso. As duas receberam um refresh token novo.

Eu estava desenhando a sessão da versão web do meu projeto pessoal, o app de inglês por conversa de voz. Pra testar o fluxo de renovação de token, abri dois terminais e rodei dois curl em paralelo, pedindo refresh com o mesmo token.

Pela lógica, o segundo devia falhar. Token usado uma vez devia morrer.

A causa: o código que processa o refresh lia o token, conferia se já estava revogado, e só depois gravava a revogação, três passos separados, em sequência, no clássico formato check-then-act. Entre o "conferir" e o "gravar" cabe uma chamada inteira de outro processo.

O efeito prático é pior do que parece à primeira vista. Se alguém roubasse um refresh token e usasse ele bem no instante em que o dono também usa, a detecção de reuso (que existe justamente pra pegar token roubado) não via nada de errado. As duas famílias de token continuavam vivas, em paralelo, sem ninguém saber.

A correção: um UPDATE só. UPDATE refresh_tokens SET revoked_at = now() WHERE id = $1 AND revoked_at IS NULL RETURNING id. Quem não recebe a linha de volta perdeu a corrida, e é tratado como reuso. Sem conferir antes, sem três passos, sem brecha.

No navegador eu travei por outro lado: o refresh fica num cookie HttpOnly, SameSite=Strict, na mesma origem da API. E só uma aba renova por vez, com a Web Locks API (navigator.locks). A aba que esperou nem precisa pedir de novo: ela já usa o cookie que a primeira aba rotacionou.

Ler, conferir e só depois gravar, em passos separados, é uma corrida esperando a hora certa de acontecer.

Você já rodou duas requisições idênticas ao mesmo tempo no seu sistema, só pra ver no que dava?

#Python #Seguranca
