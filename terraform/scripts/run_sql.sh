#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQL_DIR="${SCRIPT_DIR}/sql"
TF_ENV_DIR="${SCRIPT_DIR}/../environments/prod"

ACTION=""
PROJECT_ID="${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || true)}"
BASTION_INSTANCE="${BASTION_INSTANCE:-godzilla-bastion-v3}"
BASTION_ZONE="${BASTION_ZONE:-us-east4-b}"
DB_PRIVATE_IP="${DB_PRIVATE_IP:-}"
DB_PORT="${DB_PORT:-5432}"
LOCAL_PORT="${LOCAL_PORT:-55432}"
APP_DB_NAME="${APP_DB_NAME:-godzilla_db}"
DB_USER="${DB_USER:-godzilla_user}"
DB_PASSWORD="${DB_PASSWORD:-}"
USE_IAP=true
TUNNEL_PID=""

log() {
  echo "[run_sql] $*"
}

die() {
  echo "[run_sql][ERROR] $*" >&2
  exit 1
}

usage() {
  cat <<'EOF'
Uso:
  ./terraform/scripts/run_sql.sh [init|seed|teardown|all] [opciones]

Opciones:
  --project-id <id>         ID del proyecto GCP
  --bastion-instance <name> Nombre de la VM bastion
  --bastion-zone <zone>     Zona de la VM bastion
  --db-private-ip <ip>      IP privada de Cloud SQL
  --db-port <port>          Puerto de Cloud SQL (default: 5432)
  --local-port <port>       Puerto local para tunel (default: 55432)
  --app-db-name <name>      Base de aplicacion (default: godzilla_db)
  --db-user <user>          Usuario PostgreSQL (default: godzilla_user)
  --db-password <pwd>       Password PostgreSQL (si se omite, se solicita)
  --no-iap                  No usar IAP (usa SSH directo al bastion)
  -h, --help                Mostrar ayuda

Notas:
  - Estrategia implementada: Opcion B (tunel SSH local via bastion).
  - Para teardown, el script se conecta a la base "postgres" para poder ejecutar DROP DATABASE.
EOF
}

prompt_action() {
  echo "Selecciona fase SQL:"
  echo "  1) init"
  echo "  2) seed"
  echo "  3) teardown"
  echo "  4) all"
  read -r -p "Opcion [1-4]: " option
  case "${option}" in
    1) ACTION="init" ;;
    2) ACTION="seed" ;;
    3) ACTION="teardown" ;;
    4) ACTION="all" ;;
    *) die "Opcion invalida: ${option}" ;;
  esac
}

resolve_db_private_ip() {
  if [[ -n "${DB_PRIVATE_IP}" ]]; then
    return
  fi

  if command -v terraform >/dev/null 2>&1 && [[ -d "${TF_ENV_DIR}" ]]; then
    DB_PRIVATE_IP="$(terraform -chdir="${TF_ENV_DIR}" output -raw cloudsql_private_ip 2>/dev/null || true)"
  fi

  [[ -n "${DB_PRIVATE_IP}" ]] || die "No se pudo resolver DB_PRIVATE_IP. Pasa --db-private-ip o exporta DB_PRIVATE_IP."
}

check_dependencies() {
  command -v gcloud >/dev/null 2>&1 || die "gcloud no esta instalado."
  command -v psql >/dev/null 2>&1 || die "psql no esta instalado."
  command -v ssh >/dev/null 2>&1 || die "ssh no esta instalado."
}

parse_args() {
  if [[ $# -gt 0 ]]; then
    case "${1}" in
      init|seed|teardown|all)
        ACTION="${1}"
        shift
        ;;
    esac
  fi

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --project-id) PROJECT_ID="${2:-}"; shift 2 ;;
      --bastion-instance) BASTION_INSTANCE="${2:-}"; shift 2 ;;
      --bastion-zone) BASTION_ZONE="${2:-}"; shift 2 ;;
      --db-private-ip) DB_PRIVATE_IP="${2:-}"; shift 2 ;;
      --db-port) DB_PORT="${2:-}"; shift 2 ;;
      --local-port) LOCAL_PORT="${2:-}"; shift 2 ;;
      --app-db-name) APP_DB_NAME="${2:-}"; shift 2 ;;
      --db-user) DB_USER="${2:-}"; shift 2 ;;
      --db-password) DB_PASSWORD="${2:-}"; shift 2 ;;
      --no-iap) USE_IAP=false; shift ;;
      -h|--help) usage; exit 0 ;;
      *) die "Parametro no reconocido: $1" ;;
    esac
  done
}

wait_for_tunnel() {
  local retries=30
  local sleep_seconds=1
  local i
  for ((i=1; i<=retries; i++)); do
    if (echo >"/dev/tcp/127.0.0.1/${LOCAL_PORT}") >/dev/null 2>&1; then
      return 0
    fi
    sleep "${sleep_seconds}"
  done
  return 1
}

cleanup() {
  if [[ -n "${TUNNEL_PID}" ]]; then
    kill "${TUNNEL_PID}" >/dev/null 2>&1 || true
  fi
}

open_tunnel() {
  local ssh_flags=()
  if [[ "${USE_IAP}" == "true" ]]; then
    ssh_flags+=(--tunnel-through-iap)
  fi

  log "Abriendo tunel localhost:${LOCAL_PORT} -> ${DB_PRIVATE_IP}:${DB_PORT} via bastion ${BASTION_INSTANCE}..."
  gcloud compute ssh "${BASTION_INSTANCE}" \
    --project "${PROJECT_ID}" \
    --zone "${BASTION_ZONE}" \
    "${ssh_flags[@]}" \
    -- \
    -o ExitOnForwardFailure=yes \
    -N \
    -L "${LOCAL_PORT}:${DB_PRIVATE_IP}:${DB_PORT}" \
    >/dev/null 2>&1 &

  TUNNEL_PID=$!
  if ! wait_for_tunnel; then
    die "No se pudo establecer el tunel SSH. Verifica bastion, IAM y conectividad."
  fi
  log "Tunel SSH activo (PID ${TUNNEL_PID})."
}

run_sql_file() {
  local phase="$1"
  local sql_file="$2"
  local target_db="$3"

  log "Ejecutando fase '${phase}' sobre DB '${target_db}'..."
  PGPASSWORD="${DB_PASSWORD}" psql \
    "host=127.0.0.1 port=${LOCAL_PORT} dbname=${target_db} user=${DB_USER} sslmode=disable" \
    -v ON_ERROR_STOP=1 \
    -f "${sql_file}"
  log "Fase '${phase}' completada."
}

confirm_drop_for_all() {
  local answer
  read -r -p "La opcion 'all' ejecutara tambien teardown (DROP DATABASE). Continuar? [y/N]: " answer
  [[ "${answer}" == "y" || "${answer}" == "Y" ]] || die "Operacion cancelada por el usuario."
}

main() {
  parse_args "$@"
  check_dependencies

  [[ -n "${ACTION}" ]] || prompt_action
  [[ -n "${PROJECT_ID}" ]] || die "PROJECT_ID vacio. Configura gcloud o pasa --project-id."
  [[ -n "${BASTION_INSTANCE}" ]] || die "BASTION_INSTANCE vacio."
  [[ -n "${BASTION_ZONE}" ]] || die "BASTION_ZONE vacio."
  [[ -n "${APP_DB_NAME}" ]] || die "APP_DB_NAME vacio."
  [[ -n "${DB_USER}" ]] || die "DB_USER vacio."

  resolve_db_private_ip

  if [[ -z "${DB_PASSWORD}" ]]; then
    read -r -s -p "DB password para '${DB_USER}': " DB_PASSWORD
    echo
  fi
  [[ -n "${DB_PASSWORD}" ]] || die "DB_PASSWORD vacio."

  trap cleanup EXIT
  open_tunnel

  case "${ACTION}" in
    init)
      run_sql_file "init" "${SQL_DIR}/init.sql" "${APP_DB_NAME}"
      ;;
    seed)
      run_sql_file "seed" "${SQL_DIR}/seed.sql" "${APP_DB_NAME}"
      ;;
    teardown)
      run_sql_file "teardown" "${SQL_DIR}/teardown.sql" "postgres"
      ;;
    all)
      confirm_drop_for_all
      run_sql_file "init" "${SQL_DIR}/init.sql" "${APP_DB_NAME}"
      run_sql_file "seed" "${SQL_DIR}/seed.sql" "${APP_DB_NAME}"
      run_sql_file "teardown" "${SQL_DIR}/teardown.sql" "postgres"
      ;;
    *)
      die "Accion invalida: ${ACTION}"
      ;;
  esac
}

main "$@"
