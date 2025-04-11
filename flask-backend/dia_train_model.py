import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

# === Load dataset ===
df = pd.read_csv("flask-backend/diabetes_data_upload.csv")

# === Drop missing values (if any) ===
df.dropna(inplace=True)

# === Define symptom columns ===
exclude_cols = ["Age", "Gender", "Disease", "class", "Suggestion"]
symptom_columns = [col for col in df.columns if col not in exclude_cols]

# === Create symptom text string for each patient ===
def convert_row_to_text(row):
    return ", ".join([col for col in symptom_columns if row[col] == "Yes"])

df["symptom_text"] = df.apply(convert_row_to_text, axis=1)

# === Vectorize the symptom text ===
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["symptom_text"])
y = df["Disease"]  # make sure this column has: Type 1 Diabetes, Type 2 Diabetes, Gestational Diabetes

# ✅ Optional: Check if class imbalance exists
print("Disease distribution:\n", y.value_counts())

# === Train-test split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Train model with class weight balance ===
model = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
model.fit(X_train, y_train)

# === Save model and vectorizer ===
joblib.dump(model, "flask-backend/dia_model.pkl")
joblib.dump(vectorizer, "flask-backend/dia_vectorizer.pkl")

print("✅ Model and vectorizer saved successfully!")
