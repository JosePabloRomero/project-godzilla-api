# Terraform IaC - Project Godzilla API

Este directorio contiene la Infraestructura como Código (IaC) para GCP usando un patrón modular por servicio y un entorno `prod`.

## Estructura Modular

- `modules/network/`: VPC custom, subredes, Cloud Router y NAT.
- `modules/gke/`: Clúster administrado GKE Autopilot.
- `modules/database/`: Cloud SQL for PostgreSQL 18 (IP privada) y Service Networking.
- `modules/bastion/`: Instancia Compute Engine para acceso seguro a la base de datos vía IAP.
- `environments/prod/`: Composición del entorno productivo unificando los módulos.
- `scripts/sql/`: Scripts de inicialización, inserción (mock data) y destrucción (teardown).
- `scripts/run_sql.sh`: Orquestador Bash que abre un túnel SSH/IAP hacia la BD privada.

## Prerrequisitos

- Terraform `>= 1.6`
- Google Cloud SDK (`gcloud`) instalado y autenticado (`gcloud auth login` y `gcloud auth application-default login`)
- La cuenta de GCP usada para operar debe tener el rol `IAP-secured Tunnel User`
- Proyecto GCP con las siguientes APIs habilitadas:
  - Compute Engine API
  - Kubernetes Engine API
  - Cloud SQL Admin API
  - Service Networking API
  - Identity-Aware Proxy (IAP) API

## Despliegue de la Infraestructura

1. Posiciónate en el entorno productivo:
```bash
cd terraform/environments/prod
```

2. Copiar variables de ejemplo:

```bash
cp terraform.tfvars.example terraform.tfvars
```

3. Editar `terraform.tfvars` con tus valores (`project_id`, redes, nombres, etc.).

## Despliegue

Inicializar:

```bash
terraform init
```

Validar:

```bash
terraform validate
```

Planificar:

```bash
terraform plan -out=tfplan
```

Aplicar:

```bash
terraform apply tfplan
```

Destruir:

```bash
terraform destroy -auto-approve
```

## Scripts SQL

El script `terraform/scripts/run_sql.sh` ahora levanta un tunel SSH por IAP hacia el Bastion Host y desde ahi se conecta a la IP privada de Cloud SQL.

Desde la raiz del repositorio, usa estos comandos:

```bash
chmod +x terraform/scripts/run_sql.sh
./terraform/scripts/run_sql.sh init --project-id <TU_PROJECT_ID> --db-user godzilla_user
./terraform/scripts/run_sql.sh teardown --project-id <TU_PROJECT_ID> --db-user godzilla_user
```

Nota tecnica: en modo `teardown`, el script se conecta por defecto a la base `postgres` para poder ejecutar el `DROP DATABASE` sin errores por conexiones activas sobre la base objetivo.
