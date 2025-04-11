from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
import joblib
import numpy as np
import os
app = Flask(__name__)

# Load model and resources
model = load_model("flask-backend/ann_model.h5")
label_encoder = joblib.load("flask-backend/label_encoder.pkl")
symptom_binarizer = joblib.load("flask-backend/symptom_binarizer.pkl")
doctor_map = joblib.load("flask-backend/doctor_map.pkl")

# Context storage
chat_context = {}

@app.route("/")
def index():
    return render_template("frontend/templates/indexbot.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_message = request.form["msg"].lower().strip()

    # Greetings
    if user_message in ['hi', 'hello', 'hey','hi.', 'hello.', 'hey.']:
        chat_context['step'] = 'greet'
        return "👋 Hi, how can I help you today? Please describe your symptoms."

    # Thank you or Bye
    if user_message in ['thanks', 'thank you', 'thank u', 'bye','thanku','thankyou','thanks.', 'thank you.', 'thank u.', 'bye.','thanku.','thankyou.']:
        chat_context.clear()
        return "😊 You're welcome! Take care and get well soon!"

    # Step 1: Get Symptoms
    if chat_context.get('step') == 'greet':
        if user_message in ['nothing', 'no', 'none', 'n/a', 'na']:
            chat_context.clear()
            return "✅ You seem to be doing okay. I'm always here to help if you need anything! 🤖"

        symptoms_list = [s.strip() for s in user_message.split(",") if s.strip()]

        if len(symptoms_list) < 3:
            chat_context.clear()
            return ("✅ You seem to be doing okay based on the symptoms provided. "
                    "I'm not 100% sure since I'm an AI 🤖. "
                    "For more information, please consult with a doctor or visit our website.")

        chat_context['symptoms'] = symptoms_list
        chat_context['step'] = 'ask_days'
        return "📆 How many days have you had these symptoms?"

    # Step 2: Get Duration
    elif chat_context.get('step') == 'ask_days':
        try:
            chat_context['days'] = int(user_message)
        except ValueError:
            return "❗ Please enter the number of days as a number (e.g., 2)."
        chat_context['step'] = 'ask_history'
        return "📋 Any medical history? If yes, please provide details. If not, say 'no'."

    # Step 3: Get History and Predict
    elif chat_context.get('step') == 'ask_history':
        chat_context['history'] = user_message
        chat_context['step'] = 'done'

        symptoms_list = chat_context['symptoms']
        days = chat_context['days']

        try:
            input_features = symptom_binarizer.transform([symptoms_list])
        except Exception:
            chat_context.clear()
            return "⚠️ I couldn't understand your symptoms. Please try again with clear comma-separated symptoms."

        input_with_days = np.hstack([input_features, [[days]]])
        prediction = model.predict(input_with_days)
        pred_index = np.argmax(prediction)
        disease = label_encoder.inverse_transform([pred_index])[0]
        doctor = doctor_map.get(disease, "a general physician")

        chat_context.clear()

        return (f"🩺 Based on your symptoms, you might be experiencing **{disease}**. "
                f"I'm not 100% sure since I'm an AI 🤖. "
                f"For more accurate diagnosis, please consult with **{doctor}** or visit our website.")

    # Default fallback
    if chat_context.get('step'):
        return "❗ I didn't catch that. Could you please follow up with what I asked?"
    else:
        chat_context.clear()
        return ("✅ You seem to be doing okay. I'm not 100% sure since I'm an AI 🤖. "
                "For more information, please consult with a doctor or visit our website.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 50012))  # Render provides PORT dynamically
    app.run(host="0.0.0.0", port=port, debug=True)
