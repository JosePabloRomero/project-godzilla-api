variable "project_id" {
  description = "ID del proyecto GCP"
  type        = string
}

variable "region" {
  description = "Region del cluster GKE"
  type        = string
}

variable "cluster_name" {
  description = "Nombre del cluster GKE"
  type        = string
}

variable "network_self_link" {
  description = "Self link de la VPC"
  type        = string
}

variable "subnet_self_link" {
  description = "Self link de la subnet"
  type        = string
}

variable "pods_secondary_range_name" {
  description = "Rango secundario para pods"
  type        = string
}

variable "services_secondary_range_name" {
  description = "Rango secundario para servicios"
  type        = string
}
