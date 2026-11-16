---
scheduled_at: 2026-11-25T07:45:00-03:00
visibility: PUBLIC
type: OPINION
hook: "#1 Contrarian Take"
human_score: 80.3
image: "media/fotos/gerado-hash-senha-rehash-login.png"
image_alt: "Cartão de código C#: migração de hash de senha errada (reset forçado) vs certa (rehash no login, ASP.NET Identity)"
image_request: "Foto de um rascunho seu, à mão, no caderno ou quadro, desenhando o fluxo 'login confere senha, se for hash antigo regrava com o novo'. Sem nada do trabalho."
---
Todo mundo acha que trocar o algoritmo de hash de senha exige forçar reset de senha de todo mundo de uma vez. Eu discordo.

O ASP.NET Core Identity já resolve isso sem reset. O método VerifyHashedPassword, da interface IPasswordHasher<TUser>, devolve um enum: PasswordVerificationResult. Um dos valores é SuccessRehashNeeded. A senha bateu, mas o hash foi feito com um algoritmo mais fraco que o configurado agora.

Dá pra migrar no login.

Quando a senha certa chega em texto puro, porque o usuário acabou de digitar ela certa, você já tem a chance que precisa. A verificação confere com o algoritmo antigo, muita base legada por aí ainda usa MD5 ou SHA-1 sem salt, aprova, e devolve esse sinal. Nesse mesmo instante, o código gera o hash de novo com o algoritmo atual, BCrypt ou Argon2id, e chama UserManager.UpdateAsync pra salvar.

Ninguém recebe e-mail. Ninguém esquece senha de novo. O usuário nem sabe que algo mudou.

Quem nunca faz login de novo fica no hash antigo até fazer. Pra esses, um prazo de expiração de conta resolve, sem o drama de um reset coletivo.

O jeito errado trata a migração como um evento único, de um dia pro outro, que obriga todo mundo a mexer na própria senha. O jeito certo trata como efeito colateral do login: acontece sozinho, usuário por usuário, até não sobrar ninguém no algoritmo velho.

Forçar reset resolve rápido no papel. Também garante uma onda de chamado de suporte e usuário irritado, por um problema que a sua própria aplicação criou.

Seu sistema confere esse sinal de rehash no login, ou ainda trata hash de senha como coisa que só se mexe uma vez?
