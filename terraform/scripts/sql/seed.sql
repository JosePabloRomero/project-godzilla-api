-- Carga de datos iniciales
INSERT INTO healthcheck (status)
VALUES ('seeded')
ON CONFLICT DO NOTHING;
