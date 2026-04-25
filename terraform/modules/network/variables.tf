variable "project_id" {
  description = "ID del proyecto GCP"
  type        = string
}

variable "region" {
  description = "Region en la que se crea la red"
  type        = string
}

variable "vpc_name" {
  description = "Nombre de la VPC"
  type        = string
}

variable "subnet_name" {
  description = "Nombre de la subnet"
  type        = string
}

variable "subnet_cidr" {
  description = "CIDR de la subnet"
  type        = string
}

variable "pods_secondary_range_name" {
  description = "Nombre del rango secundario para pods"
  type        = string
}

variable "pods_secondary_cidr" {
  description = "CIDR del rango secundario para pods"
  type        = string
}

variable "services_secondary_range_name" {
  description = "Nombre del rango secundario para servicios"
  type        = string
}

variable "services_secondary_cidr" {
  description = "CIDR del rango secundario para servicios"
  type        = string
}

variable "router_name" {
  description = "Nombre del Cloud Router"
  type        = string
  default     = "godzilla-router"
}

variable "nat_name" {
  description = "Nombre del Cloud NAT"
  type        = string
  default     = "godzilla-nat"
}
