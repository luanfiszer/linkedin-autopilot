# LinkedIn Autopilot

Publicação automática no LinkedIn do meu perfil pessoal, com aprovação humana
em todo post.

```
segunda              você (celular)            GitHub Actions, a cada 30 min
Claude agendado  ->  revisa o PR, edita  ->    publica o post cujo horário
escreve 4 posts      e dá merge                chegou e move para published/
e abre um PR         (merge = aprovação)       (1 por execução)
```

- **Escrita:** as skills `li-*` do plugin
  [linkedin-agent](https://github.com/Jakeschincariol/linkedin-agent-skill)
  (MIT, © Jake Schincariol), com o humanizador adaptado para português.
- **Aprovação:** só o que chega na `main` por merge é publicado. Sem auto-merge.
- **Publicação:** API oficial do LinkedIn (Posts API, escopo `w_member_social`).
  Nada de automação de navegador ou scraping.
- **Manual:** comentários, respostas e métricas. A API self-serve não permite
  automatizar isso.

## Setup

Você precisa de Python 3.11+, de uma conta no GitHub e da CLI `gh` (opcional).

### 1. App no LinkedIn Developers

1. Entre em <https://www.linkedin.com/developers/apps> e clique em **Create app**.
   O LinkedIn exige associar o app a uma **Página do LinkedIn**. Se você não
   tem uma, crie uma página simples (pode ser com o seu nome ou marca); ela não
   aparece nos posts, que saem no seu perfil pessoal.
2. Na aba **Products**, adicione:
   - **Share on LinkedIn** (dá o escopo `w_member_social`)
   - **Sign In with LinkedIn using OpenID Connect** (dá `openid` e `profile`)
3. Na aba **Auth**, em **Authorized redirect URLs for your app**, adicione:
   `http://localhost:8000/callback`
4. Copie o **Client ID** e o **Primary Client Secret** da aba Auth.

### 2. Gerar o token

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # preencha LINKEDIN_CLIENT_ID e LINKEDIN_CLIENT_SECRET
python scripts/get_token.py
```

O navegador abre, você autoriza, e o script imprime o `LINKEDIN_ACCESS_TOKEN`,
o `LINKEDIN_PERSON_URN` (`urn:li:person:...`) e a data de expiração
(normalmente 60 dias). Ele não grava o token em nenhum arquivo.

### 3. Secrets no GitHub

No repositório: **Settings > Secrets and variables > Actions > New repository
secret**. Cadastre:

| secret | valor |
| --- | --- |
| `LINKEDIN_ACCESS_TOKEN` | o token impresso pelo `get_token.py` |
| `LINKEDIN_PERSON_URN` | `urn:li:person:...` |

Atalho: `python scripts/get_token.py --gh-secrets` faz a autorização e grava
os dois secrets direto pelo `gh`, sem imprimir o token. Ou pela CLI, colando
o valor quando pedir:

```bash
gh secret set LINKEDIN_ACCESS_TOKEN
gh secret set LINKEDIN_PERSON_URN
```

Opcional: a variável de repositório `LINKEDIN_VERSION` (em *Variables*, não em
*Secrets*) sobrescreve a versão da Posts API. O padrão é `202609`. O LinkedIn
desativa cada versão depois de mais ou menos um ano, então atualize esse valor
uma vez por ano.

### 4. Configurações do repositório

- **Não** exija Pull Request nem status check para push na `main` (branch
  protection ou ruleset): o workflow de publicação dá push direto na `main`
  para mover o post para `queue/published/` e atualizar o log, e seria
  bloqueado. A aprovação continua sendo o merge do PR da semana.
- **Não** ative "Allow auto-merge" (Settings > General).
- Em **Settings > Actions > General > Workflow permissions**, deixe como está
  (o workflow pede `contents: write` e `issues: write` sozinho). Só mude para
  "Read and write" se o push do bot falhar com erro 403.

### 5. Rotina semanal do Claude

Crie uma tarefa agendada do Claude Code (por exemplo com `/schedule`) que roda
toda segunda de manhã neste repositório com o prompt:

```
rodar rotina semanal
```

O `CLAUDE.md` explica à sessão exatamente o que fazer. A sessão precisa de
permissão para dar push numa branch e abrir PR; ela nunca dá merge.

Durante a semana, anote fatos e ideias em `linkedin/ideias.md`. A rotina só
escreve sobre o que está lá ou no `linkedin/voice.md`, e deixa `{{...}}` quando
falta algum dado.

## Como aprovar posts

1. Chega um PR "Posts da semana de DD/MM" com a tabela da semana.
2. Abra os arquivos em `queue/approved/`. Para editar pelo celular: no app ou
   no site do GitHub, **Files changed > ... > Edit file**.
3. Preencha todo `{{...}}`. O check **Validar fila** fica vermelho até não
   sobrar nenhum.
4. Quer tirar um post? Apague o arquivo no PR. Mudar o horário? Edite o
   `scheduled_at` (sempre com `-03:00`).
5. Check verde, **Merge**. Pronto: cada post sai no horário dele.

Para cancelar um post já aprovado e ainda não publicado, apague o arquivo de
`queue/approved/` na `main`.

A validação exige: frontmatter válido, `scheduled_at` no futuro e com fuso,
400 a 3.000 caracteres, nenhum `{{...}}`, nota ≥ 70 no
`detect.py --lang pt` e no máximo 1 post por dia.

## Renovar o token (a cada ~60 dias)

O token self-serve dura 60 dias e não tem refresh token. Quando ele expira, o
workflow abre a issue **"Token do LinkedIn expirou"** (uma só, atualizada a
cada falha) e os posts ficam esperando na fila; nada se perde.

```bash
python scripts/get_token.py --gh-secrets
```

Depois rode o workflow na mão (**Actions > Publicar no LinkedIn > Run
workflow**). Quando ele voltar a publicar, a issue fecha sozinha. Dica: anote
na agenda a data de expiração que o `get_token.py` imprime.

## Post de teste

Já existe um post de teste com visibilidade `CONNECTIONS` (só suas conexões
veem) em `exemplos/`, fora da fila de propósito: nada ali é publicado pelo
Actions. Publique direto com `--file`, localmente, com o token no `.env`:

```bash
python scripts/li_publish.py --file exemplos/2026-09-26-1000-teste-conexoes.md --dry-run
python scripts/li_publish.py --file exemplos/2026-09-26-1000-teste-conexoes.md
```

O `--file` ignora o `scheduled_at` e a validação. Se deu certo, o arquivo vai
para `queue/published/` com o `posted_urn` e o `posted_via`, e o
`linkedin/log.md` ganha uma linha. Commite essas mudanças.

### Qual endpoint é usado

O publicador tenta primeiro `POST https://api.linkedin.com/rest/posts` (Posts
API, com `LinkedIn-Version: 202609` e `X-Restli-Protocol-Version: 2.0.0`). Se
esse endpoint recusar o token self-serve (403, 404 ou 426), ele tenta
`POST https://api.linkedin.com/v2/ugcPosts`. O endpoint que funcionou fica
gravado no campo `posted_via` de cada post publicado.

> **Verificado em 25/09/2026:** o `rest/posts` com `LinkedIn-Version: 202609`
> aceitou o token self-serve (app com "Share on LinkedIn") e devolveu
> `urn:li:share:...`. O fallback `v2/ugcPosts` não foi necessário. O mesmo token
> também apaga posts (`DELETE /rest/posts/{urn}` respondeu 204).

### Little text

O campo `commentary` da Posts API usa o formato "little text": os caracteres
`\ | { } @ [ ] ( ) < > # * _ ~` precisam de barra invertida, senão o post é
cortado ou recusado. O publicador escapa tudo sozinho e converte hashtags
(`#vendas`, `#TransformaçãoDigital`) para o template
`{hashtag|\#|vendas}`, então elas continuam clicáveis. Escreva o post
normalmente, sem escapar nada.

## Segurança contra post duplicado

- Post com `posted_urn` no frontmatter nunca é publicado de novo.
- Antes de chamar a API, o publicador grava `publish_attempted_at`. Se o
  LinkedIn não responder direito (timeout, erro 5xx), o marcador fica, o
  arquivo não é tentado de novo e abre a issue **"Publicação incerta no
  LinkedIn"** com as instruções.
- O workflow tem `concurrency` para nunca rodar duas vezes em paralelo.
- No máximo 1 post por execução, então uma fila atrasada não sai de uma vez.

## Estrutura

```
.claude/skills/li-*          skills do linkedin-agent (MIT)
.claude/skills/li-human/     humanizador; slop_pt.json é o léxico PT-BR
linkedin/voice.md            perfil de voz
linkedin/ideias.md           fatos e ideias da semana (você escreve)
linkedin/plan.md             plano da semana (a rotina escreve)
linkedin/log.md              log de publicações (o publicador escreve)
queue/approved/              posts aprovados
queue/published/             posts publicados
scripts/get_token.py         OAuth local
scripts/li_publish.py        publicador
scripts/validate_queue.py    validação de PR
tests/                       pytest, com a API mockada
.github/workflows/           publish, validate, tests
CLAUDE.md                    instruções para as sessões do Claude
```

## Desenvolvimento

```bash
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest -q
python scripts/li_publish.py --dry-run
python .claude/skills/li-human/detect.py tests/fixtures/pt_ruim.txt tests/fixtures/pt_bom.txt
```

Custo do Actions: o cron de 30 min roda 48 vezes por dia. Em repositório
público é grátis. Em repositório privado, cada execução conta como 1 minuto,
o que dá uns 1.450 min/mês, dentro dos 2.000 minutos grátis do plano Free.

## Créditos

As skills em `.claude/skills/li-*` são do
[linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill),
de Jake Schincariol, sob licença MIT (cópia em
`.claude/skills/LICENSE-linkedin-agent`). O humanizador em português, os
scripts de publicação e os workflows foram adicionados neste repositório.
