variable "project_id" {
  description = "Existing sandbox project ID."
  type        = string
}

variable "region" {
  description = "Region for the lab subnet."
  type        = string
  default     = "us-central1"
}

variable "subnet_cidr" {
  description = "Non-overlapping RFC1918 range reserved for this lab."
  type        = string
  default     = "10.42.0.0/24"

  validation {
    condition     = can(cidrhost(var.subnet_cidr, 0))
    error_message = "subnet_cidr must be a valid CIDR range."
  }
}
