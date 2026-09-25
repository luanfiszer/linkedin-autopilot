# voice.md

Perfil de voz do Luan. Toda skill `li-*` e a rotina semanal leem este arquivo.

Regra: campo marcado **[NÃO INFORMADO]** não existe. Não preencha com
suposição. Post que depende dele leva `{{...}}` e o Luan completa no PR.

Fontes: PDF do perfil do LinkedIn e respostas do Luan (25/09/2026). Ainda
não há posts publicados.

---

## Quem eu sou

- **Nome:** Luan Fiszer
- **O que eu faço, em uma frase:** Desenvolvedor backend .NET. Construo
  microsserviços em ASP.NET Core (autenticação, mensageria, APIs) e modernizo
  sistemas legados.
- **Onde:** MEDGRUPO, desde novembro de 2025. Antes: PROVER Soluções em TI
  (out/2024 a nov/2025, júnior; set a out/2024, trainee). Rio de Janeiro.
- **Formação:** Engenharia (Sistemas e Computação) na UERJ, em andamento.
- **Objetivo com o LinkedIn:** as duas coisas: atrair vagas e recrutadores e
  construir autoridade entre devs. Nada é vendido.
- **Para quem eu escrevo:** o público de tecnologia e desenvolvimento de
  software. Na prática, escreva cada post para **um dev backend, de júnior a
  pleno, que quer sair do CRUD e trabalhar com sistemas distribuídos em
  produção**, principalmente .NET/C#. Recrutadores e tech leads leem os mesmos
  posts como prova de que eu sei fazer. O público não é limitado; o leitor de
  cada post é que é um só.

## Como eu falo

- **Posts meus que soam como eu:** [NÃO INFORMADO] (ainda não posto)
- **Tom:** leve, limpo e natural, como quem conta pra um colega dev o que
  aconteceu na semana. Pode ter um pouco de humor e autoironia ("passei duas
  horas culpando o Redis; era fuso horário"). Nada de tom de palestra ou de
  relatório. Falo direto com a pessoa, em segunda pessoa ("você").
- **Estrutura (obrigatória):**
  - linha 1: o gancho, sozinho, até ~140 caracteres;
  - parágrafos de 1 a 3 linhas, com linha em branco entre eles;
  - uma ideia por parágrafo; nada de bloco de texto corrido;
  - arco: gancho → o que aconteceu → o que eu fiz → o que aprendi → pergunta;
  - quando houver passos ou itens, lista com hífen (máximo 4 itens, tamanhos
    diferentes);
  - termo técnico explicado em meia frase na primeira vez, pra quem é júnior
    acompanhar;
  - entre 800 e 1.600 caracteres na maioria dos posts.
- **Palavras que eu uso:** vocabulário simples. "pra" e "a gente" podem
  aparecer. Termos técnicos em inglês quando é assim que se fala no dia a dia
  (Outbox Pattern, N+1, tracing, deploy).
- **Palavras que eu nunca usaria:** palavrão; gíria muito informal ("tô",
  "tá", "né", "cê", "mano", "bora", "pô"); vocabulário rebuscado ("outrossim",
  "destarte", "primordial"); jargão de coach ("mindset", "virar a chave",
  "jornada", "sair da zona de conforto"); tudo que o `slop_pt.json` marca.
- **Tamanho das frases:** mistura. A maioria curta e direta, algumas mais
  longas quando explicam algo técnico.
- **Palavrão:** não.
- **Emoji:** quase nunca. No máximo 1 por post, e nunca em lista.
- **Nada com cara de IA:** sem "Não é sobre X, é sobre Y", sem tríades, sem
  "O resultado?" sozinho numa linha, sem parede de hashtags (0 a 3 no fim).
- **Fechamento:** uma pergunta específica pro leitor sobre o assunto do post,
  que dê pra responder com a experiência dele.

## Minhas posições

Coisas em que eu acredito e que parte do meu público discorda.

1. **Programar com agente de IA exige mais disciplina, não menos.** O agente
   não lembra o que foi combinado na sessão anterior, então decisão tem que
   estar escrita (ADR), regra de arquitetura tem que quebrar o build e
   comportamento tem que ter teste. Regra que depende de lembrar erode.
   *Base:* projeto pessoal construído sessão a sessão com agente, com dezenas
   de ADRs e um registro de aprendizados.
2. **Publicar evento logo depois de salvar no banco é bug esperando
   acontecer. Outbox não é exagero.** Se o banco confirma e a publicação falha
   (ou o contrário), o sistema fica inconsistente sem ninguém perceber.
   *Base:* implementei Outbox Pattern com processamento em background e
   RabbitMQ no trabalho (sem citar a empresa).
3. **Otimização sem medição é chute.** Medir antes, e ter coragem de desfazer
   uma decisão quando o número desmente a premissa.
   *Base:* no projeto pessoal, aprovei uma otimização (prompt caching) e
   derrubei no mesmo dia: a medição mostrou que o prefixo mínimo pra cache
   engatar era 4.096 tokens, não os 1.024 que eu tinha assumido, e uma conversa
   real nunca chegava lá. No trabalho, uso tracing (Jaeger) pra achar gargalo
   antes de mexer.

Outras ideias que viram posts de TEACH (não são posições centrais): teste de
adapter contra banco de verdade (testcontainers) em vez de banco em memória;
banco como fonte da verdade e fila/cache como aceleradores (idempotência numa
coluna do Postgres em vez de Redis); não decidir arquitetura sobre código que
ainda não existe.

## Fora dos limites

- **Assuntos sobre os quais eu não posto:** [NÃO INFORMADO]
- **Projeto pessoal (app de inglês):** pode ser usado à vontade, com números e
  detalhes técnicos, mas **sem o nome do projeto**. Chame de "meu projeto
  pessoal" ou "um app que estou construindo" e diga do que se trata.
- **Empresa atual (MEDGRUPO):** posso falar da **experiência e da tecnologia**,
  de forma rasa, nunca da empresa. Regras:
  - não cite o nome da empresa, de produtos, serviços, repositórios, classes,
    tabelas, endpoints ou filas (a validação bloqueia os termos de
    `linkedin/blocklist.txt`);
  - nada de código da empresa, nem trecho adaptado; exemplos de código, se
    houver, são genéricos e escritos do zero;
  - nada de números internos (usuários, volume, tempo de resposta, custos);
  - segurança só no nível do conceito ("MFA", "migrar hash de senha antigo");
    nunca como a proteção funciona por dentro (regras de geofencing, como a VPN
    é detectada, algoritmos e parâmetros);
  - nada sobre alunos, clientes, colegas ou decisões internas.
  - Formato certo: "Esta semana implementei Outbox Pattern num consumer
    RabbitMQ; o problema era evento perdido quando o banco confirmava e a
    publicação falhava." Formato errado: qualquer coisa que permita a alguém
    de fora saber qual sistema, qual regra ou qual número.
- **Afirmações que não posso fazer:** [NÃO INFORMADO]

## Provas que posso usar

Tudo abaixo está no perfil público. Nada além disso pode virar número num post.

- **PROVER, sistema de tickets:** fiz do zero, em C# e ASP.NET MVC, um sistema
  interno de gestão de tickets que substituiu uma ferramenta paga. O custo
  operacional caiu 97,5% e sobrou só o custo de infraestrutura. Tinha
  autenticação, controle de acesso e histórico de atendimentos.
- **PROVER, performance:** refatorei consultas críticas no SQL Server (EF Core
  e LINQ), eliminei N+1 e a latência das requisições caiu 15%.
- **PROVER, chat em legado:** fiz chat em tempo real com Long Polling e AJAX
  num ambiente legado sem suporte a WebSockets.
- **Trainee:** passei numa seleção técnica com etapas eliminatórias (lógica,
  console, APIs). O desafio final foi uma API REST de locadora de veículos com
  Clean Architecture, apresentada ao vivo para a banca.
- **MEDGRUPO (sem números):**
  - microsserviços de autenticação: JWT, MFA via QR Code, geofencing, detecção
    de VPN, migração de hashes legados para criptografia moderna;
  - eventos com RabbitMQ e Outbox Pattern;
  - migração de monolito para microsserviços com DMS e DBT;
  - otimização de queries no PostgreSQL com EF Core;
  - tracing com Jaeger, métricas com Prometheus e Grafana.
- **Números do MEDGRUPO:** não usar (política acima).
- **Projeto pessoal (sem citar o nome):** um app de treino de inglês por
  conversa de áudio com um professor de IA. O aluno fala, o áudio é
  transcrito, um LLM responde e corrige, e a resposta volta em voz. Backend em
  Python (eu vim do .NET e aprendi Python nele), app mobile em React
  Native/Expo, Postgres, Redis, fila com worker, SSE. Construído sessão a
  sessão com agente de IA, com dezenas de ADRs. Começou no WhatsApp via Twilio
  e migrou pra app próprio quando o canal virou teto (sem UI, só turn-based,
  webhook público). Histórias com número:
  - prompt caching derrubado pela medição (4.096 tokens medidos contra 1.024
    assumidos);
  - idempotência do upload numa coluna do Postgres em vez de Redis `SETNX`,
    por causa de uma janela de crash entre criar o registro e enfileirar;
  - testes de persistência contra Postgres real em container.
- **Diário técnico semanal:** `linkedin/ideias.md` recebe toda semana um resumo
  já sanitizado dos meus commits (ver "Coleta semanal" no `CLAUDE.md`). É a
  principal fonte de histórias novas.
