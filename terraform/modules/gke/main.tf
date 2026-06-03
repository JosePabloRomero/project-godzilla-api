resource "google_container_cluster" "autopilot" {
  name     = var.cluster_name
  project  = var.project_id
  location = var.region

  network    = var.network_self_link
  subnetwork = var.subnet_self_link

  deletion_protection = false

  enable_autopilot = true

  ip_allocation_policy {
    cluster_secondary_range_name  = var.pods_secondary_range_name
    services_secondary_range_name = var.services_secondary_range_name
  }
}
