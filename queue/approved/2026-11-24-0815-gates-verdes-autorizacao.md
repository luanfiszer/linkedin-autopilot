---
scheduled_at: 2026-11-24T08:15:00-03:00
visibility: PUBLIC
type: PROOF
hook: "#10 The Receipt"
human_score: 70.4
image: "media/fotos/gerado-ci-verde-autorizacao.png"
image_alt: "Diagrama: 653 testes verdes, fixture com 1 aluno, QA manual de 31 verificações acha 2 bugs reais de autorização"
image_request: "Print do terminal do seu projeto pessoal rodando a suíte de testes, ou foto do caderno com o checklist de QA manual que você usou. Esconda nome do projeto e caminhos de pasta."
---
653 testes passando. 2 bugs reais que vazavam dado de um aluno pro outro.

No meu projeto pessoal, um loop autônomo de agente de IA fecha cada unidade de trabalho só depois de passar pelos gates: lint, mypy (checador de tipos do Python), cobertura e os testes. Tudo verde, direto.

Essa semana rodei um roteiro de QA manual contra a stack real, fora da suíte automatizada. 31 verificações, uma por uma, num checklist que dá pra escrever pra qualquer sistema.

Em minutos achei 2 defeitos que a suíte inteira nunca pegou.

O primeiro: todo cadastro por e-mail falhava em silêncio. O ORM (a camada que traduz objeto do código pra linha de tabela) gravava a credencial antes do aluno. A chave estrangeira recusava a inserção. O erro virava 202 Accepted com "e-mail já existe", a resposta certa pra não revelar se a conta existia, só que acontecendo pelo motivo errado.

O segundo era pior. 4 rotas não isolavam um aluno do outro. Com um token inválido, uma delas devolvia a transcrição e o áudio de outro aluno, como se o id na URL bastasse.

A causa dos dois era a mesma. O mundo dos testes tinha um aluno só. Uma fixture (dado de teste pronto antes de rodar) gravava o aluno antes da credencial. Outra sobrescrevia a identidade de quem pede em todas as rotas. Com um usuário só, autorização nunca é exercitada de verdade. Ela só aparece quando existe um segundo aluno pra vazar pra.

Corrigi movendo a checagem de dono pro caso de uso. O campo requester_id virou obrigatório em todo comando, e o mypy recusa a chamada sem ele. Recurso de outro aluno agora responde o mesmo 404 de um recurso que não existe. Toda rota sensível ganhou dois testes: sem token dá 401, outro aluno dá 404.

Gates verdes provam que o código é coerente consigo mesmo. Não provam que o produto funciona.

Você testa autorização com mais de um usuário no seu time, ou confia que o token certo sempre chega primeiro?
