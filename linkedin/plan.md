# Plano da semana de 12/10 a 18/10/2026

Semana-alvo: segunda a domingo começando na próxima segunda-feira depois de
hoje (05/10/2026). Fontes: `linkedin/voice.md` (posições, provas) e
`linkedin/ideias.md` (diário técnico das coletas de 25/09 e 28/09). Nenhum
tema, gancho ou história repete o que já saiu entre 26/09 e 04/10
(`linkedin/log.md`, `queue/published/`).

| dia | horário (America/Sao_Paulo) | tipo | gancho | ângulo |
| --- | --- | --- | --- | --- |
| ter 13/10 | 08:15 | PROOF | #17 Time Anchor | Query com vários joins projetando uma coluna de JSON grande: o produto cartesiano repetia o JSON em cada linha, a resposta foi de rápida a estourar o timeout. Correção: buscar o JSON numa consulta separada, uma vez só. |
| qua 14/10 | 08:00 | OPINION | #18 The Unpopular Rule | Regra de permissão composta por cadeia de coalescência (valor específico ?? padrão global ?? nega): o último fallback tem que ser negar, nunca liberar, pra um tipo novo sem regra nascer bloqueado. |
| qui 15/10 | 07:45 | TEACH | #16 Good vs Great | Mensageria não garante ordem nem exatamente-uma-entrega: comparar o timestamp de quem publicou (não a ordem de chegada) e reprocessar de forma idempotente. |
| sex 16/10 | 08:30 | STORY | #19 Curiosity Gap | A fila de erro (dead-letter) estava configurada certinho e nunca recebeu nada: a classe base dos consumers capturava toda exceção antes dela chegar na biblioteca, então a mensagem que falhava era descartada em silêncio e o trace marcava sucesso. |

Nenhum dia repetido, nenhum tipo dois dias seguidos, 1 post por dia, todos
entre 7h30 e 9h30, terça a sexta (sem posts à tarde).

## Engajamento

Não há lista de pessoas/empresas definida ainda em `linkedin/ideias.md`
(campo não preenchido pelo usuário). `{{lista de 10 pessoas/empresas pra
engajar: 5 de alcance, 3 pares, 2 compradores}}` — preencher quando tiver.

## Ideias não usadas nesta semana (ficam pra depois)

- Documento derivado que também guarda estado (reconstrução do zero zerava progresso).
- Revert antes de acertar (vínculo inferido por nome vira registro órfão).
- Correção manual de dados vira regra versionada (normalização + teste dbt).
- Spec antes do fix (OpenSpec: proposta, design, spec antes do código).
- Gambiarra provisória desenhada para ser apagada (remendo que não contamina o dado persistido).
- Provas de voice.md ainda não usadas: PROVER chat em legado (Long Polling/AJAX), desafio técnico do trainee (API REST com Clean Architecture), microsserviços de autenticação do MEDGRUPO (JWT, MFA, geofencing, detecção de VPN, migração de hash — só no nível de conceito).
