<div align="center">

# End-to-End Demand Forecasting MLOps Platform on Google Cloud

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![GCP Deploy](https://github.com/bhawesh263/End-to-end-demand-forecasting-pipeline-on-GCP-MLOps-/actions/workflows/deploy.yml/badge.svg)](https://github.com/bhawesh263/End-to-end-demand-forecasting-pipeline-on-GCP-MLOps-/actions)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat&logo=terraform&logoColor=white)](https://www.terraform.io/)

*A production-grade, serverless Machine Learning pipeline built entirely on GCP's free tiers.*

 Analytics & AI Platform 

</div>

---

## 🚀 Project Overview

This repository demonstrates a complete **Machine Learning Operations (MLOps)** lifecycle for a Demand Forecasting system. It moves beyond a simple Jupyter Notebook, providing a fully automated, scalable, and cost-efficient pipeline deployed on **Google Cloud Platform (GCP)**. 

The system automates data ingestion, model training, tracking, and evaluation, and serves predictions via a highly concurrent REST API with an interactive frontend dashboard.

## 🌟 Key Features & MLOps Highlights

* **Automated CI/CD:** GitHub Actions automates linting (`flake8`), unit testing (`pytest`), Docker image building, and continuous deployment to GCP Cloud Run.
* **Infrastructure as Code (IaC):** Entire GCP infrastructure (Cloud Run, Artifact Registry, BigQuery, IAM) is provisioned declaratively using **Terraform**.
* **Custom Model Registry & Tracking:** Lightweight Python-based tracking system that automatically versions model artifacts (`lgb_model_{timestamp}.txt`) and evaluates performance metrics (RMSE, MAE).
* **Serverless Serving Architecture:** Containerized **FastAPI** model server deployed on Cloud Run, scaling automatically from zero to handle high prediction loads.
* **Interactive Analytics Dashboard:** A **Streamlit** frontend allowing stakeholders to dynamically visualize demand forecasts.
* **Data Integration:** Direct data sourcing from **Google BigQuery** for model training.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| **Machine Learning** | LightGBM, Scikit-learn, Pandas, Numpy |
| **Backend / Serving API** | FastAPI, Uvicorn |
| **Frontend Dashboard** | Streamlit |
| **Data Warehouse** | Google BigQuery |
| **Containerization** | Docker, Docker Compose, GCP Artifact Registry |
| **Deployment / Compute** | Google Cloud Run (Serverless) |
| **CI / CD Pipeline** | GitHub Actions |
| **Infrastructure as Code** | Terraform |
| **Observability** | Google Cloud Monitoring |

## 🏗️ System Architecture

1. **Data Layer:** Raw historical sales and demand data are stored in **BigQuery**.
2. **Model Training (Local/Pipeline):** A Python script pulls data from BigQuery, engineers features, and trains a **LightGBM** model. Metrics and versioned artifacts are saved.
3. **Serving Layer:** The production model artifact is baked into a Dockerized **FastAPI** application.
4. **Presentation Layer:** A containerized **Streamlit** dashboard interacts with the FastAPI backend via RESTful endpoints.
5. **Deployment:** Both API and UI containers are deployed to **Cloud Run** via **GitHub Actions** and provisioned using **Terraform**.

## 📁 Repository Structure

```text
.
├── .github/workflows/       # GitHub Actions CI/CD pipelines (lint, test, deploy)
├── api/                     # FastAPI application for model serving
│   ├── main.py              # API entry point
│   ├── features.py          # Feature engineering logic
│   └── Dockerfile           # Backend container definition
├── frontend/                # Streamlit user interface dashboard
│   ├── app.py               # Dashboard layout and API integration
│   └── Dockerfile           # Frontend container definition
├── model/                   # Model training and tracking scripts
│   ├── train.py             # LightGBM training, evaluation, and artifact generation
│   └── model_artifacts/     # Versioned models and evaluation metrics (JSON)
├── terraform/               # Infrastructure as Code (GCP resource definitions)
├── tests/                   # Pytest suite for unit testing
├── docker-compose.yml       # Local multi-container orchestration
└── requirements_all.txt     # Global dependencies
```

## 💻 Getting Started (Local Development)

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop)
* Python 3.9+
* Google Cloud SDK (for interacting with GCP data)

### 1. Train the Model
Before running the application, generate the data and train the initial LightGBM model to produce the required model artifacts.

```bash
cd model
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 train.py
cd ..
```

### 2. Run the Application Environment (Docker)
The recommended way to spin up the entire application stack is via Docker Compose.

```bash
docker-compose up --build
```
* **API Interactive Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Streamlit Dashboard:** [http://localhost:8501](http://localhost:8501)

### 3. Run the Test Suite
Ensure code reliability by running the built-in test suite:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_all.txt
pytest tests/
flake8 .
```

## ☁️ Deployment Pipeline

This repository implements a zero-touch deployment strategy via GitHub Actions.

1. **Trigger:** Push to the `main` branch.
2. **Test:** The CI pipeline runs `flake8` for linting and `pytest` to validate application logic.
3. **Build:** Docker images for the `api` and `frontend` are built.
4. **Publish:** Images are pushed to Google Cloud Artifact Registry.
5. **Deploy:** Google Cloud Run instances are automatically updated with the latest container images.

---
*Disclaimer: This repository is a portfolio project designed to demonstrate MLOps architecture and engineering best practices.*
