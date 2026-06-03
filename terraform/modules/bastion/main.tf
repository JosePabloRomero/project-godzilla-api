resource "google_compute_firewall" "allow_ssh_bastion" {
  name    = "${var.instance_name}-allow-ssh"
  project = var.project_id
  network = var.network_self_link

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = var.ssh_source_ranges
  target_tags   = ["bastion-ssh"]
}

resource "google_compute_instance" "bastion" {
  name         = var.instance_name
  project      = var.project_id
  zone         = var.zone
  machine_type = var.machine_type
  tags         = ["bastion-ssh"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
      size  = 20
      type  = "pd-balanced"
    }
  }

  network_interface {
    subnetwork = var.subnet_self_link
    access_config {}
  }

  metadata = {
    enable-oslogin = "TRUE"
  }
}
