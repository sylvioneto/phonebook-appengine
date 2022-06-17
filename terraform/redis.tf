resource "google_redis_instance" "cache" {
  name           = "phonebook-cache"
  tier           = "STANDARD_HA"
  memory_size_gb = 1
  region         = var.region
  labels         = local.resource_labels

  authorized_network = module.vpc.network_id
  connect_mode       = "PRIVATE_SERVICE_ACCESS"

  redis_version = "REDIS_4_0"
  display_name  = "Phonebook cache"

  depends_on = [google_service_networking_connection.private_service_connection]
}
