#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQL_DIR="${SCRIPT_DIR}/sql"

if [[ -z "${ACTION}" ]]; then
  echo "Uso: $0 {init|seed|teardown}"
  exit 1
fi

case "${ACTION}" in
  init)
    SQL_FILE="${SQL_DIR}/init.sql"
    ;;
  seed)
    SQL_FILE="${SQL_DIR}/seed.sql"
    ;;
  teardown)
    SQL_FILE="${SQL_DIR}/teardown.sql"
    ;;
  *)
    echo "Accion invalida: ${ACTION}"
    echo "Uso: $0 {init|seed|teardown}"
    exit 1
    ;;
esac

required_vars=(PGHOST PGPORT PGDATABASE PGUSER PGPASSWORD)
for var_name in "${required_vars[@]}"; do
  if [[ -z "${!var_name:-}" ]]; then
    echo "Falta variable de entorno requerida: ${var_name}"
    exit 1
  fi
done

echo "Ejecutando ${SQL_FILE} en ${PGHOST}:${PGPORT}/${PGDATABASE}..."
psql -v ON_ERROR_STOP=1 -f "${SQL_FILE}"
echo "Ejecucion completada."
