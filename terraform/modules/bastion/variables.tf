variable "project_id" {
  description = "ID del proyecto GCP"
  type        = string
}

variable "zone" {
  description = "Zona de despliegue"
  type        = string
}

variable "instance_name" {
  description = "Nombre de la instancia bastion"
  type        = string
}

variable "subnet_self_link" {
  description = "Self link de la subnet donde vive el bastion"
  type        = string
}

variable "network_self_link" {
  description = "Self link de la VPC del bastion"
  type        = string
}

variable "machine_type" {
  description = "Tipo de maquina para bastion"
  type        = string
  default     = "e2-micro"
}

variable "ssh_source_ranges" {
  description = "Rangos permitidos para SSH"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
