---
scheduled_at: 2026-10-28T07:45:00-03:00
visibility: PUBLIC
type: OPINION
hook: "#7 The Callout"
human_score: 72.2
image: "media/fotos/gerado-spec-antes-codigo.png"
image_alt: "Infográfico: sem spec, o caso de borda aparece em produção; com proposta, design e spec no formato OpenSpec, o caso que ia quebrar aparece antes do primeiro commit"
image_request: "Foto de um rascunho seu, à mão, no caderno ou quadro, listando casos de borda de uma correção antes de escrever o código. Sem nada do trabalho."
---
Pular o design numa correção "pequena" é a parte mais cara de um bug grande.

Eu escrevo a spec antes do código. Mesmo numa correção que parece simples.

Essa semana tive mais de uma correção que não era trivial. Pra cada uma, escrevi três documentos em Markdown antes de tocar no código, no formato OpenSpec: uma proposta explicando o porquê, um design com as decisões e uma spec descrevendo o comportamento esperado, caso de borda por caso de borda.

Isso custa tempo antes de qualquer linha de código rodar.

Numa dessas specs, revisando os casos de borda no papel, achei um caso que ia quebrar.

Nenhum teste tinha pegado ainda, porque o código que testaria aquele caso nem existia.

A tentação de pular essa etapa é real: o bug parece pequeno, a correção parece óbvia, e escrever três documentos pra um fix de uma linha parece burocracia.

Só que "parece óbvia" é exatamente o tipo de frase que eu desconfio.

Se fosse tão óbvia, o bug não teria chegado até ali.

É a mesma lógica de escrever um ADR antes de decidir a arquitetura: a decisão fica em texto, revisável no PR, não escondida de quem só olha o CI passar. Vale tanto numa correção em .NET quanto em Python.

Decidir arquitetura em cima de código que ainda não existe é apostar. Escrever o design antes transforma a aposta numa lista de casos que dá pra checar, um por um, no roteiro de validação em homologação, antes do primeiro commit no Git.

Qual foi a última vez que uma correção "rápida" te custou mais tempo do que um design de dez minutos teria custado?

#Arquitetura #BackEnd