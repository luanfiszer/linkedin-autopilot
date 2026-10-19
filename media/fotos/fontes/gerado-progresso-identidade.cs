// Errado: heuristica de posicao (1 item antes, 1 item depois = "mesmo")
bool DevePreservarProgresso(List<Guid> idsAntes, List<Guid> idsDepois)
{
    return idsAntes.Count == 1 && idsDepois.Count == 1;
    // o item pode ter sido totalmente trocado, e isso ainda retorna true
}

// Certo: identidade, nao posicao
bool DevePreservarProgresso(IEnumerable<Guid> idsAntes, IEnumerable<Guid> idsDepois)
{
    if (!idsDepois.Any())
        return false; // etapa vazia nao conta

    var ordenadosAntes = idsAntes.OrderBy(id => id);
    var ordenadosDepois = idsDepois.OrderBy(id => id);

    return ordenadosAntes.SequenceEqual(ordenadosDepois);
}

// So recalcula os grupos que de fato mudaram de composicao
IEnumerable<Guid> GruposParaRecalcular(
    IEnumerable<Grupo> gruposAntes, IEnumerable<Grupo> gruposDepois)
{
    return gruposAntes
        .GroupBy(g => g.EtapaId)
        .Where(g => !DevePreservarProgresso(
            g.Select(x => x.Id),
            gruposDepois.Where(d => d.EtapaId == g.Key).Select(x => x.Id)))
        .Select(g => g.Key);
}
