---
scheduled_at: 2026-11-11T07:45:00-03:00
visibility: PUBLIC
type: OPINION
hook: "#15 The Warning"
human_score: 83.9
image: "media/fotos/gerado-vinculo-por-id.png"
image_alt: "Cartão de código em C# comparando buscar o vínculo por Nome (errado) com modelá-lo numa tabela de relação por Id (certo)"
image_request: "Print de um teste seu passando no terminal do projeto pessoal, mostrando esse tipo de comparação por chave. Sem nome de projeto ou caminho de pasta visível."
---
Achar o vínculo certo pelo nome parece prático. Isso está te custando um registro órfão que você ainda não viu.

Essa semana, um fix meu foi revertido no mesmo dia em que entrou.

A causa cabia numa linha: pra achar o vínculo certo quando o agrupamento de um usuário mudava, o código comparava um Where por Nome, nunca por Id, do jeito que o LINQ do .NET deixa escrever fácil demais.

Funcionava enquanto o nome não repetia e não mudava.

No primeiro caso real em que dois registros tinham o mesmo nome, o vínculo foi pra entidade errada, e ninguém recebeu erro nenhum: o Where encontrou alguma coisa, só não a certa.

A correção trocou a heurística por uma tabela de relação própria em Entity Framework Core, com Guid como chave, índice único, e uma Migration idempotente com backfill pros vínculos antigos.

Nada mais compara string pra decidir identidade.

Heurística por nome é conveniente até o dia em que duas linhas da mesma tabela têm o mesmo valor nesse campo.

Identidade inferida por nome vira registro órfão cedo ou tarde. A pergunta não é se, é quando.

No seu sistema, que vínculo hoje é inferido por nome em vez de guardado numa chave?

#Arquitetura #BackEnd