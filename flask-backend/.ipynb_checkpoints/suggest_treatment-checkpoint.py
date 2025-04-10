import pandas as pd

# Load dataset
df = pd.read_csv("C:/Users/SRIDEEPALAKSHMI/medi-care/medical_symptoms.csv")

def get_suggestion(predicted_disease):
    suggestion = df[df["Disease"] == predicted_disease]["Suggestion"].values
    return suggestion[0] if len(suggestion) > 0 else "No suggestion available."

# Example usage
if __name__ == "__main__":
    predicted_disease = input("Enter predicted disease: ")
    treatment_suggestion = get_suggestion(predicted_disease)
    print(f"💊 Suggested Treatment: {treatment_suggestion}")
