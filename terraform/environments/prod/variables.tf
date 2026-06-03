variable "project_id" {
  description = "ID del proyecto GCP"
  type        = string
}

variable "region" {
  description = "Region principal en GCP"
  type        = string
  default     = "us-east4"
}

variable "zone" {
  description = "Zona principal en GCP"
  type        = string
  default     = "us-east4-a"
}

variable "environment" {
  description = "Nombre del entorno"
  type        = string
  default     = "prod"
}

variable "vpc_name" {
  description = "Nombre de la VPC"
  type        = string
  default     = "godzilla-vpc"
}

variable "subnet_name" {
  description = "Nombre de la subnet principal"
  type        = string
  default     = "godzilla-subnet-us-east4"
}

variable "subnet_cidr" {
  description = "CIDR de la subnet principal"
  type        = string
  default     = "10.10.0.0/20"
}

variable "pods_secondary_range_name" {
  description = "Nombre del rango secundario para pods de GKE"
  type        = string
  default     = "gke-pods-range"
}

variable "pods_secondary_cidr" {
  description = "CIDR para pods de GKE"
  type        = string
  default     = "10.20.0.0/16"
}

variable "services_secondary_range_name" {
  description = "Nombre del rango secundario para servicios de GKE"
  type        = string
  default     = "gke-services-range"
}

variable "services_secondary_cidr" {
  description = "CIDR para servicios de GKE"
  type        = string
  default     = "10.30.0.0/20"
}

variable "gke_cluster_name" {
  description = "Nombre del cluster GKE Autopilot"
  type        = string
  default     = "godzilla-api-cluster"
}

variable "db_instance_name" {
  description = "Nombre de la instancia Cloud SQL"
  type        = string
  default     = "godzilla-postgres"
}

variable "db_name" {
  description = "Nombre de la base de datos"
  type        = string
  default     = "godzilla_db"
}

variable "db_user" {
  description = "Usuario principal de la base de datos"
  type        = string
  default     = "godzilla_user"
}

variable "bastion_instance_name" {
  description = "Nombre de la instancia bastion"
  type        = string
  default     = "godzilla-bastion"
}
