---
scheduled_at: 2026-10-08T07:45:00-03:00
visibility: PUBLIC
type: STORY
hook: "#14 Pattern Interrupt"
human_score: 73.2
image: "media/fotos/gerado-ci-verde-cadastro-quebrado.png"
image_alt: "Infográfico: de um lado, uma fixture com um aluno só esconde dois defeitos de autorização apesar de 653 testes verdes; do outro, o ID de quem pede vira obrigatório e um roteiro de QA ganha 31 verificações"
image_request: "Print do terminal do seu projeto pessoal mostrando a suíte de testes rodando (os 653 verdes, ou o roteiro de QA com as 31 verificações). Esconda nome do projeto e caminhos de pasta."
---
CI verde. Produto quebrado.

No meu projeto pessoal, um loop autônomo de agente fecha cada card passando por lint, checagem de tipos, cobertura e testes, com a main em 653 testes passando.

Eu rodei um roteiro de QA contra a stack real, por decisão minha, fora desses gates, e em minutos achei dois defeitos que a main inteira não via.

O primeiro: todo cadastro por e-mail falhava em silêncio. O ORM inseria a credencial antes do registro do aluno, e a chave estrangeira recusava.

O erro virava "e-mail já existe", um 202 escolhido assim, pra não revelar quais contas existem. Ninguém conseguia se cadastrar, e a mensagem escondia isso de mim também.

O segundo era pior: quatro rotas não isolavam um aluno do outro, e com um token inválido, uma delas devolvia a transcrição e o áudio de outro aluno.

A causa dos dois era a mesma. O mundo dos meus testes tinha um aluno só: uma fixture gravava o aluno antes da credencial, por isso a FK nunca recusava nos testes, e outra fixture sobrescrevia a identidade de quem fazia o pedido em toda rota.

Autorização nunca era exercitada. Só existia um "quem".

Eu corrigi a causa, não o sintoma. O ID de quem pede virou campo obrigatório do comando, e o mypy recusa a chamada sem ele.

Recurso de outro aluno passou a responder o mesmo 404 do inexistente. Toda rota desse tipo ganhou dois testes: sem token dá 401, token de outro aluno dá 404.

O roteiro de QA virou um arquivo versionado, com 31 verificações.

Gates verdes do CI provam que o código é coerente consigo mesmo. Não provam que o produto funciona.

Seus testes rodam com mais de um usuário, ou só o aluno de sempre?
