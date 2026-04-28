-- Inicializacion de esquema para dominio de vehiculos
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS vehicles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  make VARCHAR(50) NOT NULL,
  model VARCHAR(80) NOT NULL,
  year INTEGER NOT NULL,
  nickname VARCHAR(50) NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
