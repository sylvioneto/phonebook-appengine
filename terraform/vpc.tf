module "vpc" {
  source       = "terraform-google-modules/network/google"
  version      = "~> 5.0"
  project_id   = var.project_id
  network_name = "appengine-vpc"
  routing_mode = "GLOBAL"

  subnets = [
    {
      subnet_name           = "webapp-${var.region}"
      subnet_ip             = "10.0.0.0/28"
      subnet_region         = var.region
      subnet_private_access = true
    },
  ]
}

resource "google_vpc_access_connector" "appengine_vpc_connector" {
  name          = "appengine-vpc-access"
  ip_cidr_range = "10.200.0.0/28"
  network       = module.vpc.network_name
}

resource "google_compute_global_address" "service_range" {
  name          = "address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = module.vpc.network_id
}

resource "google_service_networking_connection" "private_service_connection" {
  network                 = module.vpc.network_id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.service_range.name]
}

