


import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.neural_network import MLPClassifier
import pickle

# Load CSV
df = pd.read_csv("flask-backend/medical_symptoms.csv")
df["Symptoms"] = df["Symptoms"].str.lower().str.strip()

# Process symptoms into list
df["SymptomList"] = df["Symptoms"].apply(lambda x: [s.strip() for s in x.split(",")])

# Encode symptoms
mlb = MultiLabelBinarizer()
X = mlb.fit_transform(df["SymptomList"])

# Encode output label (Type/Disease)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["Type"])

# ANN model
model = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
model.fit(X, y)

# Save the model and encoders
with open("flask-backend/bot_model.pkl", "wb") as f:
    pickle.dump((model, mlb, label_encoder), f)

print("✅ Model and Vectorizer saved successfully!")
