<div align="center">

# End-to-End Demand Forecasting MLOps Platform on Google Cloud
### *A Free, Production-Grade Portfolio Project*

**Built entirely on free tiers — no paid tools, no credit card surprises.**

🎯 **Target Role:** Software Developer — Analytics & AI Platform (REWE digital)

</div>

---

## 🚀 Overview

This repository contains an end-to-end, production-grade MLOps pipeline for Demand Forecasting, deployed entirely on Google Cloud Platform (GCP). The primary goal of this project is to demonstrate the ability to architect, build, and deploy a robust Machine Learning system focusing on automation, scalability, and cost-efficiency.

## 🛠️ Skills & Technologies Demonstrated

* **Programming:** Python
* **Machine Learning:** LightGBM, MLOps (Model Tracking, Registry, Evaluation)
* **Cloud Platform (GCP):** BigQuery, Cloud Run, Cloud Monitoring
* **Infrastructure as Code (IaC):** Terraform
* **CI/CD:** GitHub Actions
* **Backend:** FastAPI
* **Frontend:** Streamlit

## 🏗️ Architecture

*(Architecture Diagram Placeholder - To be added)*

1. **Data Ingestion & Storage:** Raw data is stored and processed using **BigQuery**.
2. **Model Training:** A **LightGBM** demand forecasting model is trained.
3. **Model Deployment:** The trained model is served via a **FastAPI** application, containerized and deployed on **Cloud Run**.
4. **User Interface:** A **Streamlit** dashboard interacts with the FastAPI backend to visualize forecasts.
5. **CI/CD:** **GitHub Actions** automates testing, container building, and deployment.
6. **Infrastructure:** All GCP resources are provisioned via **Terraform**.
7. **Monitoring:** **Cloud Monitoring** tracks application health and performance.

## 📁 Project Structure

```text
.
├── .github/workflows/       # CI/CD pipelines
├── api/                     # FastAPI model serving application
├── frontend/                # Streamlit user interface
├── model/                   # LightGBM training scripts and ML tracking
├── terraform/               # Infrastructure as Code
└── README.md
```

## 🚀 Getting Started

*(Setup instructions will be added here as the project development progresses)*

---
*This project is built for portfolio demonstration purposes.*
