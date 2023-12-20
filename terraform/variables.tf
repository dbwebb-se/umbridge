variable "location" {
  type        = string
  default     = "North Europe"
  description = "default resources location"
}

variable "terraform_resource_group_name" {
  type        = string
  default     = "umbridgeTerraform"
  description = "resource group name for resources managed by terraform"
}

# Containing variables that will be used in main.tf
variable "manual_resource_group_name" {
  type        = string
  default     = "umbridge"
  description = "resource group name for resource managed manuall"
}


variable "dns_records" {
  type        = list(string)
  default     = ["@", "sentry", "www", "www.sentry"]
  description = "records for dns"
}

variable "dns_name" {
  type        = string
  default     = "umbridge.arnesson.dev"
  description = "domain name for dns"
}

variable "record_ttl" {
  type        = number
  default     = 300
  description = "Number of seconds for TTL"
}

variable "ssh_name" {
  type        = string
  default     = "flask_key"
  description = "Name of shh key"
}

variable "user_name" {
  type        = string
  default     = "deploy"
  description = "Name of default user"
}
