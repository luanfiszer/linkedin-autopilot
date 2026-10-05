---
scheduled_at: 2026-10-14T08:00:00-03:00
visibility: PUBLIC
type: OPINION
hook: "#18 The Unpopular Rule"
human_score: 74.7
image: "media/fotos/gerado-fallback-fecha-codigo.png"
image_alt: "Cartão de código em C# comparando duas versões de uma regra de acesso: a correta termina negando por padrão, a errada termina liberando"
image_request: "Uma foto do seu caderno ou quadro com um fluxo rabiscado à mão (uma cadeia de decisão, um se-então-senão). Sem nada do trabalho, só o rascunho."
---
Eu não escrevo uma regra de permissão cujo último fallback seja liberar o acesso. Nunca.

Numa regra que ajustei essa semana, a permissão de cada tipo de conteúdo vinha de duas fontes: um Dictionary com o valor específico por item (Nullable, porque nem todo tipo tinha entrada ainda), e uma flag global mais grossa, guardada numa classe que chamo de ConfigDeAcesso.

Dava pra resolver com uma cadeia de coalescência. Em C#, isso é o operador `??`: usa o primeiro valor que não for nulo, senão tenta o próximo.

Valor específico, senão o padrão global, senão nega.

A parte que importa não é a sintaxe do .NET. É a ordem.

O último elo da cadeia tem que ser negar, nunca liberar. Assim, quando o GetValueOrDefault não encontra o tipo de conteúdo novo nesse Dictionary, o sistema erra pro lado seguro.

Quem escreve o fallback ao contrário está otimizando pra não quebrar nada hoje. E empurrando uma decisão de segurança pra um bug de amanhã, quando alguém notar que todo Enum de tipo desconhecido entrava liberado.

Na sua última regra de acesso: um caso que ninguém previu libera ou nega por padrão?
