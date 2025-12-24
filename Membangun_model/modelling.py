import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import mlflow
import os

def main():

    mlflow.set_tracking_uri("http://127.0.0.1:5000/")
    mlflow.set_experiment("Eksperimen_Diabetes_Basic")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'diabetes_preprocessing.csv')
    
    print(f"Loading data from: {file_path}")
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("ERROR: File csv tidak ditemukan. Pastikan sudah di-copy ke folder Membangun_model!")
        return

    # Pisahkan Fitur (X) dan Target (y)
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    
    # Split Data (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Autolog akan otomatis merekam:
    # - Metrics (Accuracy, dll)
    # - Parameters (n_estimators, max_depth, dll)
    # - Artifacts (Model.pkl, Confusion Matrix, dll)
    mlflow.autolog()

    # Training Model
    print("Memulai Training dengan Autolog...")
    with mlflow.start_run(run_name="Run_Basic_Angga"):

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Prediksi
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        print(f"Training Selesai! Akurasi: {acc:.4f}")
        print("Silakan cek dashboard MLflow untuk melihat grafik dan model.")

if __name__ == "__main__":
    main()