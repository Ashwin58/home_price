from flask import Flask, render_template, request, redirect, url_for, flash, session
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import io
import base64
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Load the saved Random Forest model
model_rf = joblib.load('random_forest_model.pkl')

# Define a function to make predictions based on user input
def predict_house_price(input_data):
    input_array = np.array(input_data).reshape(1, -1)
    prediction = model_rf.predict(input_array)
    return prediction[0]

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('Account created successfully. Please login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists')
        finally:
            conn.close()
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/about')
def about():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        input_data = [
            float(request.form['CRIM']),
            float(request.form['ZN']),
            float(request.form['INDUS']),
            int(request.form['CHAS']),
            float(request.form['NOX']),
            float(request.form['RM']),
            float(request.form['AGE']),
            float(request.form['DIS']),
            int(request.form['RAD']),
            int(request.form['TAX']),
            float(request.form['PTRATIO'])
        ]
        
        predicted_price = predict_house_price(input_data)
        
        # Feature importance visualization
        feature_importances = model_rf.feature_importances_
        feature_names = ["CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PTRATIO"]
        
        plt.style.use('dark_background')  # Set dark theme
        plt.figure(figsize=(10, 6))
        sns.barplot(x=feature_importances, y=feature_names, palette="viridis")
        plt.title("Feature Importance", color="white")
        plt.xlabel("Importance", color="white")
        plt.ylabel("Features", color="white")
        plt.tick_params(colors="white")  # Set tick colors to white
        
        # Save the plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)  # Transparent background
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close()

        # Interactive scatter plot of predicted vs. actual prices
        actual_prices = np.random.uniform(10, 50, size=100)  # Replace this with actual data
        predicted_prices = np.random.uniform(10, 50, size=100)  # Replace with your predicted prices
        df = pd.DataFrame({
            'Actual Price': actual_prices,
            'Predicted Price': predicted_prices
        })
        df_melted = df.melt(value_vars=['Actual Price', 'Predicted Price'], var_name='Price Type', value_name='Price')
        fig = px.scatter(
            df_melted, 
            x='Price Type', 
            y='Price', 
            color='Price Type', 
            title='Predicted vs Actual House Prices',
            labels={'Price Type': 'Price Type', 'Price': 'Price ($1000s)'},
            color_discrete_sequence=['cyan', 'magenta'],  # Bright colors for dark theme
            template="plotly_dark"  # Use Plotly's dark theme
        )
        scatter_plot = fig.to_html(full_html=False)

        return render_template('prediction.html', predicted_price=predicted_price * 1000, plot_url=plot_url, scatter_plot=scatter_plot)

    return render_template('prediction.html')

if __name__ == '__main__':
    app.run(debug=True)