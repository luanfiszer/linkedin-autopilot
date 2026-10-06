// Antes: cada consulta precisa lembrar do filtro.
var itens = db.Itens.Where(i => !i.Excluido).ToList();


// Depois: filtro global no DbContext. Ninguem esquece.
protected override void OnModelCreating(ModelBuilder b)
{
    b.Entity<Item>().HasQueryFilter(i => !i.Excluido);
}


// So aqui, de forma explicita, ve os excluidos tambem.
var todos = db.Itens.IgnoreQueryFilters().ToList();
