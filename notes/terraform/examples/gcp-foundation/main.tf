terraform {
  required_version = ">= 1.6.0, < 2.0.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_compute_network" "app" {
  name                    = "devsecops-lab"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "app" {
  name                     = "devsecops-lab-private"
  ip_cidr_range            = var.subnet_cidr
  region                   = var.region
  network                  = google_compute_network.app.id
  private_ip_google_access = true
}

resource "google_compute_firewall" "allow_health_check" {
  name      = "devsecops-lab-health-check"
  network   = google_compute_network.app.name
  direction = "INGRESS"
  priority  = 1000
  source_ranges = [
    "35.191.0.0/16",
    "130.211.0.0/22",
  ]
  target_tags = ["web-backend"]

  allow {
    protocol = "tcp"
    ports    = ["8080"]
  }
}
