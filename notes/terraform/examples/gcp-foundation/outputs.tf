output "network_name" {
  description = "Lab VPC name."
  value       = google_compute_network.app.name
}

output "subnet_self_links" {
  description = "Lab subnet self links keyed by the stable logical names from var.subnets."
  value       = { for key, subnet in google_compute_subnetwork.app : key => subnet.self_link }
}
