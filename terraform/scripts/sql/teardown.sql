-- El orquestador debe conectarse primero a la base "postgres" (no a "godzilla_db")
-- y terminar sesiones activas contra "godzilla_db"; de lo contrario DROP DATABASE falla.
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'godzilla_db'
  AND pid <> pg_backend_pid();

DROP DATABASE IF EXISTS godzilla_db;
