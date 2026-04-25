variable "project_id" {
  description = "ID del proyecto GCP"
  type        = string
}

variable "region" {
  description = "Region de la instancia Cloud SQL"
  type        = string
}

variable "zone" {
  description = "Zona de la instancia Cloud SQL"
  type        = string
}

variable "db_instance_name" {
  description = "Nombre de la instancia Cloud SQL"
  type        = string
}

variable "db_name" {
  description = "Nombre de la base de datos"
  type        = string
}

variable "db_user" {
  description = "Usuario principal de base de datos"
  type        = string
}

variable "network_self_link" {
  description = "Self link de la VPC para IP privada"
  type        = string
}
