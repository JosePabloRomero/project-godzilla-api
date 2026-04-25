output "instance_name" {
  description = "Nombre de la instancia bastion"
  value       = google_compute_instance.bastion.name
}

output "public_ip" {
  description = "IP publica de la instancia bastion"
  value       = google_compute_instance.bastion.network_interface[0].access_config[0].nat_ip
}
