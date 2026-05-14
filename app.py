from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model
model = joblib.load("phishing_model.pkl")

# Feature extraction function
def extract_features(url):

    feature1 = 1 if "https" in url else 0

    feature2 = url.count('.')

    feature3 = 1 if '-' in url else 0

    return [feature1, feature2, feature3]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    url = request.form['url']

    features = extract_features(url)

    final_features = [np.array(features)]

    prediction = model.predict(final_features)

    if prediction[0] == 1:
        result = "Safe Website"
    else:
        result = "Phishing Website"

    return render_template(
        'index.html',
        prediction_text=result
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)