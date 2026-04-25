# Terraform IaC - Project Godzilla API

Este directorio contiene la Infraestructura como Codigo (IaC) para GCP usando un patron modular por servicio y un entorno `prod`.

## Estructura

- `modules/`: modulos reutilizables por servicio (`network`, `gke`, `database`, `bastion`).
- `environments/prod/`: composicion del entorno productivo usando los modulos.
- `scripts/sql/`: scripts SQL de inicializacion, carga de datos y limpieza.
- `scripts/run_sql.sh`: orquestador para ejecutar scripts SQL en orden.

## Prerrequisitos

- Terraform `>= 1.6`
- Google Cloud SDK (`gcloud`) autenticado
- Proyecto GCP con APIs habilitadas:
  - Compute Engine API
  - Kubernetes Engine API
  - Cloud SQL Admin API
  - Service Networking API

## Configuracion inicial

1. Ir al entorno:

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
terraform destroy
```

## Scripts SQL

Desde la raiz del repositorio:

```bash
chmod +x terraform/scripts/run_sql.sh
./terraform/scripts/run_sql.sh init
./terraform/scripts/run_sql.sh seed
./terraform/scripts/run_sql.sh teardown
```

El script usa variables de entorno estandar de PostgreSQL (`PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`).
