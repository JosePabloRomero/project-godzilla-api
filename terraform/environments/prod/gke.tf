module "gke" {
  source = "../../modules/gke"

  project_id                    = var.project_id
  region                        = var.region
  cluster_name                  = var.gke_cluster_name
  network_self_link             = module.network.network_self_link
  subnet_self_link              = module.network.subnet_self_link
  pods_secondary_range_name     = var.pods_secondary_range_name
  services_secondary_range_name = var.services_secondary_range_name
}
