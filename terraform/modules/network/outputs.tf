output "network_name" {
  description = "Nombre de la VPC"
  value       = google_compute_network.vpc.name
}

output "network_self_link" {
  description = "Self link de la VPC"
  value       = google_compute_network.vpc.self_link
}

output "subnet_name" {
  description = "Nombre de la subnet"
  value       = google_compute_subnetwork.subnet.name
}

output "subnet_self_link" {
  description = "Self link de la subnet"
  value       = google_compute_subnetwork.subnet.self_link
}
