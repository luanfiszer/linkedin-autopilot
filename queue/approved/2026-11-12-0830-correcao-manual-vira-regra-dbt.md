---
scheduled_at: 2026-11-12T08:30:00-03:00
visibility: PUBLIC
type: TEACH
hook: "#16 Good vs Great"
human_score: 75.4
image: "media/fotos/gerado-correcao-manual-vira-regra.png"
image_alt: "Diagrama: UPDATE manual vira model dbt, com normalização do caminho e teste not_null rodando no CI a cada PR"
image_request: "Print do terminal rodando um `dbt test` (ou teste equivalente) passando, no seu projeto pessoal. Esconda nome de projeto e caminhos de pasta."
---
Dev comum corrige a linha errada na mão. Dev bom transforma a correção numa regra testada.

Um UPDATE feito à mão, pra arrumar um caminho de arquivo divergente, não batia com os valores de uma planilha de referência, um Excel que o time usava de verdade, em muitas linhas diferentes.

Não era um erro só.

Tinha barra codificada de um jeito, barra duplicada, e até arquivo com uma extensão que nem devia ter caminho registrado ali.

Resolvia a rodada.

Só aquela rodada.

Na próxima divergência, alguém ia abrir a planilha de novo, comparar à mão, e repetir o mesmo trabalho de antes, linha por linha, pra sempre.

Isso virou um Model dbt.

A planilha entrou como um Seed, o jeito do dbt de transformar uma tabela de referência em dado versionado, sem ninguém copiar e colar valor por valor.

Uma camada que lê a fonte, normaliza o caminho antes de comparar, e expõe um teste not_null que o CI roda a cada PR aberto, sem ninguém precisar lembrar de rodar nada.

A config do Model vive num arquivo YAML, não escondida numa variável que só alguém da planilha original conhecia.

SQL puro, compilado e versionado no Git.

Nada de UPDATE perdido na memória de quem rodou ele uma vez só, numa sexta-feira qualquer.

Depois eu simplifiquei.

A Macro que eu tinha criado só era usada num lugar, então virou código direto dentro do Model, sem indireção nenhuma, sem arquivo extra pra ninguém ler.

Conferi linha por linha, antes de trocar.

Idêntico.

Correção manual que não vira regra testada se repete pra sempre, do jeito que apareceu a primeira vez.

Qual correção manual do seu time já devia ter virado um teste, e ainda não virou?

#DataEngineering #BackEnd