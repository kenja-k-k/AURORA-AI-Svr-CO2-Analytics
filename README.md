# AURORA AI Service – CO₂ Analytics

This repository contains the **CO₂ Analytics AI Service**, part of the broader **AURORA Project**, focused on verifiable carbon monitoring and reporting using **AI**, **blockchain**, and **IoT** technologies.

The service demonstrates how simulated IoT data from Carbon Capture and Storage (CCS) facilities can be analyzed and visualized in real-time, providing actionable insights and alerts to improve operational performance and sustainability outcomes.

---

## 1. High-Level Architecture

The AURORA system integrates **SingularityNET**, AI Services, blockchain-based verification, and IoT data streams into a cohesive decentralized platform.

### System Overview
![AURORA Architecture](Architecture.jpg)

### Key Components
- **SingularityNET Integration**
  - Users and admins access the **Marketplace** and **Publisher Portal** to test and deploy AI services.
  - The CO₂ Analytics service is published to the marketplace for discovery and consumption.

- **Virtual Machine / Backend**
  - Each AI service runs inside **isolated containers**:
    - **Service 1 (CO₂ Analytics)** – Implemented in this repository.
    - **Service 2, Service 3, etc.** – Future services for additional analytics and reporting.
  - Blockchain hashing ensures secure and tamper-proof records.
  - IoT data streams (simulated in PoC) feed into the analytics service for processing.

- **Frontend (Optional)**
  - A dashboard visualizes live performance metrics, insights, and alerts.

- **Database Container**
  - Stores processed data and enables querying for historical analysis.

---

## 2. Role of This Service

This repository specifically implements **Service 1 Backend (CO₂ Analytics)** highlighted in **Container 1** of the architecture.

- **Input:** Simulated IoT data streams mimicking CCS facility operations (CO₂ emissions, capture rates, storage conditions, etc.).
- **Output:** Real-time metrics, actionable operational insights, and proactive alerts.
- **Blockchain Integration:** Sends hashed analytics data to the BC/Hashing service for verifiable storage.

This forms the foundation for a scalable, production-ready carbon tracking and reporting system.

---

## 3. PoC Features and Requirements

The **Proof of Concept (PoC)** demonstrates three primary features using simulated IoT data, as specified in the *CO₂ Analytics Specification*:

| Feature ID | Feature Name          | Description                                                                 |
|------------|-----------------------|-----------------------------------------------------------------------------|
| **1.1**    | Live Performance Metrics | Real-time dashboard showing CCS facility performance and capture efficiency. |
| **1.2**    | Actionable Insights      | AI-powered operational recommendations based on pattern detection.          |
| **1.3**    | Proactive Alerts         | Real-time warnings for anomalies and potential disruptions.                 |

**Summary of PoC Objectives:**
- Demonstrate live CO₂ analytics using **simulated IoT data**.
- Highlight **real-time monitoring** and detection of emission patterns.
- Showcase AI-generated insights and alerts that deliver operational value.

---

## 4. Repository Structure

The repository is structured to reflect the modular design of the CO₂ Analytics service.  
Each directory corresponds to a layer in the system, from raw data ingestion to analytics, alerts, and optional frontend visualization.

| Path / File                      | Description                                                                                      | Related Features |
|----------------------------------|--------------------------------------------------------------------------------------------------|------------------|
| **`/data/`**                     | **Sample simulated IoT datasets** used for testing and development. Includes CO₂ emission, capture rates, storage metrics, and anomaly simulation files. | 1.1, 1.2, 1.3 |
| **`/data/generator.py`**         | Python utility to generate realistic simulated IoT data streams in JSON and CSV formats.          | 1.1 |
| **`/backend/`**                  | Core backend service logic for data ingestion, processing, and analytics pipeline. Runs inside **Container 1** of the architecture. | All features |
| **`/backend/service.py`**        | Main service entry point. Handles API endpoints, incoming data streams, and routing to analytics modules. | All features |
| **`/backend/processing/`**       | Submodule containing analytics processing logic.                                                  | 1.1, 1.2 |
| **`/backend/processing/realtime.py`** | Processes incoming data in real time for metrics computation.                              | 1.1 |
| **`/backend/processing/insights.py`** | Machine learning models for detecting patterns and generating operational recommendations.   | 1.2 |
| **`/backend/alerts.py`**         | Anomaly detection and proactive alerting engine. Integrates with thresholds and machine learning models to detect anomalies such as emission spikes or efficiency drops. | 1.3 |
| **`/backend/blockchain/`**       | Interfaces with blockchain hashing service to store verifiable hashes of analytics data.           | 1.1 |
| **`/backend/daemon/`**           | Configuration files and scripts for **SingularityNET Daemon** integration, enabling the service to be published and consumed via the SingularityNET marketplace. | 1.1 |
| **`/frontend/`** *(optional)*    | Minimal dashboard frontend to visualize live performance metrics, trends, and alerts.             | 1.1 |
| **`/frontend/app.js`**           | React-based dashboard to display metrics, insights, and anomalies with real-time updates.         | 1.1 |
| **`/frontend/components/`**      | Modular UI components such as charts, tables, and alert pop-ups.                                 | 1.1 |
| **`/docs/PoC_Specification.pdf`**| The original PoC requirements document, describing functional and technical expectations for the service. | Reference |
| **`/tests/`**                     | Unit and integration tests covering data ingestion, analytics processing, and alert generation.   | 1.1, 1.2, 1.3 |
| **`/tests/test_service.py`**     | Tests core service functions, ensuring metrics and insights are calculated correctly.             | 1.1, 1.2 |
| **`/tests/test_alerts.py`**      | Validates detection logic for anomalies and alert notifications.                                  | 1.3 |
| **`Dockerfile`**                  | Container build instructions for deploying the backend service within its isolated runtime environment. | Deployment |
| **`docker-compose.yml`**         | Orchestration for multi-container setup, including backend, frontend, and database containers.    | Deployment |
| **`README.md`**                   | This file: comprehensive overview, installation, and usage instructions.                         | Documentation |

---

## 5. Deployment Instructions

### Prerequisites
- **Docker** for containerized deployment.
- **Python 3.10+** for backend services.
- **SingularityNET CLI** for publishing to the marketplace.
- **Metamask Wallet (TestNet Account)** for blockchain testnet interactions.

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/kenja-k-k/AURORA-AI-Svr-CO2-Analytics.git
   cd AURORA-AI-Svr-CO2-Analytics
2. **Build and run the container:**
   ```bash
   docker build -t co2-analytics-service .
   docker run -p 8000:8000 co2-analytics-service
3. **Access the service:**
    Backend API: http://localhost:8000/api/v1
    Optional frontend dashboard: http://localhost:3000
4. **Publish to SingularityNet testnet (optional) 
      Configure daemon files in /backend/daemon/.
     Use the SingularityNET Publisher Portal
