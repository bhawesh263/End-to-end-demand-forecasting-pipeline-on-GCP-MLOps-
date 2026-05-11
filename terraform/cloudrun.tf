# Create a dedicated service account for Cloud Run
resource "google_service_account" "cloud_run_sa" {
  account_id   = "cloud-run-sa"
  display_name = "Service Account for Cloud Run MLOps"
}

# Grant BigQuery permissions to the Service Account
resource "google_project_iam_member" "bq_user" {
  project = var.project_id
  role    = "roles/bigquery.user"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

resource "google_project_iam_member" "bq_data_viewer" {
  project = var.project_id
  role    = "roles/bigquery.dataViewer"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# API Cloud Run Service
resource "google_cloud_run_service" "api_service" {
  name     = "demand-forecast-api"
  location = var.region

  template {
    spec {
      service_account_name = google_service_account.cloud_run_sa.email
      containers {
        # This is a placeholder image. The actual image will be pushed by GitHub Actions.
        image = "gcr.io/cloudrun/hello"
        
        resources {
          limits = {
            cpu    = "1000m"
            memory = "512Mi"
          }
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Allow unauthenticated access to API (for portfolio purposes)
resource "google_cloud_run_service_iam_member" "api_public_access" {
  location = google_cloud_run_service.api_service.location
  project  = google_cloud_run_service.api_service.project
  service  = google_cloud_run_service.api_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Frontend Cloud Run Service
resource "google_cloud_run_service" "frontend_service" {
  name     = "demand-forecast-ui"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/cloudrun/hello"
        
        resources {
          limits = {
            cpu    = "1000m"
            memory = "512Mi"
          }
        }
        
        env {
          name  = "API_URL"
          value = google_cloud_run_service.api_service.status[0].url
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "frontend_public_access" {
  location = google_cloud_run_service.frontend_service.location
  project  = google_cloud_run_service.frontend_service.project
  service  = google_cloud_run_service.frontend_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
