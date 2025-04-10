import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import joblib

# 1. Load data
df = pd.read_csv("medical_symptoms.csv")

# 2. Preprocessing
df['Symptoms'] = df['Symptoms'].str.lower().str.split(', ')
df['Days'] = df['Days'].astype(int)

# 3. Vectorize symptoms
mlb = MultiLabelBinarizer()
symptom_matrix = mlb.fit_transform(df['Symptoms'])

# Save this for use later
joblib.dump(mlb, 'symptom_binarizer.pkl')

# 4. Add 'Days' as a numeric feature
X = np.hstack([symptom_matrix, df[['Days']].values])

# 5. Label encode the disease type
le = LabelEncoder()
y = le.fit_transform(df['Type'])

# Save label encoder and doctors map
joblib.dump(le, 'label_encoder.pkl')
joblib.dump(dict(zip(df['Type'], df['Doctors'])), 'doctor_map.pkl')

# 6. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7. Build ANN
model = Sequential()
model.add(Dense(64, input_dim=X.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(len(set(y)), activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=100, verbose=1)

# 8. Save model
model.save("ann_model.h5")
