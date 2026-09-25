# LinkedIn Autopilot

Publicação automática no LinkedIn do perfil pessoal do Luan, em português do
Brasil. Fluxo:

1. **Segunda-feira:** uma sessão agendada do Claude recebe "rodar rotina
   semanal", escreve 4 posts e abre um Pull Request que os adiciona em
   `queue/approved/`.
2. **O usuário revisa o PR e dá merge.** O merge é a aprovação. O que não passou
   por merge nunca é publicado.
3. **GitHub Actions** (`.github/workflows/publish.yml`), a cada 30 min, publica
   pela API oficial o post cujo horário chegou (1 por execução) e o move para
   `queue/published/`.
4. Comentários, respostas e métricas são manuais.

## Regras que valem para qualquer sessão

- **Nunca** dê merge, nunca aprove PR, nunca ative auto-merge.
- **Nunca** publique diretamente: não rode `scripts/li_publish.py` sem
  `--dry-run`, não chame a API do LinkedIn, não mexa em `queue/published/`.
- **Nunca** commite tokens ou segredos. `.env` fica fora do git; no Actions
  eles vêm de GitHub Secrets.
- Nada de automação de navegador, scraping ou API não oficial do LinkedIn.
- **Nunca invente** números, clientes, nomes, resultados ou histórias. Todo
  fato tem que vir de `linkedin/voice.md`, `linkedin/ideias.md`,
  `linkedin/log.md` ou `queue/published/`. Se faltar um dado, escreva
  `{{seu número}}` (ou `{{nome do cliente}}`, `{{o que aconteceu}}`) e avise na
  descrição do PR. A validação do PR falha de propósito até o usuário
  preencher.
- Mantenha `.claude/skills/LICENSE-linkedin-agent` e o crédito ao autor
  original das skills (Jake Schincariol, MIT).

## Rotina semanal

Quando receber **"rodar rotina semanal"**, faça exatamente isto, em ordem.

### 0. Ambiente

```bash
python3 -m pip install -q -r requirements.txt   # requests, python-dotenv, pyyaml
git checkout main && git pull
```

A **semana-alvo** é a semana de segunda a domingo que começa na **próxima
segunda-feira** depois de hoje (se hoje é segunda, 2026-09-28, a semana-alvo
começa em 2026-10-05). Assim o usuário tem uma semana para revisar.

### 1. Ler o contexto

- `linkedin/voice.md`: voz, público, posições, provas que podem ser usadas, o
  que é proibido. Campos marcados `[NÃO INFORMADO]` não existem: não preencha.
- `linkedin/ideias.md`: fatos e ideias que o usuário anotou durante a semana e
  o **diário técnico** gerado pela coleta semanal (seção abaixo). É a
  principal fonte de posts novos. Posts sobre o trabalho atual seguem as
  regras de "Fora dos limites" do `voice.md`: tecnologia e experiência, nunca
  a empresa, seus sistemas ou números.
- `linkedin/log.md` e os arquivos de `queue/published/`: o que já saiu. Não
  repita tema, gancho ou história das últimas duas semanas.
- `queue/approved/`: o que já está agendado. Não marque 2 posts no mesmo dia.

### 2. Planejar

Rode a skill `/li-plan` para a semana-alvo e salve o resultado em
`linkedin/plan.md` (sobrescreva). Como ninguém vai responder perguntas, tire as
respostas de `voice.md` e `ideias.md`; o que faltar vira `{{...}}` no plano.

O plano tem 4 posts com este mix: **PROOF, OPINION, TEACH e (STORY ou OFFER)**,
nunca dois do mesmo tipo seguidos. Horários no fuso **America/Sao_Paulo**
(`-03:00`), no máximo **1 post por dia**. Padrão da skill: terça a quinta,
7h30-9h30; segunda à tarde e sexta de manhã como segunda opção.

### 3. Escrever os 4 posts

Para cada slot do plano, rode a skill `/li-post`, **em português do Brasil e na
voz do usuário**. Os ganchos de `.claude/skills/li-post/hooks.json` estão em
inglês: use a estrutura, escreva em português natural. Entre 400 e 3.000
caracteres. Sem markdown (o LinkedIn não renderiza `**negrito**`).

### 4. Humanizar e pontuar

Para cada post, com o texto num arquivo temporário (fora do repo):

```bash
python3 .claude/skills/li-human/humanize.py /tmp/post.txt --lang pt -o /tmp/post_limpo.txt --report
python3 .claude/skills/li-human/detect.py /tmp/post_limpo.txt --lang pt
```

Reescreva à mão as estruturas sinalizadas no relatório. Se a nota
(`HUMAN SCORE`) ficar **abaixo de 70**, reescreva o post, atacando primeiro a
checagem mais fraca, e rode de novo. A nota final vai no `human_score`.

### 5. Gravar na fila

Um arquivo por post: `queue/approved/AAAA-MM-DD-HHMM-slug.md` (data e hora
locais de SP, slug em minúsculas, sem acento, com hífens):

```markdown
---
scheduled_at: 2026-10-06T08:15:00-03:00
visibility: PUBLIC          # PUBLIC ou CONNECTIONS
type: PROOF                 # PROOF | OPINION | TEACH | STORY | OFFER
hook: "#17 Time Anchor"
human_score: 84
---
Texto do post exatamente como deve ser publicado.
```

Depois valide:

```bash
python3 scripts/validate_queue.py queue/approved/<os 4 arquivos>
```

Tudo tem que passar, **exceto** placeholders `{{...}}` que você deixou de
propósito por falta de dado.

### 6. Abrir o PR

```bash
git checkout -b semana-AAAA-MM-DD        # data da segunda-feira da semana-alvo
git add queue/approved/ linkedin/plan.md
git commit -m "posts: semana de AAAA-MM-DD"
git push -u origin semana-AAAA-MM-DD
gh pr create --base main --title "Posts da semana de DD/MM" --body-file /tmp/pr.md
```

A descrição do PR tem:

- A tabela da semana:

  | dia | horário | tipo | gancho | primeira linha |
  | --- | --- | --- | --- | --- |
  | ter 06/10 | 08:15 | PROOF | #17 Time Anchor | Em março eu perdi... |

- A nota do `detect.py` de cada post.
- Uma seção **"Falta você preencher"** listando cada `{{...}}`, em qual
  arquivo e o que é necessário. Se não houver, diga "Nada a preencher".
- Um lembrete: "Merge = aprovação. Edite os arquivos direto no PR se quiser
  mudar algo."

### 7. Parar

**Não** dê merge. **Não** publique. **Não** rode o publicador. Termine
informando o link do PR.

Se `linkedin/ideias.md` estiver vazio e `voice.md` não tiver provas
suficientes, escreva mesmo assim os posts de OPINION e TEACH (que dependem de
posições, não de números) e deixe os de PROOF/STORY com `{{...}}` bem
explicados. Nunca preencha o buraco com ficção.

## Coleta semanal (roda no Mac do Luan)

Quando receber **"rodar coleta semanal"**. Esta tarefa só funciona na máquina
local, porque o código da empresa existe só lá. Ela transforma os commits da
semana em notas **sanitizadas** para `linkedin/ideias.md`. Nenhum código sai
do Mac.

**Regras de compliance (inegociáveis):**

- Repositórios de trabalho (`~/Documents/MEDGRUPO/*`) são **somente leitura**:
  só `git log`, `git show` e `git diff`. Nada de checkout, pull, fetch, commit
  ou qualquer outra alteração neles.
- Nada de código, trecho adaptado, nome de repositório, serviço, classe,
  método, tabela, fila, endpoint, variável ou arquivo da empresa nas notas.
- Nada de números internos, dados de alunos/clientes/colegas, nem detalhes de
  como uma proteção de segurança funciona por dentro.
- Cada nota descreve só: **a técnica ou padrão**, o **tipo de problema** e **o
  que o Luan aprendeu ou decidiu**. Teste: alguém de fora conseguiria
  descobrir qual sistema, qual regra ou qual número? Se sim, reescreva mais
  genérico ou descarte.
- Repositórios pessoais (`~/Documents/ProjetosPessoais/*`, exceto este) podem
  ser descritos com detalhes e números, mas **sem o nome do projeto** (está na
  blocklist): "meu projeto pessoal, um app de ..." basta.

**Passos:**

1. Para cada repositório em `~/Documents/MEDGRUPO/` e
   `~/Documents/ProjetosPessoais/`, liste os commits do Luan dos últimos 8
   dias, em todas as branches. Ele commita com mais de uma identidade (e-mail
   pessoal, corporativo e `Luan Fiszer@DESKTOP-...`), então filtre pelo nome,
   não pelo e-mail:
   `git -C <repo> log --all --no-merges -i -E --author="luan ?fiszer" --since="8 days ago" --stat`.
   O mesmo commit pode aparecer duas vezes (rebase/cherry-pick): agrupe pela
   mensagem.
2. Leia as mensagens e, quando precisar entender a técnica, os diffs
   (`git -C <repo> show <sha>`). Isso fica só na sessão; nada é copiado.
3. Escolha de 3 a 8 coisas que renderiam post: um padrão aplicado, um bug e a
   causa, uma decisão de arquitetura, um trade-off, algo que deu errado.
   Ignore commits triviais (merge, bump, formatação).
4. Acrescente ao fim de `linkedin/ideias.md` uma seção
   `## Diário técnico (coleta de AAAA-MM-DD)` com um item por ideia, marcado
   `[trabalho]` ou `[pessoal]`, no formato:
   `- [trabalho] Outbox Pattern num consumer RabbitMQ: evento se perdia quando o
   banco confirmava e a publicação falhava. Aprendi a ...`
5. Confira a blocklist e releia cada item com o teste acima:
   `python3 scripts/validate_queue.py --check-text linkedin/ideias.md`.
   Se aparecer um termo novo da empresa que deveria estar bloqueado, acrescente
   em `linkedin/blocklist.txt`.
6. Commite só `linkedin/ideias.md` (e a blocklist, se mudou) na `main` deste
   repositório com `notas: diário técnico AAAA-MM-DD` e dê push. Notas não
   são posts: nada é publicado sem passar pelo PR da rotina semanal.
7. Se não houver commits na semana, não escreva nada e diga isso.

## Mapa do repositório

| caminho | o que é |
| --- | --- |
| `.claude/skills/li-*` | skills do plugin linkedin-agent (MIT, Jake Schincariol), com caminhos adaptados para o repo |
| `.claude/skills/li-human/slop_pt.json` | léxico PT-BR do humanizador |
| `linkedin/voice.md` | perfil de voz |
| `linkedin/ideias.md` | fatos e ideias da semana + diário técnico da coleta |
| `linkedin/blocklist.txt` | termos da empresa que nunca podem aparecer num post |
| `linkedin/plan.md` | plano da semana atual |
| `linkedin/log.md` | log de publicações (escrito pelo publicador) |
| `queue/approved/` | posts aprovados (chegam por merge) |
| `queue/published/` | posts publicados, com `posted_urn` |
| `scripts/get_token.py` | OAuth local para gerar o token |
| `scripts/li_publish.py` | publicador (Actions) |
| `scripts/validate_queue.py` | validação dos PRs |

## Desenvolvimento

```bash
uv venv -p 3.12 .venv && uv pip install -p .venv/bin/python -r requirements.txt -r requirements-dev.txt
.venv/bin/python -m pytest -q
.venv/bin/python scripts/li_publish.py --dry-run
```
