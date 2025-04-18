# app.py

from flask import Flask, request, render_template
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Load dataset and train model at startup
# Make sure 'USA_Housing.csv' is in the same directory as this script
HouseDF = pd.read_csv('USA_Housing.csv')

# Define features and target
X = HouseDF[[
    'Avg. Area Income',
    'Avg. Area House Age',
    'Avg. Area Number of Rooms',
    'Avg. Area Number of Bedrooms',
    'Area Population'
]]
y = HouseDF['Price']

# Split and train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)
model = LinearRegression()
model.fit(X_train, y_train)

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        # Retrieve form inputs and convert to floats
        features = [
            float(request.form['income']),
            float(request.form['age']),
            float(request.form['rooms']),
            float(request.form['bedrooms']),
            float(request.form['population'])
        ]
        # Predict using the trained model
        prediction = model.predict([features])[0]
        prediction = round(prediction, 2)

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
