data "google_project" "project" {}

locals {
  resource_labels = {
    terraform = "true"
    app       = "app-eng-phonebook"
    purpose   = "demo"
    env       = "sandbox"
    repo      = "terraform_gcp"
  }
  application_name = "phonebook"
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

