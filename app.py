from flask import Flask, render_template, jsonify, request
import subprocess


# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template("home.html")

# Route for Student Registration
@app.route('/registration')


def registration():
    return render_template('registration.html')

@app.route("/mark", methods=["POST"])
def mark_attendance():
    try:
        # Run recognition.py as a subprocess
        result = subprocess.run(["python", "recognition.py"], capture_output=True, text=True)
        
        # Check if the script ran successfully
        if result.returncode == 0:
            return jsonify({"message": "Attendance marked successfully."})
        else:
            return jsonify({"message": f"Error in recognition script: {result.stderr}"}), 500
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
@app.route('/table')
def table():
    return render_template('table.html')

if __name__ == "__main__":
    app.run(debug=True)
