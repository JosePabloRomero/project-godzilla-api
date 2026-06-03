module "database" {
  source = "../../modules/database"

  project_id        = var.project_id
  region            = var.region
  zone              = var.zone
  db_instance_name  = var.db_instance_name
  db_name           = var.db_name
  db_user           = var.db_user
  network_self_link = module.network.network_self_link
}
