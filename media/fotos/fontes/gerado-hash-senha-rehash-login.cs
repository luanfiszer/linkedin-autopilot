// Jeito errado: migração em massa, forçando reset de todo mundo
await foreach (var usuario in _repo.TodosAsync())
{
    usuario.ForcarResetDeSenha = true; // e-mail pra todo mundo, hoje
    await _repo.AtualizarAsync(usuario);
}

// Jeito certo: migra sozinho, como efeito colateral do login
public async Task<SignInResult> LoginAsync(string email, string senha)
{
    var usuario = await _userManager.FindByEmailAsync(email);
    if (usuario is null) return SignInResult.Failed;

    var resultado = _hasher.VerifyHashedPassword(usuario, usuario.PasswordHash, senha);

    if (resultado == PasswordVerificationResult.Failed)
        return SignInResult.Failed;

    if (resultado == PasswordVerificationResult.SuccessRehashNeeded)
    {
        usuario.PasswordHash = _hasher.HashPassword(usuario, senha);
        await _userManager.UpdateAsync(usuario);
    }

    return SignInResult.Success;
}
