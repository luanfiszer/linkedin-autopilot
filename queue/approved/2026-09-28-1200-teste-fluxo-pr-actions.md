---
scheduled_at: 2026-09-28T12:00:00-03:00
visibility: CONNECTIONS     # só conexões veem
type: TEACH                 # PROOF | OPINION | TEACH | STORY | OFFER
hook: "teste"
human_score: 74.7
---
Segundo teste da automação, só pras conexões.

O primeiro teste, semana passada, validou a publicação direta: script chama a API oficial do LinkedIn, sem navegador, sem clique manual. Funcionou.

Esse aqui testa o pedaço que faltava: o post entra como arquivo, num Pull Request, eu reviso e dou merge. A partir do merge, um workflow do GitHub Actions roda a cada meia hora, olha o horário marcado no arquivo e publica sozinho quando chega a vez.

Se este texto apareceu no seu feed, os dois pedaços do fluxo estão funcionando juntos: a aprovação por merge e a publicação automática por horário. Vou apagar em seguida.

#automacao
