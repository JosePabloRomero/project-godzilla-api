output "network_name" {
  description = "Nombre de la VPC creada"
  value       = module.network.network_name
}

output "gke_cluster_name" {
  description = "Nombre del cluster GKE"
  value       = module.gke.cluster_name
}

output "cloudsql_instance_name" {
  description = "Nombre de la instancia Cloud SQL"
  value       = module.database.instance_name
}

output "cloudsql_private_ip" {
  description = "IP privada de la instancia Cloud SQL"
  value       = module.database.private_ip_address
}

output "bastion_public_ip" {
  description = "IP publica del bastion"
  value       = module.bastion.public_ip
}
