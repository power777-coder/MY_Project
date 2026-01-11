import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'ml', 'price_model.pkl')

model = joblib.load(MODEL_PATH)

def predict_price(waste_type, weight_kg):
    prediction = model.predict([{
        'waste_type': waste_type,
        'weight_kg': weight_kg
    }])
    return round(float(prediction[0]), 2)
