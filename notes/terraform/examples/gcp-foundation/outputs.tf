output "network_name" {
  description = "Lab VPC name."
  value       = google_compute_network.app.name
}

output "subnet_self_link" {
  description = "Lab subnet self link."
  value       = google_compute_subnetwork.app.self_link
}
