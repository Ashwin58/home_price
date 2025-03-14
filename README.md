# House Price Prediction

This is a Flask-based web application that predicts house prices based on user input. It uses a pre-trained Random Forest model and provides interactive visualizations.

## Features
- User authentication (Login & Signup)
- House price prediction using a trained Random Forest model
- Feature importance visualization using Matplotlib & Seaborn
- Interactive scatter plot using Plotly
- Secure user session management with SQLite

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Flask
- SQLite
- Required Python libraries (see below)

### Clone the Repository
```sh
git clone https://github.com/Ashwin58/home_price.git
cd home_price
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Initialize Database
```sh
python -c "from app import init_db; init_db()"
```

## Running the Application
```sh
python app.py
```
Access the app in your browser at `http://127.0.0.1:5000/`

## Usage
1. **Sign up** for an account.
2. **Login** to access the home page.
3. Navigate to the **Prediction** page and enter house features.
4. View the **predicted price** and visualizations.
5. Logout when done.

## File Structure
```
/House Price Prediction
│── static/                 # Static files (CSS, JS, Images)
│── templates/              # HTML templates
│── database.db             # SQLite database
│── app.py                  # Flask application
│── random_forest_model.pkl # Pre-trained model
│── requirements.txt        # Dependencies
│── README.md               # Project documentation
```

## Technologies Used
- **Flask** (Backend framework)
- **SQLite** (Database)
- **Joblib** (Model loading)
- **Matplotlib & Seaborn** (Feature importance visualization)
- **Plotly** (Interactive scatter plots)

## License
This project is licensed under the MIT License.

## Author
[Ashwin Dhungana](https://github.com/Ashwin58)

