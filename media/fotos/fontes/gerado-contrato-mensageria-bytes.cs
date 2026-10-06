// Errado: monta o objeto na mao, nunca serializa de verdade.
var msg = new Mensagem { Campo = true };
Assert.True(Regra(msg));


// Certo: parte dos bytes reais, mesmo serializer de producao.
byte[] bytesRecebidos = CarregarFixture("campo_presente.json");
var msg2 = Serializer.Deserializar<Mensagem>(bytesRecebidos);

byte[] bytesPublicados = Serializer.Serializar(Processar(msg2));
AssertSnapshot(bytesPublicados);
