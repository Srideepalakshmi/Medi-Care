import joblib

# Load model and vectorizer
model = joblib.load("bot_model.pkl")
vectorizer = joblib.load("bot_vectorizer.pkl")

def predict_disease(symptom_input):
    try:
        input_transformed = vectorizer.transform([symptom_input])
        prediction = model.predict(input_transformed)
        return prediction[0]
    except Exception as e:
        return f"Error: {str(e)}"

# Test input
symptoms = "Thirst, frequent urination, tiredness, blurred vision"
print("Prediction:", predict_disease(symptoms))
