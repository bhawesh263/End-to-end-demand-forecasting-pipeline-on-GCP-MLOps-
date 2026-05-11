terraform {
  required_version = ">= 1.0"
  
  # Note: You must uncomment this block and replace YOUR_PROJECT_ID after the bucket is created.
  # backend "gcs" {
  #   bucket  = "YOUR_PROJECT_ID-tf-state"
  #   prefix  = "terraform/state"
  # }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
