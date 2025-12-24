from prometheus_client import start_http_server, Counter, Gauge, Histogram
import psutil
import time
import random
import requests
import json


MODEL_URL = "http://localhost:5001/invocations" 
EXPORTER_PORT = 8000
SLEEP_INTERVAL = 2

# 10 Matriks
CPU_USAGE = Gauge('system_cpu_usage_percent', 'Current CPU usage percent')
MEMORY_USAGE = Gauge('system_memory_usage_percent', 'Current Memory usage percent')
REQUEST_COUNT = Counter('model_request_total', 'Total request sent to model')
REQUEST_LATENCY = Histogram('model_request_latency_seconds', 'Latency of model requests')
HTTP_ERROR = Counter('model_http_error_total', 'Total HTTP errors')
PREDICTION_VALUE = Gauge('model_last_prediction', 'Last prediction result (0 or 1)')
CLASS_0_COUNT = Counter('model_class_0_total', 'Total prediction result 0')
CLASS_1_COUNT = Counter('model_class_1_total', 'Total prediction result 1')
FEATURE_GLUCOSE = Gauge('feature_glucose_last', 'Last input Glucose value')
FEATURE_BMI = Gauge('feature_bmi_last', 'Last input BMI value')

def generate_dummy_data_simple():
    """Membuat data dummy format DataFrame Split (Standard MLflow)"""
    # Generate nilai acak
    pregnancies = random.randint(0, 10)
    glucose = random.randint(80, 200)
    bp = random.randint(50, 90)
    skin = random.randint(0, 50)
    insulin = random.randint(0, 300)
    bmi = random.uniform(18.0, 40.0)
    pedigree = random.uniform(0.1, 2.0)
    age = random.randint(21, 80)

    # Format Standard MLflow
    payload = {
        "dataframe_split": {
            "columns": ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"],
            "data": [[pregnancies, glucose, bp, skin, insulin, bmi, pedigree, age]]
        }
    }
    return payload, glucose, bmi

def process_request():
    # 1. Update System Metrics
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)

    # 2. Prepare Data
    payload, glucose, bmi = generate_dummy_data_simple()
    
    # Update Feature Metrics
    FEATURE_GLUCOSE.set(glucose)
    FEATURE_BMI.set(bmi)

    # 3. Hit Model
    start_time = time.time()
    try:
        response = requests.post(MODEL_URL, json=payload, headers={"Content-Type": "application/json"})
        latency = time.time() - start_time
        
        REQUEST_COUNT.inc()
        REQUEST_LATENCY.observe(latency)

        if response.status_code == 200:
            res_json = response.json()
            # Parsing output standar MLflow: {'predictions': [0]}
            result = res_json['predictions'][0]
            
            PREDICTION_VALUE.set(result)
            if result == 0:
                CLASS_0_COUNT.inc()
            else:
                CLASS_1_COUNT.inc()
            
            print(f"Sukses. Glucose: {glucose}, BMI: {bmi:.2f} -> Prediksi: {result}")
        else:
            HTTP_ERROR.inc()
            print(f"Error {response.status_code}: {response.text}")

    except Exception as e:
        HTTP_ERROR.inc()
        print(f"Connection Error: {e}")

if __name__ == '__main__':
    print(f"Exporter berjalan di port {EXPORTER_PORT}...")
    start_http_server(EXPORTER_PORT)
    print("Menunggu request pertama...")
    while True:
        process_request()
        time.sleep(SLEEP_INTERVAL)