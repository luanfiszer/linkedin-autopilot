// Teste de adapter: banco em memória deixa passar

// Em memória: não bate com as regras do banco real
services.AddDbContext<AppDbContext>(o =>
    o.UseInMemoryDatabase("teste"));

await repo.SalvarAsync(pedidoDuplicado);
// passa, mesmo com UNIQUE no banco real

// Com Testcontainers: Postgres de verdade
var postgres = new PostgreSqlBuilder().Build();
await postgres.StartAsync();

services.AddDbContext<AppDbContext>(o =>
    o.UseNpgsql(postgres.GetConnectionString()));

await repo.SalvarAsync(pedidoDuplicado);
// estoura DbUpdateException: viola a constraint UNIQUE
