# 🏥 End-to-End MLOps: Diabetes Prediction System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![MLflow](https://img.shields.io/badge/MLflow-Tracking%20%26%20Serving-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C)
![Grafana](https://img.shields.io/badge/Grafana-Observability-F46800)

## 📖 Project Overview
Repository ini berisi implementasi lengkap siklus **Machine Learning Operations (MLOps)** untuk kasus prediksi penyakit diabetes. Proyek ini mendemonstrasikan bagaimana model machine learning tidak hanya dilatih, tetapi juga di-deploy, dipantau kesehatannya, dan divisualisasikan kinerjanya secara real-time.

Tujuan utama proyek ini adalah membangun sistem yang *robust* (tahan banting) dengan menerapkan standar **Serving**, **Monitoring**, dan **Alerting**.

## 🏗️ System Architecture
Sistem ini dibangun dengan alur kerja (pipeline) sebagai berikut:

1.  **Model Training & Tuning:** Menggunakan **Scikit-Learn** dan **MLflow** untuk melatih model *Random Forest Classifier* dengan hyperparameter tuning. Artifacts (Confusion Matrix, ROC Curve) disimpan secara otomatis.
2.  **Model Serving:** Model dibungkus (containerized) menggunakan **Docker** dengan backend **MLServer** untuk menyediakan API prediksi (`/invocations`) yang stabil.
3.  **Data Logging (Exporter):** Script Python custom (`prometheus_exporter.py`) berfungsi sebagai jembatan yang mengirimkan *dummy traffic* dan mengekspos metrics sistem ke Prometheus.
4.  **Monitoring:** **Prometheus** mengumpulkan (scrape) data metrics setiap beberapa detik.
5.  **Visualization & Alerting:** **Grafana** memvisualisasikan data tersebut ke dalam Dashboard interaktif dan mengirimkan notifikasi jika terjadi anomali (misal: Latency tinggi atau CPU spike).

## 🚀 Key Features

### 1. Advanced Model Training
- **Algorithm:** Random Forest Classifier.
- **Tracking:** Eksperimen dicatat menggunakan MLflow Tracking.
- **Artifacts:** Tersimpan bukti evaluasi model berupa grafik Confusion Matrix dan ROC Curve.

### 2. Scalable Model Serving
- Menggunakan **Docker Container** untuk isolasi environment.
- Endpoint API siap menerima request prediksi dalam format JSON.
- Konfigurasi `MLSERVER_PARALLEL_WORKERS` disesuaikan untuk stabilitas resource.

### 3. Comprehensive Monitoring (Prometheus)
Memantau 3 aspek vital:
- **System Health:** CPU Usage, RAM Usage.
- **Traffic:** Total Request, Error Rate, Latency.
- **Data Drift & Business Logic:** Distribusi input (Glucose, BMI) dan hasil prediksi (Sehat vs Diabetes).

### 4. Observability Dashboard (Grafana)
Dashboard terpusat yang menampilkan **10 Panel Visualisasi** dan dilengkapi dengan **3 Alert Rules**:
- 🚨 **High CPU Warning**
- 🚨 **High Latency Detection**
- 🚨 **Memory Usage Alert**

## 📂 Project Structure

```text
MLops_Diabetes/
├── Membangun_model/
│   ├── requirements.txt            # Dependencies project
│   └── (Notebooks/Scripts Training)
├── Monitoring dan Logging/
│   ├── inference.py                # Script testing API endpoint
│   ├── prometheus_exporter.py      # Custom metrics exporter
│   └── prometheus.yml              # Konfigurasi target Prometheus
├── Eksperimen_SML_Angga Zakariya.txt   # Dokumentasi/Catatan Eksperimen
├── Workflow-CI.txt                     # Dokumentasi Workflow CI/CD
