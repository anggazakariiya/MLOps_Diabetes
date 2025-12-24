import requests
import json

BASE_URL = "http://localhost:5001"

print("Memeriksa kesehatan server...")

# 1. Cek Apakah Server Siap (Live/Ready)
try:
    live = requests.get(f"{BASE_URL}/v2/health/live")
    ready = requests.get(f"{BASE_URL}/v2/health/ready")
    print(f"   Status Live: {live.status_code} (Harusnya 200)")
    print(f"   Status Ready: {ready.status_code} (Harusnya 200)")
except Exception as e:
    print(f"Server mati/tidak bisa dihubungi: {e}")
    exit()

# 2. Cek Daftar Model yang Dimuat
print("\nMemeriksa daftar model...")
try:
    repo = requests.post(f"{BASE_URL}/v2/repository/index", json={})
    if repo.status_code == 200:
        models = repo.json()
        print("   Model yang ditemukan:")
        print(json.dumps(models, indent=2))
        
        # Ambil nama model pertama jika ada
        if len(models) > 0:
            nama_model = models[0]['name']
            print(f"\nNAMA MODEL YANG BENAR: '{nama_model}'")
        else:
            print("\nDAFTAR MODEL KOSONG. Server jalan tapi model gagal dimuat.")
    else:
        print(f"Gagal cek repo: {repo.status_code}")
except Exception as e:
    print(f"Error request: {e}")