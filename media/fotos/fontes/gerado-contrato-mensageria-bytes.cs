public class ContratoMensageriaTests
{
    [Theory]
    [InlineData("campo_presente")]
    [InlineData("campo_ausente")]
    [InlineData("revogacao_tardia")]
    public async Task Consome_mensagem_pelos_bytes_reais(string caso)
    {
        // Serializa como a mensagem sai de produção: não monta objeto na mão
        byte[] bytesRecebidos = Fixture.CarregarMensagem(caso);

        await _consumidor.ProcessarAsync(bytesRecebidos);

        byte[] bytesPublicados = await _fila.UltimaMensagemPublicadaAsync();

        Fixture.ValidarContrato(caso, bytesPublicados);
    }
}

// campo_presente:    RevogadoEm chega e segue até o fim do pipeline
// campo_ausente:     mensagem antiga sem a propriedade; default decidido
// revogacao_tardia:  sobrescreve pela chave natural o que já estava gravado
