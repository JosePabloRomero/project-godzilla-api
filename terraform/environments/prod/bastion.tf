module "bastion" {
  source = "../../modules/bastion"

  project_id        = var.project_id
  zone              = var.zone
  instance_name     = var.bastion_instance_name
  subnet_self_link  = module.network.subnet_self_link
  network_self_link = module.network.network_self_link
}
