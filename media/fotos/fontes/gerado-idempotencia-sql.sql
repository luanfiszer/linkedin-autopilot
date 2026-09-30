-- a chave vem num header e mora no mesmo registro
CREATE TABLE falas (
    id               bigserial PRIMARY KEY,
    idempotency_key  text        NOT NULL,
    audio_path       text        NOT NULL,
    criado_em        timestamptz NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX ux_falas_idempotency_key
    ON falas (idempotency_key);

-- o app reenviou o mesmo áudio? o banco recusa a segunda linha
INSERT INTO falas (idempotency_key, audio_path)
VALUES ($1, $2);
