output "cluster_name" {
  description = "Nombre del cluster GKE"
  value       = google_container_cluster.autopilot.name
}

output "endpoint" {
  description = "Endpoint del control plane"
  value       = google_container_cluster.autopilot.endpoint
}
