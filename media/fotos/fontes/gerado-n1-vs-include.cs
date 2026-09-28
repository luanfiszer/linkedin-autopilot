// Antes: N+1 - uma consulta extra por item do resultado
var pedidos = db.Pedidos.ToList();

foreach (var pedido in pedidos)
{
    pedido.Cliente = db.Clientes
        .First(c => c.Id == pedido.ClienteId);
}

// Depois: uma unica ida ao banco, com os dados relacionados
var pedidos = db.Pedidos
    .Include(p => p.Cliente)
    .ToList();
