// Errado: identidade inferida pelo nome (heuristica de string)
var entidade = db.Entidades
    .FirstOrDefault(x => x.Nome == novoNome);
// funciona ate duas linhas terem o mesmo Nome

// Certo: vinculo explicito numa tabela de relacao propria
public class UsuarioEntidade
{
    public Guid UsuarioId { get; set; }
    public Guid EntidadeId { get; set; }
    // chave composta (UsuarioId, EntidadeId) + indice unico
}

// Migration idempotente, com backfill pros vinculos antigos
modelBuilder.Entity<UsuarioEntidade>()
    .HasKey(x => new { x.UsuarioId, x.EntidadeId });
