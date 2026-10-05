// Regra de acesso por tipo de conteudo: do mais especifico pro mais generico.
// O ULTIMO fallback tem que negar. Nunca libere por padrao.
public bool PodeAcessar(ConfigDeAcesso cfg, string tipo)
{
    bool? especifico = cfg.ValorEspecifico.GetValueOrDefault(tipo);

    return especifico
        ?? cfg.PadraoGlobal
        ?? false; // tipo novo, sem regra: comeca bloqueado
}

// Errado: o ultimo fallback libera.
public bool PodeAcessarErrado(ConfigDeAcesso cfg, string tipo)
{
    bool? especifico = cfg.ValorEspecifico.GetValueOrDefault(tipo);

    return especifico
        ?? cfg.PadraoGlobal
        ?? true; // tipo novo entra liberado: o bug que ninguem ve ainda
}
