# Imagens dos posts

Todo post sai com imagem. A preferida é sempre uma foto ou print **seu**; a
gerada é só a reserva. A rotina decide post a post:

- **usa** um print ou foto que você já deixou nesta pasta; se não tiver,
- **pede** a você, no PR, exatamente o que mandar (`image_request`) **e** deixa
  uma imagem reserva no post:
  - um diagrama ou um cartão de código genérico (`scripts/gerar_imagem.py`), ou
  - um infográfico desenhado em SVG que explica o post sozinho (passos,
    antes/depois, o detalhe técnico), sem pessoas.

Se você mandar a sua, ela substitui a reserva. Toda imagem gerada é
`gerado-*.png`, com a fonte (YAML, código ou SVG) em `fontes/`.

Nunca: imagem gerada por IA com pessoas ou cena fantasiosa, print falso, imagem da internet.

## Prints

Print de tela (PNG) pode vir direto: celular e Mac não gravam localização em
print. Antes de mandar, confira que não aparece nada do trabalho, nem
notificação, nem nome de outra pessoa. Bons prints: o app do seu projeto
pessoal rodando, testes passando no terminal do projeto pessoal, um trecho de
documentação ou ADR seu, um gráfico de medição.

## Fotos

Foto de celular guarda a localização GPS. Coloque as originais em
`media/entrada/` (essa pasta **não** vai para o GitHub) e rode:

```bash
.venv/bin/python scripts/preparar_fotos.py
```

O script reduz para 2000 px, corrige a rotação e remove os metadados. Depois é
só commitar. Descreva cada uma no `CATALOGO.md` se quiser.

## Ideias de fotos

Fotos simples e reais funcionam melhor que foto de banco de imagem. Algumas
ideias, da mais fácil para a mais trabalhosa:

- o setup de cima (mesa, teclado, monitor, café), com luz natural;
- a mesma mesa à noite, só com a luz da tela;
- o notebook num lugar fora do comum (café, biblioteca da faculdade, viagem);
- mãos no teclado, de lado, com a tela desfocada;
- quadro branco ou caderno com um diagrama rabiscado (fila, eventos, camadas);
- post-its com um fluxo desenhado à mão;
- a tela do seu **projeto pessoal** (terminal, testes passando, app no celular);
- você trabalhando, de costas ou de lado (alguém tira, ou timer do celular);
- a UERJ, a caminho do trabalho ou da aula;
- um livro técnico aberto na mesa.

Tire 10 a 15 de uma vez, na horizontal, com variações. Isso cobre umas 5 semanas.

## Nunca

- tela com código, sistema, dashboard, Slack/Teams/e-mail **do trabalho**;
- crachá, logo ou nome da empresa;
- rosto de colegas sem autorização;
- janela com vista que entregue onde você mora; documentos na mesa.

A rotina recusa fotos com esses problemas, mas o primeiro filtro é você.
