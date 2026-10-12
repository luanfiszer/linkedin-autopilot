---
scheduled_at: 2026-10-21T07:45:00-03:00
visibility: PUBLIC
type: OPINION
hook: "#18 Unpopular Rule"
human_score: 76
image: "media/fotos/gerado-remendo-persistido.png"
image_alt: "Infográfico: lado errado marca o dado gravado e precisa de migração; lado certo grava a entrada intacta e decide na leitura, num Calculator"
image_request: "Foto de um rascunho seu, à mão, no caderno ou quadro, mostrando a separação entre 'dado gravado' e 'regra aplicada na leitura'. Sem nada do trabalho, só o esquema."
---
Eu não deixo um remendo temporário tocar o dado que fica salvo. Nunca.

Migração pra desfazer é a prova de que ele nunca foi temporário.

A situação: um serviço de fora mandava um veredito inconsistente enquanto corrigia o problema do lado dele. Eu precisava de uma checagem redundante no meu lado, só pra segurar a barra nesse meio-tempo.

A tentação óbvia: marcar o campo errado direto no registro gravado, e tirar a marca depois.

Eu separei as duas coisas.

O dado de entrada entra puro, do jeito que chegou do serviço de fora, e fica assim: na prática, um Value Object, imutável, sem setter. Intacto, pra auditoria.

A regra que decide o veredito final não mora no Repository. Mora na leitura, dentro de um Calculator isolado do resto do fluxo, no mesmo estilo que uso em C# e .NET pra qualquer regra de negócio que não deveria vazar pra fora de um lugar só. Não é Strategy. Não é Decorator. Não é Factory, nem Builder, nem Singleton escondido em algum canto. É só separar o que chegou do que eu decido.

Tinha um motivo técnico extra. Esse eu só vi lendo o código com calma de novo: o mesmo objeto é compartilhado por referência em vários trechos do documento. Marcar ele na gravação vazaria a marca pra todo lugar que aponta pra aquele objeto. Um bug puxando outro.

Quando o serviço de fora corrigir o problema dele, a saída é apagar o Calculator. Um commit.

Sem migration. Sem campo zumbi. Sem "lembrar de desligar isso depois" numa reunião de sexta.

Remendo provisório que entra no dado persistido quase nunca sai. Ele fica, um "só por enquanto" que ninguém tem coragem de remover porque alguma outra parte do sistema já passou a depender dele, em silêncio.

No seu sistema, qual remendo "temporário" já passou de um ano? O que quebraria se você removesse ele hoje?

#Arquitetura #BackEnd
