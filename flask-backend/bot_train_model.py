import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.neural_network import MLPClassifier
import joblib
import os

# Create backend directory if not exists
os.makedirs("flask-backend", exist_ok=True)

# Load CSV
df = pd.read_csv("flask-backend/medical_symptoms.csv")
df["Symptoms"] = df["Symptoms"].str.lower().str.strip()

# Convert comma-separated symptoms into list
df["SymptomList"] = df["Symptoms"].apply(lambda x: [s.strip() for s in x.split(",")])

# Encode symptoms
symptom_binarizer = MultiLabelBinarizer()
X = symptom_binarizer.fit_transform(df["SymptomList"])

# Encode diseases
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["Type"])

# Train ANN model using scikit-learn
model = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42)
model.fit(X, y)

# Save model and encoders using joblib
joblib.dump(model, "flask-backend/ann_model.pkl")
joblib.dump(symptom_binarizer, "flask-backend/symptom_binarizer.pkl")
joblib.dump(label_encoder, "flask-backend/label_encoder.pkl")

print("✅ Model, symptom binarizer, and label encoder saved successfully!")
