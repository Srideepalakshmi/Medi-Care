import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("C:/Users/SRIDEEPALAKSHMI/medi-care/auto_model.pkl")

# Load dataset
df = pd.read_csv("C:/Users/SRIDEEPALAKSHMI/medi-care/medical_symptoms.csv")

st.title("Symptom Analyzer")

# Select symptoms
symptoms_list = df.columns[:-2]  # Exclude 'Disease' and 'Suggestion'
selected_symptoms = st.multiselect("Select Symptoms", Joint pain, stiffness, swelling
Fatigue, skin rashes, organ damage
Muscle weakness, vision problems, balance issues
Increased thirst, weight loss, frequent urination
Diarrhea, bloating, malabsorption
 )

if st.button("Predict"):
    if selected_symptoms:
        input_data = [1 if sym in selected_symptoms else 0 for sym in symptoms_list]
        disease_pred = model.predict([input_data])[0]
        suggestion = df[df["Disease"] == disease_pred].iloc[0]["Suggestion"]
        st.success(f"Disease: {disease_pred}")
        st.info(f"Suggestion: {suggestion}")
    else:
        st.warning("Please select at least one symptom.")
