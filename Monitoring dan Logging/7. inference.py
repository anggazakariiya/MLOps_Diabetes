import requests
import json

# Alamat Server Docker
url = "http://localhost:5001/invocations"

# Data
data = {
    "dataframe_split": {
        "columns": ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"],
        "data": [[1, 85, 66, 29, 0, 26.6, 0.351, 31]]
    }
}

print("Mengirim data ke model")

try:
    # Kirim request POST ke server
    response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
    
    # Cek respon
    if response.status_code == 200:
        print("\nPrediksi:")
        print(response.json())
    else:
        print(f"\nGagal. Kode Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"\nTidak bisa konek ke server. Pastikan Docker sudah 'run'.")
    print(f"Error: {e}")