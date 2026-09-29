# Prompt para montar o LinkedIn Autopilot para outra pessoa

Clone este repositório, abra o Claude Code na pasta do clone e cole tudo o que
está abaixo da linha.

---

Este repositório é um clone do "LinkedIn Autopilot" de outra pessoa (o Luan).
Quero adaptar tudo para o **meu** perfil do LinkedIn. Leia o `CLAUDE.md`, o
`README.md`, os `scripts/`, os `tests/` e o `.github/workflows/` antes de
começar, para entender o sistema. Monte um plano com etapas e vá executando uma
por vez, me avisando no fim de cada uma.

## Como o sistema funciona (resumo)

1. **Coleta semanal (no meu computador):** uma tarefa agendada do Claude lê os
   meus commits da semana e escreve notas técnicas **sanitizadas**, sem nada
   da empresa, em `linkedin/ideias.md`.
2. **Rotina semanal (na nuvem, segunda de manhã):** uma rotina do Claude Code
   lê `linkedin/voice.md` e `linkedin/ideias.md`, escreve 4 posts, humaniza e
   pontua cada um, gera imagem quando faz sentido e abre um PR com os posts em
   `queue/approved/`.
3. **Eu reviso o PR e dou merge.** O merge é a aprovação.
4. **GitHub Actions**, a cada 30 min, publica pela API oficial do LinkedIn o
   post cujo horário chegou e o move para `queue/published/`.

## Regras que não podem ser quebradas

- Nunca commitar tokens ou segredos. `.env` fica fora do git e, no Actions,
  eles vêm de GitHub Secrets.
- Nada de automação de navegador, scraping ou API não oficial do LinkedIn.
- Nada de auto-merge. Você nunca dá merge nem publica sem me perguntar.
- Não invente nada sobre mim. O que eu não informar fica marcado como
  `[NÃO INFORMADO]` no voice, e os posts usam `{{...}}`.
- Mantenha o `LICENSE` (MIT) e o crédito ao autor original das skills (Jake
  Schincariol) em `.claude/skills/LICENSE-linkedin-agent`.

## Etapa 1: perguntas (faça todas de uma vez, antes de mexer em qualquer coisa)

1. Meu nome, como aparece no LinkedIn.
2. Onde trabalho hoje, e se posso citar a empresa nos posts.
3. Caminho, no meu computador, das pastas com os **repositórios de trabalho** e
   com os **repositórios pessoais** (para a coleta semanal).
4. Nomes/e-mails com que eu commito (rode `git log --format='%an <%ae>' | sort -u`
   nos meus repositórios e me mostre, pra eu confirmar quais são meus).
5. Termos que **nunca** podem aparecer num post: nome da empresa, dos
   produtos, dos sistemas internos, de clientes, e o nome de projetos pessoais
   que eu não queira citar.
6. Nome que quero para o repositório no GitHub (ele vai ser **privado**).
7. Dia e hora da coleta semanal (padrão: sexta 17h, no meu computador) e da
   rotina (padrão: segunda 9h, na nuvem). Meu fuso horário.

## Etapa 2: limpar os dados do Luan

O clone tem dados pessoais do Luan (voice, notas de trabalho, posts, log) e o
histórico git carrega tudo isso. Faça, nesta ordem:

1. Apague o histórico e comece do zero: `rm -rf .git && git init -b main`.
2. Apague todo o conteúdo de `queue/approved/` e `queue/published/`, mantendo
   os `.gitkeep`.
3. Apague as imagens de `media/fotos/` e `media/fotos/fontes/`, mantendo o
   `README.md` e os `.gitkeep`.
4. Recrie `linkedin/log.md` só com o cabeçalho da tabela e `linkedin/plan.md`
   como "Ainda não gerado".
5. Recrie `linkedin/ideias.md` só com a explicação do topo e uma seção
   `## Esta semana` vazia.
6. Recrie `linkedin/voice.md` com a mesma **estrutura** de seções do atual
   (Quem eu sou, Como eu falo, Minhas posições, Fora dos limites, Provas que
   posso usar), com todos os campos `[NÃO INFORMADO]` e sem nenhuma informação
   do Luan. As regras genéricas de estilo e de "nada com cara de IA" podem
   ficar.
7. Reescreva `linkedin/blocklist.txt` só com o comentário do topo e os termos
   que eu te passar na etapa 1.
8. Confirme que não existe `.env` e que `exemplos/` só tem o post de teste.
9. Procure e troque toda referência pessoal: rode
   `grep -rniE 'luan|fiszer|medgrupo|medsoft|voicecoach|prover|uerj|Documents/' --exclude-dir=.venv .`
   e ajuste cada ocorrência no `CLAUDE.md`, no `README.md`, nos comentários de
   `scripts/` e em `media/fotos/README.md`. No `CLAUDE.md`, a seção "Coleta
   semanal" precisa usar **os meus** caminhos e **os meus** nomes de autor no
   filtro `git log --all --no-merges -i -E --author="<regex dos meus nomes>"`.
   O `-E` é obrigatório: sem ele, o `?` do regex vira literal e a coleta não
   encontra nada.
10. Rode o grep de novo e me mostre que não sobrou nada.

## Etapa 3: ambiente e testes

1. Python 3.11+ num `.venv` (use `uv` se existir):
   `requirements.txt`, `requirements-dev.txt` e `requirements-images.txt`.
2. Rode `python -m pytest -q`. Tudo tem que passar.
3. Rode `python scripts/li_publish.py --file exemplos/2026-09-26-1000-teste-conexoes.md --dry-run`
   e me mostre a saída.
4. Commit inicial: "chore: LinkedIn Autopilot adaptado para <meu nome>".

## Etapa 4: GitHub

1. Confira `gh auth status`. Crie o repositório **privado** com o nome da
   etapa 1 e dê push:
   `gh repo create <nome> --private --source . --remote origin --push`.
2. Não crie proteção de branch que exija PR na `main`: o workflow de
   publicação precisa dar push direto na `main` para mover os posts publicados.
3. Rode o workflow "Publicar no LinkedIn" na mão (`gh workflow run publish.yml`)
   e confira que ele termina com "Nada a publicar".

## Etapa 5: app e token do LinkedIn (eu faço a parte do navegador)

Me guie, passo a passo:

1. Em https://www.linkedin.com/developers/apps, criar o app. O LinkedIn exige
   associar o app a uma Página; se eu não tiver, uma página simples serve.
2. Na aba **Products**, adicionar **Share on LinkedIn** e **Sign In with
   LinkedIn using OpenID Connect**.
3. Na aba **Auth**, em *Authorized redirect URLs*, adicionar exatamente
   `http://localhost:8000/callback`. Sem isso, a autorização dá "The
   redirect_uri does not match the registered value".
4. Eu preencho `LINKEDIN_CLIENT_ID` e `LINKEDIN_CLIENT_SECRET` num `.env`,
   copiado do `.env.example`. Não me peça o secret no chat.
5. Rode em background `python -u scripts/get_token.py --gh-secrets --save-env`,
   me avise para autorizar no navegador e espere. Esse comando grava o token no
   `.env` e nos secrets do GitHub sem imprimir o valor.
6. Me diga a data de expiração (normalmente 60 dias) e como renovar.

## Etapa 6: meu perfil de voz

1. Peça o PDF do meu perfil do LinkedIn (Perfil > Mais > Salvar como PDF) e/ou
   3 posts meus.
2. Rode a skill `li-profile`, me dê a nota e as reescritas sugeridas.
3. Me pergunte, de uma vez: objetivo com o LinkedIn, para quem escrevo, o que
   posso contar do trabalho atual e o que não posso, tom, emoji e palavras que
   não uso.
4. Para as **posições**, olhe os meus repositórios (só leitura: mensagens de
   commit, ADRs, READMEs, nunca código da empresa) e me proponha de 5 a 7
   posições, cada uma com a evidência que a sustenta. Eu escolho 3.
5. Preencha o `linkedin/voice.md` só com o que eu confirmei. O resto fica
   `[NÃO INFORMADO]`.
6. Commit e push.

## Etapa 7: agendamentos

1. **Coleta semanal (local):** crie uma tarefa agendada do Claude no meu
   computador, no dia e hora da etapa 1, que rode a seção "Coleta semanal" do
   `CLAUDE.md` neste repositório. O prompt da tarefa precisa ser completo:
   caminho do repositório, repetir as regras de compliance (repositórios de
   trabalho só leitura, nada de código, nome de sistema ou número interno
   nas notas), conferir a blocklist com
   `python scripts/validate_queue.py --check-text linkedin/ideias.md`,
   commitar só `linkedin/ideias.md` e dar push. Ela só roda com o app aberto.
2. **Rotina semanal (nuvem):** eu preciso conectar o GitHub em
   https://claude.ai/connect-github, com acesso ao repositório novo. Depois,
   crie a rotina (via `/schedule`) no dia e hora da etapa 1, convertendo para
   UTC, com o prompt "rodar rotina semanal" + um resumo dos passos da seção
   "Rotina semanal" do `CLAUDE.md` e a lista do que é proibido (merge,
   publicar, inventar, citar termos da blocklist).

## Etapa 8: teste de ponta a ponta

1. **Post de teste**: só com o meu "pode publicar" explícito.
   `python scripts/li_publish.py --file exemplos/2026-09-26-1000-teste-conexoes.md`
   publica com visibilidade CONNECTIONS. Se eu pedir, apague logo depois com
   `DELETE https://api.linkedin.com/rest/posts/{urn codificado}` (headers
   `LinkedIn-Version` e `X-Restli-Protocol-Version: 2.0.0`). Registre o
   resultado no log e no README.
2. Rode a coleta uma vez e me mostre as notas.
3. Dispare a rotina uma vez e revise o PR que ela abrir antes de me mostrar.
   Procure três coisas:
   - **fatos inventados**: falas entre aspas, cenas, justificativas ou "eu
     usava" quando era só um plano. Toda frase precisa de fonte no voice ou
     nas notas;
   - **truques no detector**: algarismo solto ("2 operações") no lugar de
     detalhe técnico real;
   - **tom e estrutura**: parágrafos curtos, uma ideia por parágrafo, pergunta
     no fim.

   Corrija o que achar e me passe o link do PR.

## Ao terminar

Me entregue:

1. O que foi feito.
2. O que ficou pendente do meu lado (app, secrets, GitHub conectado ao Claude,
   fotos).
3. A data de renovação do token.
4. O link do repositório, da rotina e do PR de teste.
