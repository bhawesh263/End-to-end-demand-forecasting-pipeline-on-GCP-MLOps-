variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region for resources (use a free-tier eligible region like us-central1)"
  type        = string
  default     = "us-central1"
}
