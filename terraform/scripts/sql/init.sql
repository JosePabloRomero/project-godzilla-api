-- Inicializacion de esquema base
CREATE TABLE IF NOT EXISTS healthcheck (
  id SERIAL PRIMARY KEY,
  status TEXT NOT NULL DEFAULT 'ok',
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
