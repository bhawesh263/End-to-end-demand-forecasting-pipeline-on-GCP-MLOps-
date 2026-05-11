# Enable necessary APIs
resource "google_project_service" "run_api" {
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "build_api" {
  service            = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}

# BigQuery Dataset
resource "google_bigquery_dataset" "ml_dataset" {
  dataset_id    = "demand_forecasting_data"
  friendly_name = "Demand Forecasting Data"
  description   = "Dataset for MLOps demand forecasting project"
  location      = "US" # Multi-region US is often free tier eligible for small storage
}

# Artifact Registry to store Docker Images
resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = "mlops-repo"
  description   = "Docker repository for API and Frontend"
  format        = "DOCKER"
}

# Terraform State Bucket
resource "google_storage_bucket" "terraform_state" {
  name          = "${var.project_id}-tf-state"
  location      = "US"
  force_destroy = false
  versioning {
    enabled = true
  }
}
