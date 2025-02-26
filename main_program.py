import numpy as np
from flask import Flask, render_template, request
import pickle
import sqlite3

# Initialize the Flask application
app = Flask(__name__)

# Load the saved model and encoder
with open('multi_linear_model.pkl', 'rb') as file:
    model = pickle.load(file)


# Home route to show the input form
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    area = float(request.form['area'])
    bedrooms = float(request.form['bedrooms'])
    age = float(request.form['age'])

    # Prepare the input for the model
    features = np.array([[area, bedrooms, age]])
    prediction = model.predict(features)

    con=sqlite3.connect('linear_regg.db')
    cur=con.cursor()
    sql=f"insert into input_data(area,bedrooms,age,price_prediction)values({area},{bedrooms},{age},'{prediction}')"
    cur.execute(sql)
    con.commit()
    cur.close()
    
    return render_template('index.html', price=prediction)
                           

# Run the app
if __name__ == '__main__':
    app.run(debug=True)