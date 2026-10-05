---
scheduled_at: 2026-10-13T08:15:00-03:00
visibility: PUBLIC
type: PROOF
hook: "#17 Time Anchor"
human_score: 76.7
image: "media/fotos/gerado-query-json-grande-join.png"
image_alt: "Infográfico: antes, um JOIN repete uma coluna de JSON grande em cada linha e estoura o timeout; depois, o JSON é buscado numa consulta separada e a resposta volta rápida"
image_request: "Print do seu projeto pessoal mostrando uma consulta ou um gráfico de tempo de resposta (antes/depois de uma otimização). Esconda nome do projeto, caminhos de pasta e qualquer dado real de usuário."
---
Uma consulta que sempre foi rápida começou a estourar o timeout.

Voltar a ficar rápida levou uma mudança pequena.

Ela tinha vários JOIN e projetava, lado a lado com o resto, uma coluna de JSON grande. É assim que JOIN funciona: ele multiplica tudo que está do lado de quem tem mais linha, inclusive o JSON que você só queria ler uma vez.

Com pouca linha, ninguém notava. O volume cresceu. A resposta que levava segundos parou de voltar dentro do tempo limite.

A correção não mudou o SQL que o ORM (Entity Framework, no caso) gera pra consulta principal. Só tirou o JSON dali.

Depois de já saber quais linhas eu precisava, busquei o JSON numa consulta LINQ separada, pelo id de cada uma. Uma vez. Não uma vez por linha do JOIN.

Coluna pesada e JOIN com muita linha não combinam na mesma projeção.

Hoje, antes de adicionar um Include novo, eu faço uma pergunta: esse dado precisa estar na mesma consulta, ou só precisa chegar no mesmo lugar que o resto?

Você já teve uma consulta que ficou lenta sem nenhuma linha de código ter mudado?
