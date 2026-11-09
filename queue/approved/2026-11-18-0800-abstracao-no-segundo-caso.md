---
scheduled_at: 2026-11-18T08:00:00-03:00
visibility: PUBLIC
type: OPINION               # PROOF | OPINION | TEACH | STORY | OFFER
hook: "#18 The Unpopular Rule"
human_score: 70.4
image: "media/fotos/gerado-abstracao-segundo-caso.png"
image_alt: "Diagrama: primeiro caso de uso vira código concreto; a abstração só nasce quando aparece o segundo caso"
image_request: "Foto de um rascunho à mão (caderno ou quadro) com duas versões do mesmo trecho, a direta e a abstraída, ou print do histórico de commits do seu projeto pessoal mostrando a abstração chegando depois do código direto. Sem nome do projeto."
---
Eu não desenho arquitetura pra código que ainda não existe. Nunca.

Parece disciplina. É economia.

Toda abstração criada hoje pra um caso hipotético precisa ser mantida, testada e explicada pra quem entra no time daqui a um ano, mesmo que esse caso nunca apareça.

Já vi uma IRepository com um único implementador, criada "pra garantir flexibilidade" antes de existir um segundo banco. Já vi uma Strategy Pattern pronta pra uma variação que nunca chegou, em .NET e em outras linguagens.

Três anos depois, ninguém lembrava por que aquilo existia. Remover dava mais medo do que manter.

Minha regra: a abstração nasce no segundo caso de uso real, não no primeiro. Até lá, classe concreta.

Isso não é desculpa de YAGNI pra fazer mal feito, nem contradiz SOLID. É regra contra pagar hoje, em complexidade, por um futuro que pode nunca chegar, ou chegar diferente do que você imaginou.

Você já teve que desfazer uma abstração que ninguém usava, só pra conseguir entender o código de novo?
