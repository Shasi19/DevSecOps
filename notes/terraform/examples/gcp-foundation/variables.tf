variable "project_id" {
  description = "Existing sandbox project ID."
  type        = string
}

variable "region" {
  description = "Region for the lab subnet."
  type        = string
  default     = "us-central1"
}

variable "subnets" {
  description = "Subnets keyed by stable logical name; do not use generated IDs as keys."
  type = map(object({
    cidr   = string
    region = string
  }))
  default = {
    app = {
      cidr   = "10.42.0.0/24"
      region = "us-central1"
    }
    data = {
      cidr   = "10.42.1.0/24"
      region = "us-central1"
    }
  }

  validation {
    condition     = alltrue([for subnet in values(var.subnets) : can(cidrhost(subnet.cidr, 0))])
    error_message = "Every subnet cidr must be a valid CIDR range."
  }
}

variable "allow_health_check_ingress" {
  description = "Create a narrowly targeted health-check firewall rule for backend VMs tagged web-backend."
  type        = bool
  default     = false
}
