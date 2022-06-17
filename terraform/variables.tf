data "google_project" "project" {}

locals {
  application_name = "phonebook"
  resource_labels = {
    terraform = "true"
    app       = local.application_name
    purpose   = "demo"
    env       = "sandbox"
    repo      = "phonebook-appengine"
  }
}

variable "project_id" {
  description = "GCP Project ID"
  default     = null
}

variable "region" {
  type        = string
  description = "GCP region"
  default     = "southamerica-east1"
}

