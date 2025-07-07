# backend/train_model.py

import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt

# Set paths
DATA_PATH = os.path.join("data", "balanced_dataset_1000.csv")
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "randomforest_bot_detector.joblib")
SCALER_PATH = os.path.join(MODEL_DIR, "standard_scaler.joblib")

# Step 1: Load dataset
df = pd.read_csv(DATA_PATH)

# ✅ Optional: Shuffle 1% labels (robustness)
np.random.seed(42)
num_samples = len(df)
shuffle_indices = np.random.choice(df.index, size=int(0.01 * num_samples), replace=False)
df.loc[shuffle_indices, 'label'] = 1 - df.loc[shuffle_indices, 'label']

# Step 2: Split features and labels
X = df.drop("label", axis=1)
y = df["label"]

# ✅ Penalize answer_length (reduce its influence)
X['answer_length'] = X['answer_length'] * 0.1  # You can try 0.1 to 0.3 for tuning

# Step 3: Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 5: Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Step 6: Evaluate
y_pred = model.predict(X_test_scaled)
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 🔍 Step 6.5: Feature Importance
importances = model.feature_importances_
feature_names = X.columns
importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("\n📊 Feature Importances:")
print(importance_df)

# Optional: Save importance plot
plt.figure(figsize=(8, 5))
plt.barh(importance_df['Feature'], importance_df['Importance'], color='skyblue')
plt.xlabel('Importance')
plt.title('Feature Importance in RandomForest Model')
plt.gca().invert_yaxis()
plt.tight_layout()

# Ensure models folder exists
os.makedirs(MODEL_DIR, exist_ok=True)
plt.savefig(os.path.join(MODEL_DIR, "feature_importance.png"))
plt.close()

# Step 7: Save model and scaler
joblib.dump(model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)

print(f"\n✅ Model saved to: {MODEL_PATH}")
print(f"✅ Scaler saved to: {SCALER_PATH}")
